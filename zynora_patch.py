# zynora_patch.py - перебрендинг клиента: имя, пакет, фиолетовая тема, иконка.
# Запускается из корня репозитория внутри сборки на GitHub.
import os, re, sys
from PIL import Image, ImageDraw

APP = "V2rayNG/app"
RES = f"{APP}/src/main/res"

def rd(p):
    return open(p, encoding="utf-8").read()
def wr(p, s):
    open(p, "w", encoding="utf-8").write(s)

# ---- 1. имя и пакет ----
p = f"{APP}/build.gradle.kts"
s = rd(p)
s = s.replace('applicationId = "com.v2ray.ang"', 'applicationId = "com.v2ray.ang.zynora"')
s = s.replace('"v2rayNG_', '"Zynora_')
wr(p, s)
p = f"{RES}/xml/shortcuts.xml"
wr(p, rd(p).replace('targetPackage="com.v2ray.ang"', 'targetPackage="com.v2ray.ang.zynora"'))
for d in os.listdir(RES):
    f = f"{RES}/{d}/strings.xml"
    if d.startswith("values") and os.path.isfile(f):
        wr(f, re.sub(r'(<string name="app_name"[^>]*>)[^<]*', r'\1Zynora', rd(f)))

# ---- 2. фиолетовая тема ----
DARK = {
 "primary": "A855F7", "onPrimary": "1E0A3C", "primaryContainer": "4C1D95", "onPrimaryContainer": "EDE0FF",
 "secondary": "C084FC", "onSecondary": "2A0A55", "secondaryContainer": "3B1A6B", "onSecondaryContainer": "F1E6FF",
 "tertiary": "7DD3FC", "onTertiary": "062A3A", "tertiaryContainer": "0C4A6E", "onTertiaryContainer": "D4F0FF",
 "background": "0B0614", "onBackground": "EDE7F6", "surface": "0B0614", "onSurface": "EDE7F6",
 "surfaceVariant": "2A1B45", "onSurfaceVariant": "CBBDE6", "outline": "8E7BB0", "outlineVariant": "3A2A5C",
 "inverseSurface": "EDE7F6", "inverseOnSurface": "0B0614", "inversePrimary": "6D28D9",
 "surfaceTint": "A855F7",
 "surfaceContainerLowest": "07030E", "surfaceContainerLow": "120A20", "surfaceContainer": "170E28",
 "surfaceContainerHigh": "21153A", "surfaceContainerHighest": "2B1D4A",
}
LIGHT = {
 "primary": "6D28D9", "onPrimary": "FFFFFF", "primaryContainer": "EDE0FF", "onPrimaryContainer": "2A0A55",
 "secondary": "9333EA", "onSecondary": "FFFFFF", "secondaryContainer": "F1E6FF", "onSecondaryContainer": "2A0A55",
 "surfaceTint": "6D28D9",
}
p = f"{APP}/src/main/java/com/v2ray/ang/ui/compose/Theme.kt"
s = rd(p)
def recolor(block, table):
    for k, v in table.items():
        block = re.sub(rf'(\n\s+{k} = Color\()0x[0-9A-Fa-f]{{8}}(\))', rf'\g<1>0xFF{v}\g<2>', block)
    return block
i = s.index("private val LightColor"); j = s.index("private val DarkColor"); k = s.index("// Semantic Colors")
s = s[:i] + recolor(s[i:j], LIGHT) + recolor(s[j:k], DARK) + s[k:]
s = re.sub(r'(val colorFabActive = Color\()0x[0-9A-Fa-f]{8}', r'\g<1>0xFFA855F7', s)
wr(p, s)

# ---- 3. иконка ----
logo = Image.open("zynora_logo.png").convert("RGB")
dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for name, m in dens.items():
    d = f"{RES}/mipmap-{name}"
    os.makedirs(d, exist_ok=True)
    logo.resize((int(108*m), int(108*m)), Image.LANCZOS).save(f"{d}/ic_launcher_foreground.png")
    sq = logo.resize((int(48*m), int(48*m)), Image.LANCZOS)
    sq.save(f"{d}/ic_launcher.png")
    mask = Image.new("L", sq.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, sq.size[0]-1, sq.size[1]-1), fill=255)
    rnd = Image.new("RGBA", sq.size, (0, 0, 0, 0)); rnd.paste(sq, (0, 0), mask); rnd.save(f"{d}/ic_launcher_round.png")
wr(f"{RES}/values/ic_launcher_background.xml", rd(f"{RES}/values/ic_launcher_background.xml").replace("#FFFFFF", "#000000"))
for f in ("ic_launcher.xml", "ic_launcher_round.xml"):
    pth = f"{RES}/mipmap-anydpi-v26/{f}"
    if os.path.isfile(pth):
        wr(pth, '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                '    <background android:drawable="@color/ic_launcher_background" />\n'
                '    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n</adaptive-icon>\n')
print("zynora_patch: ok")
