import dataclasses
import json
import multiprocessing
import multiprocessing.queues
import queue
from pathlib import Path
from typing import Any

_ctx = multiprocessing.get_context('fork')

try:
    import numpy as np
    _has_numpy = True
except ImportError:
    _has_numpy = False

from sim_ui.simdata import Frame

_svelte_path = Path(__file__).parent / 'dist' / 'index.html'


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if _has_numpy and isinstance(obj, np.ndarray):
            return obj.flatten().tolist()
        return super().default(obj)


def _webview_worker(
    q: multiprocessing.queues.Queue,
    ready: multiprocessing.synchronize.Event,
    title: str,
    width: int,
    height: int,
    svelte_uri: str,
) -> None:
    import webview

    win = webview.create_window(title, svelte_uri, width=width, height=height)
    win.events.loaded += ready.set

    def _pump() -> None:
        while True:
            try:
                item = q.get(timeout=0.05)
            except queue.Empty:
                continue
            for key, value in item.items():
                win.evaluate_js(
                    f'window.onData({json.dumps(key)}, {json.dumps(value, cls=_Encoder)})'
                )

    webview.start(func=_pump)


class SimUI:
    def __init__(self, title: str = 'sim-ui', width: int = 1024, height: int = 768) -> None:
        self._q = _ctx.Queue()
        ready = _ctx.Event()
        self._proc = _ctx.Process(
            target=_webview_worker,
            args=(self._q, ready, title, width, height, _svelte_path.as_uri()),
            daemon=True,
        )
        self._proc.start()
        ready.wait()   # block until the page has loaded

    def send(self, frame: Frame) -> None:
        if not self._proc.is_alive():
            return
        try:
            self._q.put(dataclasses.asdict(frame))
        except Exception:
            pass

    def wait(self) -> None:
        """Block until the viewer window is closed by the user."""
        try:
            self._proc.join()
        except Exception:
            pass
