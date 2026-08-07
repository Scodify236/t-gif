# GCVX_IMS

A Windows desktop wrapper for the GCVX_IMS web application, built with
Python + `pywebview`.

## Features

- Loads the GCVX_IMS web app inside a native desktop window (no browser
  address bar, so the underlying web address is never visible to the user).
- If there is no internet connection, or the service can't be reached, a
  custom branded "You're not connected" screen is shown — never a raw
  webview/browser error dialog.
- A background watchdog keeps checking the connection while the app is
  open. If the connection drops mid-session, it automatically swaps to the
  same custom offline screen instead of leaving a broken/blank window.
- A **Retry** button on the offline screen re-checks connectivity and the
  service, and reloads the app automatically once both are back.
- Right-click / context menu is disabled so the address can't be inspected
  via "View source" or similar.

## Project structure

```
GCVX_IMS/
├── main.py          # App entry point (pywebview window, connectivity checks, watchdog)
├── error.html        # Custom offline/error screen
├── requirements.txt   # Python dependencies
├── build_exe.bat      # Builds a standalone GCVX_IMS.exe with PyInstaller
└── icon.ico            # (optional) put your own .ico here for the exe icon
```

## Run from source (for testing)

1. Install Python 3.9+ on Windows.
2. Open a terminal in this folder and run:
   ```
   pip install -r requirements.txt
   python main.py
   ```

> Note: `pywebview` on Windows uses the Edge WebView2 runtime. It's
> preinstalled on Windows 10/11 in almost all cases. If it's missing, install
> the "WebView2 Runtime" from Microsoft — the user will not see any mention
> of this, it's just a one-time environment requirement for you as the
> developer/tester.

## Build a standalone `GCVX_IMS.exe`

This must be done **on a Windows machine** (PyInstaller builds a Windows
binary only when run on Windows):

1. (Optional) Drop an `icon.ico` file into this folder if you want a custom
   app icon.
2. Double-click `build_exe.bat`, or run it from a terminal:
   ```
   build_exe.bat
   ```
3. The finished executable will be in `dist\GCVX_IMS.exe`. You can copy
   just that single file to distribute the app — no console window, no
   Python installation required on the target machine.

## How the "never show the URL" behavior works

- The window has no address bar/toolbar (pywebview windows don't include
  one by default), so there's nothing showing the address during normal use.
- The window title is fixed to `GCVX_IMS`, never the page title from the
  remote site.
- The offline/error screen is a fully local file and never mentions the
  remote address.
- Right-click context menu is disabled, so "Inspect"/"View page source"
  aren't available as an easy way to find the address.
- DevTools are disabled (`debug=False`) in the packaged build.

## Customizing

- Change branding text/colors in `error.html`.
- Adjust window size in `main.py` (`WINDOW_WIDTH`, `WINDOW_HEIGHT`).
- Adjust how often the app checks connectivity via `WATCHDOG_INTERVAL` in
  `main.py`.
