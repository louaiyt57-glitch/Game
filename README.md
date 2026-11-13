# Breaker Run (Android)

Pixel arcade flight game, wrapped as an Android app with Capacitor.

## Get the APK
1. Push this folder to a GitHub repository (branch `main`).
2. Open the **Actions** tab, run **Build Android APK** (it also runs on every push).
3. When it finishes, open the run and download the **breaker-run-apk** artifact (a zip containing `app-debug.apk`).
4. Copy the APK to the phone and install it (allow "install unknown apps" for your file manager or browser).

The APK is a debug build. Publishing to Google Play needs a signed release build and a developer account.

## Edit the game
All game code is in `www/index.html`. The libraries and fonts are local, so the app works offline.

## Credits
- Downtown map buildings: Quaternius "Downtown City MegaKit" (CC0), decimated and vertex-coloured. quaternius.com
- Blocky Land trees: Jean Charpentier "LowPoly Pack" (Beerware) and a Low Poly Spring Trees pack.
- Three.js (MIT) and the Press Start 2P / Silkscreen fonts (OFL) are bundled locally.
