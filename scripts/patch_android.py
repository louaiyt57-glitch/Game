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
t = t.replace('</style>', '        <item name="android:windowBackground">@android:color/black</item>\n'
              '        <item name="android:statusBarColor">@android:color/black</item>\n'
              '        <item name="android:navigationBarColor">@android:color/black</item>\n    </style>', 1) if 'windowBackground' not in t else t
st.write_text(t)

# 2b) cutout mode for API 28+ (the unprefixed attr is ignored on older files) + immersive sticky in code
v28 = root / 'res/values-v28'
v28.mkdir(exist_ok=True)
(v28 / 'styles.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
        <item name="android:background">@null</item>
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowBackground">@android:color/black</item>
        <item name="android:statusBarColor">@android:color/black</item>
        <item name="android:navigationBarColor">@android:color/black</item>
        <item name="android:windowLayoutInDisplayCutoutMode">shortEdges</item>
    </style>
</resources>
''')
for j in (root / 'java').rglob('MainActivity.java'):
    pkg = re.search(r'package ([\w.]+);', j.read_text()).group(1)
    j.write_text('''package %s;

import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle b) {
        super.onCreate(b);
        if (android.os.Build.VERSION.SDK_INT >= 28) {
            getWindow().getAttributes().layoutInDisplayCutoutMode =
                WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
        }
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().getDecorView().setBackgroundColor(0xFF0A0B0D);
        immersive();
    }
    @Override
    public void onWindowFocusChanged(boolean f) {
        super.onWindowFocusChanged(f);
        if (f) immersive();
    }
    private void immersive() {
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }
}
''' % pkg)

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
