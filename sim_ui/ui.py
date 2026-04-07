import dataclasses
import json
from pathlib import Path
from typing import Any

import webview

from sim_ui.simdata import Frame

try:
    import numpy as np
    _has_numpy = True
except ImportError:
    _has_numpy = False

svelte_path = Path(__file__).parent / 'dist' / 'index.html'


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if _has_numpy and isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


class SimUI:
    def __init__(self) -> None:
        self._window: webview.Window | None = None
        self._queue: dict[str, Any] = {}

    def send(self, frame: Frame) -> None:
        data = dataclasses.asdict(frame)
        self._queue.update(data)
        if self._window:
            for key, value in data.items():
                self._push(key, value)

    def show(self, title: str = 'sim-ui', width: int = 1024, height: int = 768) -> None:
        self._window = webview.create_window(title, svelte_path.as_uri(), width=width, height=height)
        self._window.events.loaded += self._flush
        webview.start()

    def _push(self, key: str, value: Any) -> None:
        self._window.evaluate_js(f'window.onData({json.dumps(key)}, {json.dumps(value, cls=_Encoder)})')

    def _flush(self) -> None:
        for key, value in self._queue.items():
            self._push(key, value)
