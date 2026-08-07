# GCVX_IMS

A Windows desktop wrapper for the GCVX_IMS web application, built with
Python + `pywebview`, with a GitHub Actions workflow that builds the
`.exe` on a Windows runner and publishes it to GitHub Releases.

## Features

- Loads the GCVX_IMS web app inside a native desktop window (no browser
  address bar, so the underlying web address is never visible to the user).
- If there is no internet connection, or the service can't be reached, a
  custom branded "You're not connected" screen is shown — never a raw
  webview/browser error dialog.
- A background watchdog keeps checking the connection while the app is
  open. If the connection drops mid-session, it automatically swaps to the
  same custom offline screen.
- A **Retry** button on the offline screen re-checks connectivity and the
  service, reloading the app automatically once both are back.
- Right-click / context menu is disabled and DevTools are off, so the
  address can't be inspected via "View source" or similar.

## Repository structure

```
GCVX_IMS/
├── .github/
│   └── workflows/
│       └── build-release.yml   # CI: builds exe, publishes to Releases
├── main.py                      # App entry point
├── error.html                   # Custom offline/error screen
├── requirements.txt              # Python dependencies
├── build_exe.bat                 # Local (manual) Windows build script
├── icon.ico                       # (optional) add your own app icon here
├── .gitignore
└── README.md
```

> `icon.ico` is optional. If you add one at the repo root, both the local
> build script and the GitHub Actions workflow will automatically pick it
> up and use it as the exe icon. If it's absent, the build just skips it.

## Setting this up on GitHub

1. Create a new repository and push these files to it (keep the folder
   structure exactly as-is, including `.github/workflows/build-release.yml`).
2. No extra secrets/setup needed — the workflow uses the automatically
   provided `GITHUB_TOKEN`, which already has permission to create releases
   in your own repo (the workflow also explicitly requests
   `permissions: contents: write`).

## How the workflow builds and releases the exe

File: `.github/workflows/build-release.yml`

It runs on `windows-latest`, installs dependencies from
`requirements.txt`, and runs PyInstaller to produce `dist/GCVX_IMS.exe`
exactly like `build_exe.bat` does locally.

**It triggers in three ways:**

1. **Push a version tag** — e.g.:
   ```
   git tag v1.0.0
   git push origin v1.0.0
   ```
   This builds the exe and creates/updates a GitHub Release tagged `v1.0.0`
   with the exe attached. If your tag name contains a hyphen (e.g.
   `v1.0.0-beta`, `v1.0.0-rc1`), it's automatically published as a
   **pre-release**; a plain tag like `v1.0.0` is published as a normal
   release.

2. **Manual run** — go to your repo's **Actions** tab → select
   **"Build and Release GCVX_IMS"** → **Run workflow**. You'll be prompted
   for:
   - `version`: the tag to create/use (e.g. `v1.2.0` or `v1.2.0-beta`)
   - `prerelease`: checkbox to mark it as a pre-release
   
   This is handy for cutting a release without needing to push a git tag
   yourself.

3. **Push to `main` / open a pull request** — the workflow still builds the
   exe (as a sanity check that nothing is broken) and uploads it as a
   **workflow artifact** (downloadable from the run's summary page), but it
   does **not** create or touch any Release. Only tag pushes and manual runs
   publish a release.

After a successful tag-push or manual run, check your repo's **Releases**
page — the newest run's release will be there (or updated in place if you
reuse the same tag) with `GCVX_IMS.exe` attached as a downloadable asset.

## Run from source locally (for testing before pushing)

```
pip install -r requirements.txt
python main.py
```

> `pywebview` on Windows uses the Edge WebView2 runtime, preinstalled on
> almost all Windows 10/11 machines.

## Build locally without GitHub (optional)

Double-click `build_exe.bat` on a Windows machine, or run it from a
terminal:
```
build_exe.bat
```
The finished executable will be in `dist\GCVX_IMS.exe`.

## How the "never show the URL" behavior works

- The window has no address bar/toolbar (pywebview windows don't include
  one by default).
- The window title is fixed to `GCVX_IMS`, never the remote page's title.
- The offline/error screen is a fully local file and never mentions the
  remote address.
- Right-click context menu is disabled.
- DevTools are disabled (`debug=False`) in the packaged build.

## Customizing

- Change branding text/colors in `error.html`.
- Adjust window size in `main.py` (`WINDOW_WIDTH`, `WINDOW_HEIGHT`).
- Adjust how often the app checks connectivity via `WATCHDOG_INTERVAL` in
  `main.py`.
