"""Preparation adapters. This CPU task intentionally contains no real model runner."""
from pathlib import Path
from typing import Protocol
import json

from .contracts import validate_input,save
from .media import encode,decode,validate_media
from .build import render_lines


class ModelAdapter(Protocol):
    def check_capabilities(self,track): ...
    def prepare_input(self,payload,destination): ...
    def run(self,prepared): ...
    def collect_artifacts(self,prepared): ...
    def validate_media(self,prepared): ...


class PreparationAdapter:
    def __init__(self, model):self.model=model
    def check_capabilities(self,track):return self.model['task_support'].get(track,'not_verified')
    def prepare_input(self,payload,destination):
        validate_input(payload)
        if self.check_capabilities(payload['track'])!='verified_supported':raise ValueError('Released interface not verified for this track')
        out=Path(destination);out.mkdir(parents=True,exist_ok=False)
        save(out/'prepared.json',{'model':self.model['id'],'input':payload,'status':'prepared_unexecuted',
                                  'gpu_authorized':False,'download_authorized':False,'training_authorized':False})
        return out
    def run(self,prepared):raise PermissionError('No GPU/model execution authorized in this CPU preparation adapter')
    def collect_artifacts(self,prepared):return [str(p) for p in Path(prepared).iterdir()]
    def validate_media(self,prepared):return {'status':'not_run','reason':'No model output exists'}


class MockAdapter(PreparationAdapter):
    """CPU behavior fixture, never included as a model performance row."""
    def __init__(self,case='correct'):
        super().__init__({'id':'CPU_MOCK','task_support':{'G-ATOMIC':'verified_supported'}});self.case=case
    def run(self,prepared):
        p=Path(prepared)/'mock.mp4'
        if self.case=='corrupt':p.write_bytes(b'not a video')
        else:
            frames=render_lines('swap' if self.case=='swap' else 'flash' if self.case=='static' else 'correct')
            if self.case=='missing_frames':frames=frames[:-1]
            encode(p,frames)
        return p
    def validate_media(self,prepared):
        frames,pts=decode(Path(prepared)/'mock.mp4')
        return validate_media('native_video',frames,pts,33)
