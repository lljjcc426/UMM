"""Small, original RGB fixtures for native interfaces, not a research dataset."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import subprocess
import zlib


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)


def write_canvas(path: Path, width: int, height: int, horizontal: float, vertical: float) -> None:
    pixels = bytearray(b"\xff" * (width * height * 3))
    left, right = width // 3, width * 2 // 3
    top, bottom = height // 4, height * 3 // 4
    radius = max(2, height // 96)
    if horizontal > 0:
        end = left + round((right - left) * horizontal)
        for y in range(height // 2 - radius, height // 2 + radius + 1):
            start = (y * width + left) * 3
            pixels[start:(y * width + end + 1) * 3] = b"\x00" * ((end - left + 1) * 3)
    if vertical > 0:
        end = top + round((bottom - top) * vertical)
        for y in range(top, end + 1):
            start = (y * width + width // 2 - radius) * 3
            pixels[start:start + (2 * radius + 1) * 3] = b"\x00" * ((2 * radius + 1) * 3)
    scanlines = b"".join(b"\x00" + pixels[y * width * 3:(y + 1) * width * 3] for y in range(height))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
                     + png_chunk(b"IDAT", zlib.compress(scanlines)) + png_chunk(b"IEND", b""))


def prepare_inputs(bundle: Path, plan: dict, encode_video: bool = False) -> dict:
    inputs = bundle / "inputs"
    frames = inputs / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    for index in range(plan["num_frames"]):
        progress = index / (plan["num_frames"] - 1)
        write_canvas(frames / f"{index:03d}.png", plan["width"], plan["height"],
                     min(1.0, progress * 2), max(0.0, progress * 2 - 1))
    write_canvas(inputs / "prefix.png", plan["width"], plan["height"], 1.0, 0.0)
    prompt = ("A fixed camera looks straight at a plain white canvas. Black ink forms the Chinese character 十 "
              "one stroke at a time: first a horizontal stroke from left to right, then a vertical stroke "
              "from top to bottom through its center. No hand, no pen, no camera motion.")
    samples = {
        "t2v": {"0001": prompt},
        "i2v": {"0001": {"interleave_array": [
            "Continue this actual canvas by forming a vertical black ink stroke from top to bottom through "
            "the center of the existing horizontal stroke. Preserve the horizontal stroke and white background. "
            "Fixed camera, no hand or pen.", str((inputs / "prefix.png").resolve())],
            "element_dtype_array": ["text", "image"], "istarget_in_interleave": [0, 0]}},
        "x2t_video": {"0001": {"interleave_array": [str((inputs / "observed_strokes.mp4").resolve()), [
            "Watch the video carefully and answer the question.",
            "Describe how the black ink strokes appear over time, including their order and direction.",
            "Reference answer withheld."]], "element_dtype_array": ["video", "text"],
            "istarget_in_interleave": [0, 1]}}
    }
    for task, sample in samples.items():
        (inputs / f"{task}.json").write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n")
    manifest = {"origin": "Original deterministic straight-stroke drawing; no external dataset or font",
                "purpose": "Native interface input only; no calibration or performance evidence",
                "i2v_visible_input": "Completed horizontal stroke only; no future vertical stroke or final glyph",
                "x2t_reference": "Nonempty placeholder required by native target schema; no gold answer supplied",
                "width": plan["width"], "height": plan["height"], "frames": plan["num_frames"], "fps": plan["fps"],
                "video_encoded": encode_video}
    if encode_video:
        import imageio_ffmpeg
        command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-framerate", str(plan["fps"]),
                   "-i", str(frames / "%03d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                   str(inputs / "observed_strokes.mp4")]
        subprocess.run(command, check=True)
        manifest["encoding_command"] = command
    (inputs / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--encode-video", action="store_true")
    args = parser.parse_args()
    prepare_inputs(args.bundle.resolve(), json.loads((args.bundle / "plan.json").read_text()), args.encode_video)
