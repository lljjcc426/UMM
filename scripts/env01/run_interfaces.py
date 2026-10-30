"""Run three approved native Lance interfaces and preserve every attempted result."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import resource
import runpy
import shutil
import subprocess
import sys
import time
import traceback


def save_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def inference_args(bundle: Path, inputs: Path, output: Path, task: str, plan: dict) -> list:
    fixed = {
        "model_path": str(bundle / "upstream/downloads/Lance_3B_Video"),
        "vit_path": str(bundle / "upstream/downloads/Qwen2.5-VL-ViT"),
        "vit_type": "qwen_2_5_vl_original", "llm_qk_norm": "true",
        "llm_qk_norm_und": "true", "llm_qk_norm_gen": "true",
        "tie_word_embeddings": "false", "validation_num_timesteps": plan["denoising_steps"],
        "validation_timestep_shift": 3.5, "copy_init_moe": "true", "max_num_frames": 121,
        "max_latent_size": 64, "visual_und": "true", "visual_gen": "true", "vae_model_type": "wan",
        "apply_qwen_2_5_vl_pos_emb": "true", "apply_chat_template": "false", "cfg_type": 0,
        "global_seed": plan["seed"], "validation_data_seed": plan["seed"],
        "video_height": plan["height"], "video_width": plan["width"], "num_frames": plan["num_frames"],
        "task": task, "save_path_gen": str(output), "resolution": "video_480p", "text_template": "true",
        "cfg_text_scale": plan["cfg_text_scale"], "use_KVcache": str(plan["use_kv_cache"]).lower(),
        "enhance_prompt": str(plan["enhance_prompt"]).lower(),
        "val_dataset_config_file": str(inputs / f"{task}.json"),
    }
    args = [part for key, value in fixed.items() for part in ("--" + key, str(value))]
    return args + ["--latent_patch_size", "1", "1", "1"]


def inspect_outputs(task: str, output: Path) -> dict:
    """Check native media/text actually exists; this is not a stroke-order evaluator."""
    if task == "x2t_video":
        rows = json.loads((output / "result.json").read_text())
        valid = len(rows) == 1 and bool(str(rows[0].get("answer", "")).strip())
        return {"valid": valid, "answer_count": len(rows), "artifact": "outputs/result.json"}
    import imageio.v2 as imageio
    videos = sorted(output.glob("*.mp4"))
    decoded = []
    for path in videos:
        with imageio.get_reader(str(path), format="ffmpeg") as reader:
            count = 0
            shape = None
            for frame in reader:
                count += 1
                shape = list(frame.shape)
            decoded.append({"path": "outputs/" + path.name, "decoded_frames": count, "last_frame_shape": shape})
    valid = len(decoded) == 1 and decoded[0]["decoded_frames"] > 1 and decoded[0]["last_frame_shape"][-1] == 3
    return {"valid": valid, "videos": decoded, "meaning": "RGB decoding only; no scientific accuracy claim"}


def worker(bundle: Path, attempt: Path, task: str, plan: dict) -> int:
    started = time.perf_counter()
    metrics = {"task": task, "status": "failed", "cuda_peak_allocated_bytes": None,
               "cuda_peak_reserved_bytes": None, "gpu": None, "error": None}
    torch = None
    code = 1
    try:
        import torch
        if not torch.cuda.is_available() or torch.cuda.device_count() != plan["expected_gpu_count"]:
            raise RuntimeError("This approved recipe requires one visible CUDA GPU")
        torch.cuda.set_device(0)
        torch.cuda.reset_peak_memory_stats(0)
        device = torch.cuda.get_device_properties(0)
        metrics.update(gpu=device.name, gpu_total_bytes=device.total_memory,
                       torch_version=torch.__version__, cuda_runtime=torch.version.cuda,
                       python_version=platform.python_version())
        source = bundle / "upstream"
        os.chdir(source)
        sys.path.insert(0, str(source))
        sys.argv = [str(source / "inference_lance.py")] + inference_args(
            bundle, attempt.parent / "inputs", attempt / "outputs", task, plan)
        try:
            runpy.run_path(str(source / "inference_lance.py"), run_name="__main__")
        except SystemExit as exit_status:
            if exit_status.code not in (None, 0):
                raise
        torch.cuda.synchronize()
        metrics["status"] = "process_completed"
        code = 0
    except BaseException as error:
        metrics["error"] = {"type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc()}
        traceback.print_exc()
    finally:
        if torch is not None and torch.cuda.is_initialized():
            metrics["cuda_peak_allocated_bytes"] = torch.cuda.max_memory_allocated(0)
            metrics["cuda_peak_reserved_bytes"] = torch.cuda.max_memory_reserved(0)
        metrics["worker_elapsed_seconds_including_loading"] = time.perf_counter() - started
        metrics["host_peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        save_json(attempt / "worker_metrics.json", metrics)
    return code


def assess_attempt(task: str, attempt: Path, return_code: int) -> dict:
    result = {"task": task, "exit_code": return_code, "status": "failed", "sample_denominator": 1,
              "worker_metrics": "worker_metrics.json", "log": "process.log", "output_check": None}
    metrics_path = attempt / "worker_metrics.json"
    if metrics_path.is_file():
        result["measurements"] = json.loads(metrics_path.read_text())
    if return_code == 0:
        try:
            result["output_check"] = inspect_outputs(task, attempt / "outputs")
            if result["output_check"]["valid"]:
                result["status"] = "interface_passed"
        except Exception as error:
            result["output_check"] = {"valid": False, "error": str(error)}
    return result


def gpu_sample_peak(path: Path) -> dict:
    values = []
    for line in path.read_text().splitlines():
        try:
            values.append(float(line.split(",")[1].strip()))
        except (ValueError, IndexError):
            continue
    return {"device_used_memory_peak_mib": max(values) if values else None,
            "sample_count": len(values), "interval_seconds": 1,
            "limitation": "Whole visible device, sampled once per second; short peaks may be missed"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true", help="Print commands without importing GPU libraries")
    parser.add_argument("--tasks", nargs="+", choices=("x2t_video", "t2v", "i2v"),
                        help="Retry selected approved interfaces without repeating successful ones")
    parser.add_argument("--worker-task", choices=("x2t_video", "t2v", "i2v"), help=argparse.SUPPRESS)
    parser.add_argument("--attempt", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    plan = json.loads((bundle / "plan.json").read_text())
    if not args.dry_run and plan.get('approval', {}).get('user_approved') is not True:
        parser.error('GPU execution requires explicit approval recorded in this plan')
    if args.worker_task:
        return worker(bundle, args.attempt.resolve(), args.worker_task, plan)
    tasks = [task for task in plan["tasks"] if args.tasks is None or task in args.tasks]
    if args.dry_run:
        for task in tasks:
            print(json.dumps({"task": task, "argv": inference_args(bundle, bundle / "inputs",
                             bundle / "runs/EXAMPLE" / task / "outputs", task, plan)}, ensure_ascii=False))
        return 0

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run = bundle / "runs" / run_id
    run.mkdir(parents=True, exist_ok=False)
    summary = {"experiment_id": plan.get("experiment_id", "ENV-01"), "run_id": run_id, "status": "running",
               "approved_scope": plan["scope"], "plan": plan, "attempts": [], "sample_denominator": len(tasks),
               "selected_tasks": tasks, "not_selected_tasks": [task for task in plan["tasks"] if task not in tasks],
               "started_at_utc": datetime.now(timezone.utc).isoformat(),
               "setup_attempts": sorted(path.name for path in (bundle / "setup").glob("*")),
               "cost": {"spending_cap_cny": None, "actual_billed_cny": None,
                        "note": "User approved no spending cap. Rental bill, setup and idle time remain to be reconciled."},
               "scientific_claim": ("P1 generation attempt only; actual RGB requires independent evaluation"
                                    if "request" in plan else
                                    "Native interface executability only; full ENV-01 remains incomplete")}
    save_json(run / "summary.json", summary)
    started = time.perf_counter()
    try:
        if "request" not in plan:
            if __package__:
                from .fixtures import prepare_inputs
            else:
                from fixtures import prepare_inputs
            prepare_inputs(bundle, plan, encode_video=True)
        shutil.copytree(bundle / "inputs", run / "inputs")
        # Make execution inputs immutable within this run directory.
        for task in plan["tasks"]:
            sample = (run / "inputs" / f"{task}.json").read_text()
            if "request" in plan and task == "i2v":
                sample = json.loads(sample)
                for row in sample.values():
                    for index, kind in enumerate(row["element_dtype_array"]):
                        if kind == "image":
                            media = Path(row["interleave_array"][index])
                            row["interleave_array"][index] = str(run / "inputs" / media.name)
                save_json(run / "inputs" / f"{task}.json", sample)
            else:
                (run / "inputs" / f"{task}.json").write_text(sample.replace(str(bundle / "inputs"), str(run / "inputs")))
        env = os.environ.copy()
        env.update(CUDA_VISIBLE_DEVICES="0", EXP_HW_20250819="False", POSITION_EMBEDDING_3D_VERSION="v2",
                   CUDA_LAUNCH_BLOCKING="0", PYTHONUNBUFFERED="1", TOKENIZERS_PARALLELISM="false",
                   HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", WANDB_MODE="disabled")
        for key in ("RANK", "WORLD_SIZE", "LOCAL_RANK"):
            env.pop(key, None)
        for task in tasks:
            attempt = run / task
            attempt.mkdir()
            command = [sys.executable, str(Path(__file__).resolve()), "--bundle", str(bundle),
                       "--worker-task", task, "--attempt", str(attempt)]
            save_json(attempt / "command.json", {"command": command,
                      "native_argv": inference_args(bundle, run / "inputs", attempt / "outputs", task, plan),
                      "environment_overrides": {k: env[k] for k in ("CUDA_VISIBLE_DEVICES", "EXP_HW_20250819",
                                                "POSITION_EMBEDDING_3D_VERSION", "HF_HUB_OFFLINE")}})
            print(f"Starting {task}: {attempt}", flush=True)
            task_started = time.perf_counter()
            execution_error = None
            interrupted = False
            return_code = 1
            with (attempt / "gpu_samples.csv").open("w") as gpu_log, (attempt / "process.log").open("w") as log:
                monitor = subprocess.Popen(["nvidia-smi", "-i", "0", "--query-gpu=timestamp,memory.used,memory.total,utilization.gpu",
                                            "--format=csv,noheader,nounits", "-l", "1"], stdout=gpu_log, stderr=subprocess.STDOUT)
                process = None
                try:
                    process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                               text=True, bufsize=1)
                    for line in process.stdout:
                        log.write(line)
                        log.flush()
                        print(line, end="", flush=True)
                    return_code = process.wait()
                except BaseException as error:
                    execution_error = {"type": type(error).__name__, "message": str(error),
                                       "traceback": traceback.format_exc()}
                    interrupted = isinstance(error, KeyboardInterrupt)
                    if process is not None:
                        if process.poll() is None:
                            process.terminate()
                            try:
                                process.wait(timeout=10)
                            except subprocess.TimeoutExpired:
                                process.kill()
                                process.wait()
                        return_code = process.returncode or 1
                finally:
                    monitor.terminate()
                    monitor.wait()
            result = assess_attempt(task, attempt, return_code)
            result.update(gpu_sampling=gpu_sample_peak(attempt / "gpu_samples.csv"),
                          wall_seconds=time.perf_counter() - task_started,
                          path=task)
            if execution_error:
                result.update(status="failed", runner_error=execution_error)
            save_json(attempt / "result.json", result)
            summary["attempts"].append(result)
            save_json(run / "summary.json", summary)
            print(f"{task}: {result['status']}", flush=True)
            if interrupted:
                raise KeyboardInterrupt("Interrupted task was stopped and retained")
    except BaseException as error:
        summary["runner_error"] = {"message": str(error), "traceback": traceback.format_exc()}
        traceback.print_exc()
    finally:
        passed = sum(row["status"] == "interface_passed" for row in summary["attempts"])
        summary.update(status="interfaces_passed" if passed == len(tasks) else "incomplete_or_failed",
                       passed_interfaces=passed, attempted_interfaces=len(summary["attempts"]),
                       unattempted_tasks=[t for t in tasks if t not in [a["task"] for a in summary["attempts"]]],
                       elapsed_seconds=time.perf_counter() - started,
                       finished_at_utc=datetime.now(timezone.utc).isoformat())
        save_json(run / "summary.json", summary)
        print(f"Retained run: {run}", flush=True)
    return 0 if summary["status"] == "interfaces_passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
