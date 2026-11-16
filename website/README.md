# Eyedentify website

The static source for the hosted Eyedentify workspace. No package installation or build step is needed.

## Run with PowerShell

With Python 3 installed, run from the repository root:

```powershell
py -m http.server 8000 --bind 127.0.0.1 --directory website
```

Open `http://localhost:8000` in your browser. Keep PowerShell open while using the site; press Ctrl+C to stop the server. If your Python installation uses `python` instead of `py`, substitute that command.

## Files

- `index.html`: page shell and navigation containers.
- `style.css`: responsive layout and visual styling.
- `app.js`: routes, camera preview, text reading and accessibility controls.

The browser camera requires localhost or HTTPS and explicit permission. It is a preview only. Sensor observations and history stay empty without an integrated data source. Text-to-speech uses browser voices. Preferences are saved locally. Google Fonts are requested by the stylesheet; fallback system fonts remain available offline.

## Hosting

Serve this directory as a static website over HTTPS. There is no backend or build command for this frontend. It does not change the Raspberry Pi application in `EyeDentify-GitHub/`.

The live Sites deployment is maintained separately. Pushing to this GitHub repository alone does not republish that deployment. Hosting credentials and Sites project configuration are intentionally excluded from this export.
