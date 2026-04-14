import json
import multiprocessing
import multiprocessing.queues
import queue
from pathlib import Path

from sim_ui.simdata import Frame

_ctx = multiprocessing.get_context('fork')

_svelte_path = Path(__file__).parent / 'dist' / 'index.html'


def _webview_worker(
    q: multiprocessing.queues.Queue,
    ready: multiprocessing.synchronize.Event,
    title: str,
    width: int,
    height: int,
    svelte_uri: str,
) -> None:
    import threading
    import webview

    stop = threading.Event()
    win = webview.create_window(title, svelte_uri, width=width, height=height)
    win.events.loaded += ready.set
    win.events.closed += stop.set

    def _pump() -> None:
        while not stop.is_set():
            try:
                wire = q.get(timeout=0.05)
            except queue.Empty:
                continue
            win.evaluate_js(f'window.onFrame({json.dumps(wire)})')

    webview.start(func=_pump, debug=False)


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
        ready.wait()

    def send(self, frame: Frame) -> None:
        if not self._proc.is_alive():
            return
        try:
            self._q.put(frame.to_wire())
        except Exception:
            pass

    def wait(self) -> None:
        """Block until the viewer window is closed by the user."""
        try:
            self._proc.join()
        except Exception:
            pass
