#!/usr/bin/env python3
"""Run after `npx cap add android`: force landscape, go fullscreen, install the pixel icon."""
import re, shutil, pathlib

root = pathlib.Path('android/app/src/main')

# 1) landscape-only activity
mf = root / 'AndroidManifest.xml'
t = mf.read_text()
if 'screenOrientation' not in t:
    t = t.replace('<activity', '<activity android:screenOrientation="sensorLandscape"', 1)
mf.write_text(t)

# 2) fullscreen theme, draw into the display cutout
st = root / 'res/values/styles.xml'
t = st.read_text()
if 'windowFullscreen' not in t:
    t = re.sub(r'(<style name="AppTheme\.NoActionBar"[^>]*>)',
               r'\1\n        <item name="android:windowFullscreen">true</item>\n'
               r'        <item name="android:windowLayoutInDisplayCutoutMode">shortEdges</item>', t, count=1)
st.write_text(t)

# 3) icon: pixel rocket on near-black
for d in pathlib.Path('icons').iterdir():
    dest = root / 'res' / d.name
    dest.mkdir(parents=True, exist_ok=True)
    for f in d.iterdir():
        shutil.copy(f, dest / f.name)
bg = root / 'res/values/ic_launcher_background.xml'
if bg.exists():
    bg.write_text(re.sub(r'#[0-9A-Fa-f]{6,8}', '#0A0B0D', bg.read_text()))
print('android patched')
