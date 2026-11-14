<div align="center"><img src="assets/banner.svg" width="100%"><h1>WebManifest Doctor</h1><p>Catch PWA manifest mistakes before they break installation.</p></div>

## Validation
- App name and start URL.
- Display mode and theme/background colors.
- Icon objects, source paths, sizes, MIME types and purposes.
- Scope/start URL origin and path consistency.
- Shortcut object structure.
- Human-readable and JSON reports.

## Run
```bash
python app.py manifest.webmanifest
python app.py manifest.json --json
```
Python 3.9+, standard library only. This is a structural validator; it does not download icons or guarantee browser-specific installability.

## Tests
```bash
python -m unittest discover -s tests -v
```
MIT License.