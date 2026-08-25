"""
GCVX_IMS
--------
Desktop wrapper application. Loads the GCVX_IMS web application inside a
native window. If there is no internet connection, or the backend service
cannot be reached, a custom branded screen is shown instead of any raw
browser/webview error. The remote address is never displayed anywhere in
the UI (no address bar, no title text, no error text).
"""

import os
import sys
import socket
import threading
import time
import urllib.request

import webview

webview.settings['ALLOW_DOWNLOADS'] = True

from toolbar import HARDENING_JS, CLEAR_STORAGE_JS, TOOLBAR_JS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
APP_TITLE = "GCVX_IMS"
TARGET_URL = "https://laughing-octo-funicular-76gs.onrender.com/"

CONNECT_TIMEOUT = 6          # seconds to wait for a single reachability check
WATCHDOG_INTERVAL = 5        # seconds between background health checks
STARTUP_GRACE_PERIOD = 5     # seconds before the watchdog starts polling

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
WINDOW_MIN_SIZE = (960, 640)


# ---------------------------------------------------------------------------
# Paths (works both when run as a script and when frozen with PyInstaller)
# ---------------------------------------------------------------------------
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def error_page_uri() -> str:
    path = resource_path("error.html")
    path = path.replace("\\", "/")
    if not path.startswith("/"):
        path = "/" + path
    return "file://" + path


ERROR_PAGE = error_page_uri()


# ---------------------------------------------------------------------------
# Connectivity checks
# ---------------------------------------------------------------------------
def has_internet(timeout: float = 3.0) -> bool:
    """Raw internet reachability check, independent of the app's own server."""
    for host, port in (("8.8.8.8", 53), ("1.1.1.1", 53)):
        try:
            socket.setdefaulttimeout(timeout)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
            return True
        except OSError:
            continue
    return False


def server_reachable(timeout: float = CONNECT_TIMEOUT) -> bool:
    """Checks whether the backend service is reachable, without ever
    surfacing the address to the caller/UI."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(TARGET_URL, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return 200 <= resp.status < 500
        except Exception:
            continue
    return False


def app_available() -> bool:
    return has_internet() and server_reachable()


# ---------------------------------------------------------------------------
# JS <-> Python bridge
# ---------------------------------------------------------------------------
class Api:
    """Exposed to injected page JavaScript as `window.pywebview.api`."""

    def __init__(self, window_ref: dict, state: dict):
        self._window_ref = window_ref
        self._state = state

    def _navigate_async(self, url: str):
        def _target():
            time.sleep(0.05)
            window = self._window_ref["window"]
            if window:
                try:
                    window.load_url(url)
                except Exception:
                    pass
        threading.Thread(target=_target, daemon=True).start()

    def retry(self):
        """Used by the offline screen's own Retry button."""
        if not has_internet():
            return {"ok": False, "reason": "no_internet"}
        if not server_reachable():
            return {"ok": False, "reason": "unavailable"}
        self._navigate_async(TARGET_URL)
        self._state["showing_app"] = True
        return {"ok": True}

    def refresh_app(self):
        """Toolbar 'Refresh': reload the current webpage. If the app can be
        reached, reload it; otherwise fall back to the offline screen."""
        if has_internet() and server_reachable():
            self._navigate_async(TARGET_URL)
            self._state["showing_app"] = True
            return {"ok": True}
        self._navigate_async(ERROR_PAGE)
        self._state["showing_app"] = False
        return {"ok": False}

    def update_app(self):
        """Toolbar 'Update': clear all local cache/cookies/storage for the
        app, then do a fresh, cache-busted reload of the website."""
        window = self._window_ref["window"]

        try:
            window.clear_cookies()
        except Exception:
            pass
        try:
            window.evaluate_js(CLEAR_STORAGE_JS)
        except Exception:
            pass

        if has_internet() and server_reachable():
            cache_bust = str(int(time.time() * 1000))
            sep = "&" if "?" in TARGET_URL else "?"
            fresh_url = f"{TARGET_URL}{sep}_gcvx_cb={cache_bust}"
            self._navigate_async(fresh_url)
            self._state["showing_app"] = True
            return {"ok": True}

        self._navigate_async(ERROR_PAGE)
        self._state["showing_app"] = False
        return {"ok": False}


# ---------------------------------------------------------------------------
# Window Construction
# ---------------------------------------------------------------------------
def app_icon_path() -> str:
    for filename in ("icon.ico", "icon.icns", "images.png"):
        p = resource_path(filename)
        if os.path.exists(p):
            return p
    return ""


APP_ICON = app_icon_path()


def build_window(window_ref: dict, state: dict) -> "webview.Window":
    start_ok = app_available()
    state["showing_app"] = start_ok
    initial_target = TARGET_URL if start_ok else ERROR_PAGE

    api = Api(window_ref, state)

    window = webview.create_window(
        APP_TITLE,
        initial_target,
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=WINDOW_MIN_SIZE,
        text_select=False,
        confirm_close=False,
    )
    window_ref["window"] = window

    def on_loaded():
        # Best-effort hardening: no context menu / view-source, so the
        # underlying address is never exposed via the right-click menu.
        try:
            window.evaluate_js(HARDENING_JS)
        except Exception:
            pass
        # Inject the GCVX_IMS toolbar (Refresh / Update / About) on top of
        # whatever page just finished loading — the real app or the local
        # offline screen.
        try:
            window.evaluate_js(TOOLBAR_JS)
        except Exception:
            pass

    window.events.loaded += on_loaded
    return window


def main():
    window_ref = {"window": None}
    state = {"showing_app": False, "auto_recover": False}

    build_window(window_ref, state)
    webview.start(debug=False, http_server=False, icon=APP_ICON if APP_ICON else None)


if __name__ == "__main__":
    main()
