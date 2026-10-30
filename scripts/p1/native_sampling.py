"""Observe the unchanged Lance loader's actual reads and transforms."""
import json
from pathlib import Path
import numpy as np


def install_sampling_trace(output):
    from data.datasets_custom.validation_dataset import ValidationDataset
    output = Path(output)
    original_get = ValidationDataset.get_video_tensor_online
    original_read = ValidationDataset._read_decord
    records = []
    active = {}

    def traced_read(video, indices):
        frames = original_read(video, indices)
        active.update(indices=[int(i) for i in indices], reader_fps=float(video.get_avg_fps()),
                      reader_frame_count=len(video), reader_PTS_intervals=np.asarray(video.get_frame_timestamp(indices)).tolist())
        np.savez_compressed(output / (active['trace_id'] + '-read_RGB.npz'), frames=np.stack([np.asarray(f) for f in frames]))
        return frames

    def traced_get(dataset, media_url, vision_stream, worker_id=0, element_dtype='image'):
        active.clear()
        active.update(trace_id=f'sampling-{len(records):03}', media=str(media_url),
                      vision_stream=vision_stream, element_dtype=element_dtype)
        tensor = original_get(dataset, media_url, vision_stream, worker_id, element_dtype)
        np.savez_compressed(output / (active['trace_id'] + '-transformed.npz'), tensor=tensor.detach().cpu().float().numpy())
        active['transformed_shape'] = list(tensor.shape)
        records.append(dict(active))
        (output / 'actual_sampling.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
        return tensor

    ValidationDataset._read_decord = staticmethod(traced_read)
    ValidationDataset.get_video_tensor_online = traced_get
    return records
