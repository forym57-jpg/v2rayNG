# plamix_patch_v9.py - новый главный экран (чёрный фон, фиолетовое свечение, кнопка с кольцом). Перебрендинг клиента (PlamixVless): имя, пакет, фиолетовая тема, иконка.
# Запускается из корня репозитория внутри сборки на GitHub.
import os, re, sys, io, base64
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
s = re.sub(r'applicationId = "com\.v2ray\.ang[^"]*"', 'applicationId = "com.v2ray.ang.plamix"', s, count=1)
s = s.replace('"v2rayNG_', '"Plamix_').replace('"Zynora_', '"Plamix_')
wr(p, s)
p = f"{RES}/xml/shortcuts.xml"
wr(p, re.sub(r'targetPackage="com\.v2ray\.ang[^"]*"', 'targetPackage="com.v2ray.ang.plamix"', rd(p)))
for d in os.listdir(RES):
    f = f"{RES}/{d}/strings.xml"
    if d.startswith("values") and os.path.isfile(f):
        wr(f, re.sub(r'(<string name="app_name"[^>]*>)[^<]*', r'\1PlamixVless', rd(f)))

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
LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwQDAwQEBAQFBQQFBwsHBwYGBw4KCggLEA4RERAOEA8SFBoWEhMYEw8QFh8XGBsbHR0dERYgIh8cIhocHRz/2wBDAQUFBQcGBw0HBw0cEhASHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBz/wAARCAFAAUADASIAAhEBAxEB/8QAHQABAAIDAQEBAQAAAAAAAAAAAAECBAUGAwcICf/EAEcQAAIBAwEGAgYFCAUNAAAAAAABAgMEEQUGEiExQWETUQcicZGh0RQyUrHhIzVCcnOBssEVJEWS8BYXMzREVGJjgpOjwtL/xAAbAQEAAgMBAQAAAAAAAAAAAAAAAQIDBAUGB//EADkRAAIBAwEFBgMHAQkAAAAAAAABAgMEEQUSITFBYRNRcaGx0YGR4QYUIjI0QvAVFiMkM0NSU8Hx/9oADAMBAAIRAxEAPwD+f4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwMAEAnAwMAgFgTgFQWAwCoLYIwMAgE4GCAQCcDABAJwMAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvCST9aOV1XIyKlo1R8ek/EoLg5LnB+Ul0+5mKjItLurZVlVoyxLk01lSXVNdV2M1Jw4VOHmvfw80Xhs8JHhgnBv4abba5TlUsHGheJZnayfqy7wf8jTVqFS3qyp1YShUi8OMlhoz17OpRip8Yvg1wfs+j3l50ZQSlxT5ngC2CMGrgxkAYAAAAABOBgYIIBOCcDAKgtgjAwCCMFsEEYGCMEFiGiMEEAAgAAAAAAAAAAAAAAAAAAAAAAAAAlEEoIEkogsi6JL0qs6FSNSnKUKkXmMovDTOvtNSs9pKULTUoxheJYp1o8N72Po+3JnH7kt3eSe7nGehGWjo2V/UtG1jahLjF8H9e5mxRrypbsZT4rvNzq2z1zpjc1+Vt+lSK5e1dDTuJ1ehbUYUbW+l6vKNaXTtL5mxvdmrC6bqU06LfHNN8H+7l7jry0ijew7fT5bucXxX86/M23Zwrx27d/B8jgsEYOqnsnTjyu5Z7wXzPN7LR/3t5/Z/iaEtDvFxh5r3MDsay5eaOZwTg6VbKJv/AFv/AMf4ntHY6Mnj6cv+3y+JC0O9fCHmvcKxrv8Ab5o5TAwdlDYZT/tCOPPwvxMuh6O1V56nFJ9fB/EyL7P37/0/Ne5dadcP9vmvc4PdG6fRf82PlqsM96L/APo8p+jXd5arTb/Yv5lv7PX/APx+a9yf6bc/7fNe5wGCMHZ1tga1P6moW8mvOMka+vshqFGLlHwavaE8P44Mc9EvYfmpP4b/AEyUlY148Ys5zBGDYXOlXlmt6vbVYR83Hh7zEcHg51ShOm9maw+prSg4vElg8GiD0aKswOJRoo0QXZVoxtEEAAggAAAAAAAAAAAAAAAAAAAAAEoglEoEkohcyxdEmRa3FS1qqcN19HCSzGS8muqO3Wwa2l0eGq7NxlOrxVewbzKElzUH180n069Dg4n2L0B3k1rWqWGfydW3Vfi+UoySz7pHb0iFKvV+611mMuD5p969GuD+Bv2ShUn2NRbn5PofHqlKdGpOnOMoTg3GUZLDTXNNG50baGpYbtCs3Utei6w9nbsfpX0i+inTdsrV3dooWetwjwr49Wv2qLr+tzXc/L2s6LfaBqFWx1G3nQuqT4xl1XRp8mn5otcWl1pFbtKb3cnyfR+3yJq0KtnPai93f7ncxq07ilGrTmpwksqSfA8ZZ4nFadqtbTqnqPept+tTfJ/JnW217SvqPiUHldU+cfaeis9Vp3sccJrivY36N1Gsu5nqqmHg9YVcYTfAxnHHEr6y88GwpyizKptG2p3Ki+fAy6V+sczn99pY4+0jx5Llkzxu3Eyqu0dP/S0sYUkuGDxnqTw8M5915Iq68u5Z3zJdyzcSv23jPxEbpN5zxNI6kufERrPPMxffpZKfeGdFC5TXPh5GBe6FY6g3KVNQqP8ATpcPeuTMalWxjDNhQr9zZ7Slcx2K0U11Mm1GqtmaycVqugXGm5m8VKH249Pauhp5RPrCiqkWsJ54NPkzi9pNA+g/1q3hi2m8OK/QfyZ5jV9B7GDuLffHmu76ehzLzT+zXaU+By7RVnq4lGjyckchooyCzKmNlQACAAAAAAAAAAAAAAAAAAACyKkolAsiVzKosi6LF48z6n6Cqro7XXOMZlZzXH9eB8tifQPRLcO32jrzj9Z2skv70Tt6Gs31JdTesFm4h4n6br6mqcMJxwl59D57tppWnbU2f0e9gnODfg1ocJ0n2fl25MzLvUd2jhyzLHFnMX+pc8vpzPpdShTnFwqLKfI9XOnGScZrKPimv7PXegXTp10p0pP8nWh9Wa/k+xrbW7q2dVVaMt2S9zXkz63e1KN7b1Le4pxqUp8HGR8513Z6ppc3Vot1bR8pdYdn8z59q+izspdvatuC+cfp1+feeZvLF0H2lF7vNGZ9Khrduo0pujdwWd1SaT/D7jQ1a9zSnKE6tVSjwacmY8JypyUotxkuKa5o2Xj09Vgo1XGF4liM+UanZ+TOZO6d2vxPFTyl9fU1JVXVW/dL1+pgO4rPnVqf3mVdWp9uXvZFSEqc5QnFxlF4afNFGc6U5cGzXbZZ1Jfal7wqkvtS95QFNpkZZ7QuK0MbtWax5SZlUdXuqT4z8ReU1n4mvLIy07irDfGTRaNSUeDOr0/U6V4t1epVSy4v+RvLWWcI+eUqkqU41IPEovKZ9B05qvClVS4VIqWPaew0O8lc5jPivM7FjWdTc+KN5bwbxx4Iy6un07u3nSqQUqVSO7Jdi9ha7+ElxOkttMc4rhh8uZ7mjSTjifBnoqdNOOJH581CznY3de3qfWpTcX37mGztfSTZKz2kkoxwqlGnP2vGH9xxcj5LqVsre5qUo8E2jxt1SVKrKC5M82irLMqzls1WQACpAAAAAAAAAAAAAAAAAAAJRBKAJLIqWMiLIvE7X0bVPC1uvJc3byWf+qJxUTrtgZ7mrV5Ppby/iidvQni/peJvaf8AqIeJ9OvLxvKzjoc/e3O/nDz55Pe6uM5zx8jR3Nd8eJ9Guq2yj0tepjcUqV2nzKKtvcJYa8n1MOdXGcHnGrxOHK5eTnOrvNVq2g/Xr2cfV5ypLmu6+RzvXsd/TqcTX6noML5Orb7sLjm1yU/kzz+oaOqmatst/Ne3sc+4s9r8dL5exzfjq5jGFZ+vFYjVfl5S7d+hjzg4ScZLDQqU50ZyhOLjOLw01holTzHdlxXR+R52UnLdPj/OJzm88eJ5tDBZxaGGYtkrgqkSTunrSozqzUKcJTk+UYrLLRg28IlLJSMXJpJNt8El1Pp2k2bo29Ck1xhCMX7jQ6Bs5KjUp3Vyl4i4xp/Zfm+59B0qy3pJuLxzZ9B+zOk1KKdaqsOXLoeh0uzlHM58zcaNZyk01HGGuLO1sNOi4RjKOGupgaRZKD3muL6+RudS1e10DSrnULpqNG2pubWfrtcku7eEeuqTUI55I7kpKKPz16XriNXbS7ox5WtOnRePNRy/jI+fyNhq2o1tV1C6vbh5r3NSVWb7t5NdI+Q6hX7evOr3ts8VcVO0qSn3s82VZZlWcyRrMgAFSAAAAAAAAAAAAAAAAAAASiCUASWRUlci6JPRczptifzpWeeVCX3o5hHSbG/nKt+xf3o7OiP/AB1LxN2xf9/DxOyuKu9nzwaW5ljPHJsrmWE/NmmuG2z3F9NnbuJGLKWQk2em5hNvglxefIwK+s21u2qadV9uC95watSnSW1Vlg0JSjDfJ4NpTTZmUXjgct/lJWT9W3pJd2zJo7VJNeLbcOrhL5lqGrWaeHPyYhd0U+JvtR0Whq9P1vydeK9Wol8H5o4e+sLjTq7o3FNxmuK8pLzT6o7fT9atL2SVOruz+xPg/wATZXdlb6vbfR7iOVn1Zr60X5pmze6Vb6pDtraS2+9cH49evzM1a1p3Udum/wAXqfOLC4o0qmLijGrRfPK4rujqKWjafXpxqQoxlCfFOMnj7zRa1oNxotdRqevRm/ydWK4S+T7DRtXnplZKSc7eT9aGeXddzz9lUjaVnbX1NYXelle6/wDUc+i1Sn2VeP0OlpaDZr/ZoN98s21np8KKSpU4wX/CkjJsZUbyjCtRkp0p8U0bajapLL5Hv7TTqMUp04rxSR6Ghaw/NFI87Gyzh44nV6dbqCWY8zVW9OMOL4Y+JlXWs2+nW861xVhSpQz60n/jL9h2FFU45e5I6CioROxo3FO3pSblGOIuWW8JLrk+GeknbtbS3MbKzk/6NtpZ3uXjT5b3sXT3mBtXt7c62qlpbSnSsJP1ukqvt8l295xkpZPB69r0aydtbP8ADzff0XT18OPndR1FVM0qXDm+/wCglLJ5SZLZRs8XOWTiNlWVZZlTAyjAAIIAAAAAAAAAAAAAAAAAABJAQBYlEEouiS6Ok2NytSrefgv70c2jp9i1nUbjtQf8SOzoizfUvE3LH/PgdLd8EzV1EknKbxGPFt9Dc3NPPE5DaW93cWdN80pVMfBfz9x7LVqsbanKrL4dWdi7kqacmarU9TleTcKeY0FyX2u7NcWwD5zWqzrTc6jy2eenNze1IrjIwe8KtKHOgp+2bX3GXS1KhS/s21feTk/vZMKUH+aaXwfsIwi+MvUwIRlJ4im35LidTouoarb7tOVtVr0V9tYcV2bMWhtNGk1/UaUf2ct3+RsKG1lo2vFt60O6akd7TY2lCanG6cX0TXrlG/bKlCWVVw/A6pOjd0JULimqlKosShL/ABzOJ2g2XraS3cUd6rZSfCfWHaXzN/ba9pldrFyqcvKonH8DfULqFSnhONWlJYeGpRaPXXFpZ6vS2dtOS4STTa8enQ69SlRvIYbWVwaPnOh63X0W43oetRk/Xpt8+68mfSrXV7W5tFdU68FQfOU3jdfk+5xu0WyngRleadByoc50VxdPuvNfFHIuTSxnhzPP0NSvNCk7avHajy37vFPu6ejyaFO6r6e3Smsrl9D6Lqm3lvbZp2UHXmv03wh82cNqWrXeq1vFuq0qjX1Y8ox9i6GC3kjJyNR1u7v3irL8Pcty+vxyadzfVrjdN7u7kWyGyuRk5O0aeSGyrJZUxtkEMglkGNlQAAAAAAAAAAAAAAAAAAAAASQACxKIBZEoujqNieOpXH7F/wASOXR1GxH5yuF/yX/Ejt6D+vpeJu2H6iHidXfVIW9GpWqf6OnFyZ8xuK07itUqz+vNuTO12zvFRs6VtF4nWlmX6q/HHuOFbOl9qbrbuFQi90ePi/obOq1c1OzXIgAg8o2cokEZJAAAJBZM9ra8r2c1O3rTpyXWLweCBeE5Qe1F4ZaLaeUdxom2SlKFK+xCfJVo8Iv2roTtFszTvIyvtNivEfrTox5T7x79uvQ4dM3Oj7Q3GlSUcupb9abfL2eR6W31mndUvuuprajylzj16/zOTpU72NWHZXO9d/NGnaabTWGirO31DTbTaWhK+0+UVefpw5b/AGflLv1OKq0p0akqdSLhOLxKMlhpnI1DTp2ck87UJflkuDXv3o07i3lRfenwfeUBGSDm5NclsgENlWyGQACpAAAAAAAAAAAAAAAAAAAAAAAABZAhElkSWTOq2Gipahct8lR/9kcojqtiqkaFbUa8vq0qG837Hn+R2dAaWoUm+Cb9Gblh+ojn+bjC2rvPpWs1o5zGglSj+7n8WzR5L1akq1SdSTzKbcn7XxPNmjeXDuK86z/c2zBWqOpNzfMgAGqYgACMjIyTkgE5BYnJQnJOSS2RkrknJOQZNnfV7CvGtb1HCouq6rya6o6OdWz2rppTlC21aKxFv6tXtn/DXc5LIUmnlczetdQnRi6M1tU3xi/Vdz6rzM9Ku4LYe+L5fzgz1ubera1p0a1OUKkHhxl0PE3cNUparRjbapJqpBYpXaWZQ7S84/FGru7OrZVfDqxXFb0ZReYzXRp9UYbihCK7Si8wfzXR+/B8uaValNJbUHlenj/N5j5IJZBpGAAAAAAAAAAAAAAAAAAAAAAAAAAAAEogkAk2+m13b6Pq7TxKrGlS98m38EagyVV3bF0lznVUn+5fibdrV7Kbn0kvmmv+zLSnsvPR+awY7ZABr5MYAIZBAbIAKgkZIABbIKgnILAgjIyMlgRkjIyMk5MqleNUfo9VeJb5yovnB+cX0+5mIC0akoPMS0ZOO9F6iUZPdlvR6PkUAKveVAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAALZ4FQATkZIABJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//Z"
src = next((f for f in ("plamixfoto.png", "zynora_logo.png") if os.path.isfile(f)), None)
logo = Image.open(src).convert("RGB") if src else Image.open(io.BytesIO(base64.b64decode(LOGO_B64))).convert("RGB")
print("logo:", src or "встроенный")
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


# ---- 3b. буква P из логотипа для заголовка (прозрачный фон) ----
from PIL import ImageChops
r_, g_, b_ = logo.convert("RGB").split()
lum = ImageChops.lighter(ImageChops.lighter(r_, g_), b_)
alpha = lum.point(lambda v: max(0, min(255, (v - 14) * 5)))
box = lum.point(lambda v: 255 if v > 40 else 0).getbbox()
box = (max(box[0] - 20, 0), max(box[1] - 20, 0), min(box[2] + 20, lum.size[0]), min(box[3] + 20, lum.size[1]))
# родные цвета логотипа: снимаем чёрный фон (обратное премножение на альфу)
_c = logo.convert("RGB").crop(box)
pimg = Image.new("RGBA", _c.size, (0, 0, 0, 0))
_cl = _c.load(); _ol = pimg.load()
for _y in range(_c.size[1]):
    for _x in range(_c.size[0]):
        _r, _g, _b = _cl[_x, _y]
        _a = max(0, min(255, (max(_r, _g, _b) - 14) * 5))
        if _a > 0:
            _k = 255.0 / _a
            _ol[_x, _y] = (min(255, int(_r * _k)), min(255, int(_g * _k)), min(255, int(_b * _k)), _a)
h = 256
pimg = pimg.resize((max(1, int(pimg.size[0] * h / pimg.size[1])), h), Image.LANCZOS)
os.makedirs(f"{RES}/drawable-nodpi", exist_ok=True)
pimg.save(f"{RES}/drawable-nodpi/plamix_p.png")
print("P glyph:", pimg.size)

# ---- 4. тема: без динамических цветов, по умолчанию тёмная ----
TH = f"{APP}/src/main/java/com/v2ray/ang/ui/compose/Theme.kt"
s = rd(TH)
s = s.replace("decodeSettingsBool(AppConfig.PREF_DYNAMIC_COLOR, true)", "decodeSettingsBool(AppConfig.PREF_DYNAMIC_COLOR, false)")
s = s.replace('decodeSettingsString(AppConfig.PREF_UI_MODE_NIGHT, "0") ?: "0"', 'decodeSettingsString(AppConfig.PREF_UI_MODE_NIGHT, "2") ?: "2"')
wr(TH, s)

# ---- 5. логотип в меню не красим в белый ----
DR = f"{APP}/src/main/java/com/v2ray/ang/ui/main/MainDrawer.kt"
s = rd(DR)
s = s.replace("ColorFilter.tint(Color.White, BlendMode.SrcIn)", "null")
wr(DR, s)

# ---- 6. новый главный экран ----
API_BASE = "https://s.arimakicho.space"
KT = r"""package com.v2ray.ang.ui.main

import android.content.Context
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Intent
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.Uri
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.widget.Toast
import androidx.activity.compose.BackHandler
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.v2ray.ang.R
import com.v2ray.ang.dto.entities.ServersCache
import com.v2ray.ang.extension.toTrafficString
import com.v2ray.ang.handler.MmkvManager
import com.v2ray.ang.handler.PlamixOffNotice
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

// Адрес сервера ключей и пробника подставляет скрипт сборки (plamix_patch). Пусто = ещё не подключено.
private const val PLAMIX_API = "__PLAMIX_API__"
private const val PLAMIX_BOT_URL = "https://t.me/Zynoravlessrobot_bot"
private const val PLAMIX_VERSION = "1.1.0"

private val PxPurple = Color(0xFFA855F7)
private val PxPurpleDeep = Color(0xFF7C3AED)
private val PxBg = Color(0xFF000000)
private val PxCard = Color(0xFF170E28)
private val PxCardHi = Color(0xFF21153A)
private val PxWhite = Color(0xFFFFFFFF)
private val PxWhiteDim = Color(0xB3FFFFFF)
private val PxGreen = Color(0xFF22C55E)

private val PlamixEmptyServers: StateFlow<List<ServersCache>> = MutableStateFlow(emptyList())

private enum class PxScreen { HOME, SERVERS, INFO, PLAN, KEY }

private fun plamixCleanName(remarks: String): String =
    remarks
        .replace(Regex("\\s*\\|?\\s*\\[(WIFI|LTE)\\]", RegexOption.IGNORE_CASE), "")
        .replace(Regex("\\s*#\\d+"), "")
        .replace(Regex("[\\x{1F1E6}-\\x{1F1FF}]"), "")
        .trim()

private fun plamixFlag(name: String): String {
    val n = name.lowercase()
    return when {
        n.contains("нидерланд") || n.contains("netherland") || n.contains("holland") -> "🇳🇱"
        n.contains("герман") || n.contains("german") -> "🇩🇪"
        n.contains("финлянд") || n.contains("finland") -> "🇫🇮"
        n.contains("росси") || n.contains("russia") -> "🇷🇺"
        n.contains("авто") || n.contains("auto") -> "⚡"
        else -> "🌐"
    }
}

/** Перед входом по ключу убираем старые подписки, чтобы в приложении была только своя. */
private fun plamixClearSubs() {
    try {
        MmkvManager.decodeSubscriptions().forEach { MmkvManager.removeSubscription(it.guid) }
    } catch (e: Exception) {
    }
}

private fun plamixAuto(list: List<ServersCache>): ServersCache? =
    list.firstOrNull {
        val n = plamixCleanName(it.profile.remarks)
        n.contains("авто", true) || n.contains("auto", true)
    } ?: list.firstOrNull()

private fun plamixIsAuto(s: ServersCache): Boolean {
    val n = plamixCleanName(s.profile.remarks)
    return n.contains("авто", true) || n.contains("auto", true)
}

private fun plamixPrefs(ctx: Context) = ctx.getSharedPreferences("plamix_ui", Context.MODE_PRIVATE)

/** Простой запрос. Возвращает код ответа и текст. */
private fun plamixHttp(url: String, post: String?): Pair<Int, String> {
    val c = URL(url).openConnection() as HttpURLConnection
    try {
        c.connectTimeout = 15000
        c.readTimeout = 20000
        c.setRequestProperty("User-Agent", "PlamixVless/$PLAMIX_VERSION")
        if (post != null) {
            c.requestMethod = "POST"
            c.doOutput = true
            c.setRequestProperty("Content-Type", "application/x-www-form-urlencoded")
            c.outputStream.use { it.write(post.toByteArray()) }
        }
        val code = c.responseCode
        val stream = if (code in 200..399) c.inputStream else c.errorStream
        val text = stream?.bufferedReader()?.use { it.readText() } ?: ""
        return Pair(code, text.take(4000))
    } finally {
        c.disconnect()
    }
}

@Composable
fun PlamixHome(
    mainViewModel: MainViewModel,
    uiState: MainUiState,
    onAction: (MainAction) -> Unit,
    onNavigate: (MainDestination) -> Unit,
) {
    val ctx = LocalContext.current
    val scope = rememberCoroutineScope()
    var lang by remember { mutableStateOf(plamixPrefs(ctx).getString("lang", "ru") ?: "ru") }
    var savedKey by remember { mutableStateOf(plamixPrefs(ctx).getString("key", "") ?: "") }
    var screen by remember { mutableStateOf(PxScreen.HOME) }
    var confirmDelete by remember { mutableStateOf(false) }
    var autoPending by remember { mutableStateOf(false) }
    var connecting by remember { mutableStateOf(false) }
    var forever by remember { mutableStateOf(plamixPrefs(ctx).getBoolean("forever", true)) }

    val en = lang == "en"
    fun t(ru: String, eng: String): String = if (en) eng else ru
    fun setLang(l: String) {
        lang = l
        plamixPrefs(ctx).edit().putString("lang", l).apply()
    }
    fun toast(msg: String) {
        Toast.makeText(ctx, msg, Toast.LENGTH_LONG).show()
    }

    val groups = uiState.groups
    val group = groups.firstOrNull { it.id == uiState.selectedGroupId } ?: groups.firstOrNull()
    val serversFlow: StateFlow<List<ServersCache>> =
        if (group != null) mainViewModel.serversForGroup(group.id) else PlamixEmptyServers
    val servers by serversFlow.collectAsStateWithLifecycle()
    val visible = servers.filter {
        val r = it.profile.remarks
        val host = it.profile.server ?: ""
        host != "0.0.0.0" && host != "127.0.0.1" &&
            !r.contains("ДЛЯ WI-FI", ignoreCase = true) &&
            !r.contains("ДЛЯ МОБИЛЬНОГО", ignoreCase = true) &&
            !r.contains("↓")
    }

    val problemNote: String? =
        if (servers.isNotEmpty() && visible.isEmpty())
            servers.joinToString("; ") { plamixCleanName(it.profile.remarks) }.take(140)
        else null

    // Какая сеть сейчас у устройства: Wi-Fi или мобильный интернет.
    var net by remember { mutableStateOf("wifi") }
    DisposableEffect(Unit) {
        val cm = ctx.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val handler = Handler(Looper.getMainLooper())
        val calc = Runnable {
            var wifi = false
            var cell = false
            try {
                for (n in cm.allNetworks) {
                    val c = cm.getNetworkCapabilities(n)
                    if (c != null && c.hasCapability(NetworkCapabilities.NET_CAPABILITY_NOT_VPN)) {
                        if (c.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) wifi = true
                        if (c.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)) cell = true
                    }
                }
            } catch (e: Exception) {
            }
            val result = if (wifi) "wifi" else if (cell) "mobile" else ""
            if (result.isNotEmpty()) net = result
        }
        val cb = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                handler.post(calc)
            }

            override fun onLost(network: Network) {
                handler.post(calc)
            }

            override fun onCapabilitiesChanged(network: Network, caps: NetworkCapabilities) {
                handler.post(calc)
            }
        }
        try {
            cm.registerNetworkCallback(
                NetworkRequest.Builder().addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET).build(), cb
            )
        } catch (e: Exception) {
        }
        handler.post(calc)
        onDispose {
            try {
                cm.unregisterNetworkCallback(cb)
            } catch (e: Exception) {
            }
        }
    }
    val wifiList = visible.filter { it.profile.remarks.contains("WIFI", ignoreCase = true) }
    val lteList = visible.filter { it.profile.remarks.contains("LTE", ignoreCase = true) }
    val otherList = visible.filter { s -> s !in wifiList && s !in lteList }
    val shown = if (forever) ((if (net == "wifi") wifiList else lteList) + otherList).ifEmpty { visible } else visible
    val selected = visible.firstOrNull { it.guid == uiState.selectedGuid }
    val isRunning = uiState.isRunning

    // Сеть сменилась или сервер не из текущего списка: берём «Авто» для этой сети.
    LaunchedEffect(net, visible.size, uiState.selectedGuid, forever) {
        if (shown.isNotEmpty() && shown.none { it.guid == uiState.selectedGuid }) {
            val auto = shown.firstOrNull {
                val n = plamixCleanName(it.profile.remarks)
                n.contains("авто", true) || n.contains("auto", true)
            } ?: shown.first()
            onAction(MainAction.SelectServer(auto.guid))
            if (isRunning) onAction(MainAction.RestartService)
        }
    }

    // Уведомление «Отключено / Подключить», когда VPN выключен.
    LaunchedEffect(isRunning, visible.isNotEmpty()) {
        if (isRunning || visible.isEmpty()) PlamixOffNotice.hide(ctx) else PlamixOffNotice.show(ctx)
    }

    // Кнопка: «подключаемся» гаснет, когда VPN поднялся, или через 20 с, если не вышло.
    LaunchedEffect(isRunning) { connecting = false }
    LaunchedEffect(connecting) {
        if (connecting) {
            delay(20000)
            connecting = false
        }
    }

    // Выбор сервера вручную выключает режим «Раз и навсегда».
    fun pickServer(srv: ServersCache?) {
        if (srv == null) return
        forever = false
        plamixPrefs(ctx).edit().putBoolean("forever", false).apply()
        onAction(MainAction.SelectServer(srv.guid))
        if (isRunning) onAction(MainAction.RestartService)
    }
    // «Раз и навсегда»: сам берёт Авто для текущей сети (Wi-Fi или мобильный/обход) и переключается при смене сети.
    fun pickForever() {
        forever = true
        plamixPrefs(ctx).edit().putBoolean("forever", true).apply()
        val target = plamixAuto(if (net == "wifi") wifiList else lteList)
        if (target != null) {
            onAction(MainAction.SelectServer(target.guid))
            if (isRunning) onAction(MainAction.RestartService)
        }
    }
    val autoWifi = wifiList.firstOrNull { plamixIsAuto(it) }
    val autoLte = lteList.firstOrNull { plamixIsAuto(it) }
    val wifiCountries = wifiList.filter { !plamixIsAuto(it) }
    val lteCountries = lteList.filter { !plamixIsAuto(it) }

    // Автовыбор: ждём окончания проверки пинга и берём самый быстрый сервер.
    LaunchedEffect(uiState.isTesting, autoPending) {
        if (autoPending && !uiState.isTesting) {
            val best = shown.filter { it.testDelayMillis > 0L }.minByOrNull { it.testDelayMillis }
            if (best != null) onAction(MainAction.SelectServer(best.guid))
            autoPending = false
        }
    }

    // Тариф из заголовков подписки.
    val info = group?.usageInfo
    var planTitle = t("Тариф", "Plan")
    var planLine = t("Подписка не загружена", "Subscription not loaded")
    var leftFraction = 0f
    if (info != null) {
        val parts = ArrayList<String>()
        if (!info.title.isNullOrBlank()) planTitle = info.title!!
        if (info.total > 0L) {
            val used = info.upload + info.download
            parts.add(t("Осталось ", "Left ") + (info.total - used).coerceAtLeast(0L).toTrafficString())
            leftFraction = (1f - used.toFloat() / info.total.toFloat()).coerceIn(0f, 1f)
        } else {
            parts.add(t("Трафик без лимита", "Unlimited traffic"))
            leftFraction = 1f
        }
        if (info.expire > 0L) {
            val days = ((info.expire * 1000L - System.currentTimeMillis()) / 86400000L).coerceAtLeast(0L)
            parts.add(t("на $days дн.", "for $days d."))
        }
        planLine = parts.joinToString(" ")
    }

    // Применить ключ: проверить на сервере и подключить подписку.
    fun applyKey(raw: String, onDone: (Boolean) -> Unit) {
        val key = raw.trim()
        if (key.length < 16) {
            toast(t("Вставьте ключ целиком: кнопка «Вставить» берёт его из буфера.", "Paste the whole key: the Paste button takes it from the clipboard."))
            onDone(false)
            return
        }
        if (PLAMIX_API.isEmpty() || PLAMIX_API.startsWith("__")) {
            toast(t("Проверка ключей скоро заработает. Пока вставьте ссылку подписки из бота.", "Key check is coming soon. For now paste the subscription link from the bot."))
            onDone(false)
            return
        }
        scope.launch {
            val url = "$PLAMIX_API/k/" + Uri.encode(key)
            val r = try {
                withContext(Dispatchers.IO) { plamixHttp(url, null) }
            } catch (e: Exception) {
                Pair(-1, "")
            }
            if (r.first in 200..299) {
                plamixPrefs(ctx).edit().putString("key", key).apply()
                savedKey = key
                plamixClearSubs()
                onAction(MainAction.ImportBatchConfig(url))
                onDone(true)
            } else {
                toast(
                    if (r.first == 404) t("Ключ не найден. Проверьте символы.", "Key not found. Check the characters.")
                    else if (r.first == 410 || r.first == 403) t("Срок ключа закончился. Продлите тариф в боте.", "The key has expired. Renew in the bot.")
                    else t("Нет связи с сервером (код ${r.first}). Попробуйте ещё раз.", "No connection to the server (code ${r.first}). Try again.")
                )
                onDone(false)
            }
        }
    }

    // Пробный период: запрос из самого приложения, один раз на устройство.
    fun startTrial(onDone: (Boolean) -> Unit) {
        if (PLAMIX_API.isEmpty() || PLAMIX_API.startsWith("__")) {
            toast(t("Пробный период скоро будет доступен.", "The trial will be available soon."))
            onDone(false)
            return
        }
        scope.launch {
            val dev = try {
                Settings.Secure.getString(ctx.contentResolver, Settings.Secure.ANDROID_ID) ?: ""
            } catch (e: Exception) {
                ""
            }
            val r = try {
                withContext(Dispatchers.IO) { plamixHttp("$PLAMIX_API/api/app/trial", "device=$dev") }
            } catch (e: Exception) {
                Pair(-1, "")
            }
            if (r.first in 200..299) {
                val lines = r.second.trim().lines().map { it.trim() }.filter { it.isNotEmpty() }
                val link = lines.firstOrNull() ?: ""
                if (link.startsWith("http")) {
                    if (lines.size > 1) {
                        plamixPrefs(ctx).edit().putString("key", lines[1]).apply()
                        savedKey = lines[1]
                    }
                    plamixClearSubs()
                    onAction(MainAction.ImportBatchConfig(link))
                    onDone(true)
                    return@launch
                }
            }
            toast(
                if (r.first == 409 || r.first == 429) t("Пробный период на этом устройстве уже использован.", "The trial has already been used on this device.")
                else t("Не удалось получить пробный период (код ${r.first}). Попробуйте позже.", "Could not start the trial (code ${r.first}). Try again later.")
            )
            onDone(false)
        }
    }

    BackHandler(enabled = screen != PxScreen.HOME) {
        screen = if (screen == PxScreen.KEY) PxScreen.INFO else if (screen == PxScreen.PLAN) PxScreen.INFO else PxScreen.HOME
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(PxBg)
            .drawBehind {
                if (screen == PxScreen.HOME && visible.isNotEmpty()) {
                    drawRect(
                        brush = Brush.radialGradient(
                            0f to PxPurple.copy(alpha = 0.70f),
                            0.35f to PxPurpleDeep.copy(alpha = 0.40f),
                            0.7f to PxPurpleDeep.copy(alpha = 0.12f),
                            1f to Color.Transparent,
                            center = Offset(size.width / 2f, 0f),
                            radius = size.height * 0.62f
                        )
                    )
                }
            }
            .systemBarsPadding()
    ) {
        when (screen) {
            PxScreen.HOME -> {
                if (visible.isEmpty()) {
                    PxOnboarding(
                        lang = lang,
                        t = ::t,
                        onLang = ::setLang,
                        onApplyKey = { k, done -> applyKey(k, done) },
                        onTrial = { done -> startTrial(done) },
                        onPaste = { onAction(MainAction.ImportClipboard) },
                        onBot = { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) },
                        note = problemNote,
                    )
                } else {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .verticalScroll(rememberScrollState())
                            .padding(horizontal = 24.dp, vertical = 12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(20.dp))
                                    .background(Color.White.copy(alpha = 0.08f))
                                    .clickable { screen = PxScreen.INFO }
                                    .padding(horizontal = 16.dp, vertical = 8.dp)
                            ) {
                                Text(t("Настройки", "Settings"), color = PxWhite, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                            }
                        }
                        Spacer(Modifier.height(16.dp))
                        PxBrand()
                        Spacer(Modifier.height(12.dp))
                        Text(planLine, color = PxWhiteDim, fontSize = 14.sp)
                        Spacer(Modifier.height(10.dp))
                        LinearProgressIndicator(
                            progress = { leftFraction },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(5.dp)
                                .clip(RoundedCornerShape(3.dp)),
                            color = PxPurple,
                            trackColor = PxCardHi
                        )
                        TextButton(onClick = { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }) {
                            Text(t("УЛУЧШИТЬ ТАРИФ", "UPGRADE PLAN"), color = PxPurple, fontWeight = FontWeight.SemiBold)
                        }
                        Spacer(Modifier.height(20.dp))

                        PxPower(running = isRunning, connecting = connecting) {
                            if (!isRunning) connecting = true
                            onAction(MainAction.ToggleService)
                        }
                        Spacer(Modifier.height(16.dp))
                        Text(
                            text = if (isRunning) t("VPN подключён", "VPN connected")
                            else if (connecting) t("Подключаемся…", "Connecting…")
                            else t("Нажмите, чтобы подключиться", "Tap to connect"),
                            color = if (isRunning) PxPurple else PxWhite,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(Modifier.height(24.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(t("Серверы", "Servers"), color = PxWhite, fontSize = 18.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(16.dp))
                                    .background(Color.White.copy(alpha = 0.08f))
                                    .clickable { onAction(MainAction.TestRealAllServers) }
                                    .padding(horizontal = 14.dp, vertical = 7.dp)
                            ) {
                                Text(t("Проверить пинг", "Check ping"), color = PxWhite, fontSize = 13.sp)
                            }
                        }
                        Spacer(Modifier.height(10.dp))
                        PxServerRow(
                            flag = "∞",
                            title = t("Раз и навсегда", "Once and forever"),
                            sub = t("Сам переключает обход и Wi-Fi", "Switches bypass and Wi-Fi by itself"),
                            selected = forever, ms = 0L, testing = false
                        ) { pickForever() }
                        Spacer(Modifier.height(8.dp))
                        if (autoWifi != null) {
                            PxServerRow(
                                flag = "⚡", title = t("Авто выбор", "Auto select") + " WIFI", sub = null,
                                selected = !forever && uiState.selectedGuid == autoWifi.guid,
                                ms = autoWifi.testDelayMillis, testing = uiState.isTesting
                            ) { pickServer(autoWifi) }
                            Spacer(Modifier.height(8.dp))
                        }
                        if (autoLte != null) {
                            PxServerRow(
                                flag = "⚡", title = t("Авто выбор", "Auto select") + " LTE", sub = null,
                                selected = !forever && uiState.selectedGuid == autoLte.guid,
                                ms = autoLte.testDelayMillis, testing = uiState.isTesting
                            ) { pickServer(autoLte) }
                            Spacer(Modifier.height(8.dp))
                        }
                        for (srv in wifiCountries) {
                            val nm = plamixCleanName(srv.profile.remarks)
                            PxServerRow(
                                flag = plamixFlag(nm), title = nm + " WIFI", sub = null,
                                selected = !forever && uiState.selectedGuid == srv.guid,
                                ms = srv.testDelayMillis, testing = uiState.isTesting
                            ) { pickServer(srv) }
                            Spacer(Modifier.height(8.dp))
                        }
                        for (srv in lteCountries) {
                            val nm = plamixCleanName(srv.profile.remarks)
                            PxServerRow(
                                flag = plamixFlag(nm), title = nm + " LTE", sub = null,
                                selected = !forever && uiState.selectedGuid == srv.guid,
                                ms = srv.testDelayMillis, testing = uiState.isTesting
                            ) { pickServer(srv) }
                            Spacer(Modifier.height(8.dp))
                        }
                        Spacer(Modifier.height(16.dp))
                    }
                }
            }

            PxScreen.SERVERS -> {
                Column(modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 14.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            "‹", color = PxPurple, fontSize = 34.sp,
                            modifier = Modifier.clickable { screen = PxScreen.HOME }.padding(horizontal = 10.dp)
                        )
                        Text(
                            t("Выбор сервера", "Choose a server"),
                            color = PxWhite, fontSize = 22.sp, fontWeight = FontWeight.SemiBold,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.weight(1f)
                        )
                        Spacer(Modifier.size(54.dp))
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
                        PxToolCard(
                            title = t("Пинг", "Ping"),
                            sub = if (uiState.isTesting) t("Проверяем…", "Testing…") else t("Проверить задержку", "Check latency"),
                            busy = uiState.isTesting,
                            modifier = Modifier.weight(1f)
                        ) { onAction(MainAction.TestRealAllServers) }
                        PxToolCard(
                            title = t("Автовыбор", "Auto"),
                            sub = t("Оптимальный сервер", "Best server"),
                            modifier = Modifier.weight(1f)
                        ) {
                            val best = shown.filter { it.testDelayMillis > 0L }.minByOrNull { it.testDelayMillis }
                            if (best != null) {
                                onAction(MainAction.SelectServer(best.guid))
                            } else {
                                autoPending = true
                                onAction(MainAction.TestRealAllServers)
                            }
                        }
                    }
                    Spacer(Modifier.height(18.dp))
                    LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        pxSection("", shown, uiState.selectedGuid, onAction) { screen = PxScreen.HOME }
                    }
                }
            }

            PxScreen.INFO -> {
                Column(modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 14.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                "‹", color = PxPurple, fontSize = 34.sp,
                                modifier = Modifier.clickable { screen = PxScreen.HOME }.padding(end = 10.dp)
                            )
                            Text(t("Настройки", "Settings"), color = PxWhite, fontSize = 28.sp, fontWeight = FontWeight.Bold)
                        }
                        PxLangChip(lang, ::setLang)
                    }
                    LazyColumn(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                        item {
                            PxGroup(t("АККАУНТ", "ACCOUNT")) {
                                PxRow(t("Тариф и ключ", "Plan and key")) { screen = PxScreen.PLAN }
                                PxRow(t("Сменить ключ", "Change key")) { screen = PxScreen.KEY }
                                PxRow(t("Удалить аккаунт", "Delete account"), danger = true) { confirmDelete = true }
                            }
                        }
                        item {
                            PxGroup(t("ВОЗМОЖНОСТИ", "FEATURES")) {
                                PxRow(t("Серверы и пинг", "Servers and ping")) { screen = PxScreen.SERVERS }
                                PxRow(t("Раздельное подключение", "Split tunneling")) { onNavigate(MainDestination.PerAppProxy) }
                            }
                        }
                        item {
                            PxGroup(t("ПОДДЕРЖКА", "SUPPORT")) {
                                PxRow(t("Помощь и поддержка", "Help and support")) { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }
                                PxRow(t("Пригласить друга", "Invite a friend")) {
                                    val send = Intent(Intent.ACTION_SEND).apply {
                                        type = "text/plain"
                                        putExtra(Intent.EXTRA_TEXT, "PlamixVless: $PLAMIX_BOT_URL")
                                    }
                                    ctx.startActivity(Intent.createChooser(send, null).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                                }
                                PxRow(t("Сообщить о проблеме", "Report a problem")) { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }
                            }
                        }
                        item {
                            PxGroup(t("ИНФОРМАЦИЯ", "INFORMATION")) {
                                PxRow(t("Сайт и контакты", "Website and contacts")) { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }
                                Row(
                                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 14.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Text(t("Версия", "Version") + " $PLAMIX_VERSION", color = PxWhiteDim, fontSize = 14.sp)
                                    Text("PlamixVless", color = PxWhiteDim, fontSize = 14.sp)
                                }
                            }
                        }
                        item { Spacer(Modifier.height(24.dp)) }
                    }
                }
            }

            PxScreen.PLAN -> {
                Column(modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp)) {
                    PxTopBar(t("Тариф и ключ", "Plan and key")) { screen = PxScreen.INFO }
                    PxGroup(planTitle) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(planLine, color = PxWhite, fontSize = 16.sp)
                            Spacer(Modifier.height(12.dp))
                            LinearProgressIndicator(
                                progress = { leftFraction },
                                modifier = Modifier.fillMaxWidth().height(5.dp).clip(RoundedCornerShape(3.dp)),
                                color = PxPurple,
                                trackColor = PxCardHi
                            )
                            Spacer(Modifier.height(16.dp))
                            Text(t("Ваш ключ", "Your key"), color = PxWhiteDim, fontSize = 13.sp)
                            Spacer(Modifier.height(4.dp))
                            Text(
                                if (savedKey.isNotEmpty()) savedKey else t("Ключ не введён", "No key entered"),
                                color = PxWhite, fontSize = 14.sp, fontWeight = FontWeight.Medium
                            )
                            if (savedKey.isNotEmpty()) {
                                TextButton(onClick = {
                                    val cbm = ctx.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                    cbm.setPrimaryClip(ClipData.newPlainText("key", savedKey))
                                    toast(t("Ключ скопирован", "Key copied"))
                                }) { Text(t("Скопировать ключ", "Copy key"), color = PxPurple) }
                            }
                        }
                    }
                    Spacer(Modifier.height(16.dp))
                    PxPrimaryButton(t("Продлить или улучшить", "Renew or upgrade")) {
                        onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL))
                    }
                }
            }

            PxScreen.KEY -> {
                PxOnboarding(
                    lang = lang,
                    t = ::t,
                    onLang = ::setLang,
                    onApplyKey = { k, done -> applyKey(k) { ok -> if (ok) screen = PxScreen.HOME; done(ok) } },
                    onTrial = { done -> startTrial { ok -> if (ok) screen = PxScreen.HOME; done(ok) } },
                    onPaste = { onAction(MainAction.ImportClipboard) },
                    onBot = { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) },
                    onBack = { screen = PxScreen.INFO },
                    note = problemNote,
                )
            }
        }
    }

    if (confirmDelete) {
        AlertDialog(
            onDismissRequest = { confirmDelete = false },
            containerColor = PxCardHi,
            title = { Text(t("Удалить аккаунт?", "Delete account?"), color = PxWhite) },
            text = {
                Text(
                    t("Ключ и список серверов будут удалены с этого устройства. Подписка в боте останется.",
                        "The key and server list will be removed from this device. Your bot subscription stays."),
                    color = PxWhiteDim
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    confirmDelete = false
                    plamixPrefs(ctx).edit().remove("key").apply()
                    savedKey = ""
                    onAction(MainAction.RemoveAllServers)
                    screen = PxScreen.HOME
                }) { Text(t("Удалить", "Delete"), color = PxPurple) }
            },
            dismissButton = {
                TextButton(onClick = { confirmDelete = false }) { Text(t("Отмена", "Cancel"), color = PxWhite) }
            }
        )
    }
}

@Composable
private fun PxBrand() {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
        Image(
            painter = painterResource(R.drawable.plamix_p),
            contentDescription = null,
            modifier = Modifier.height(40.dp).offset(y = (-3).dp)
        )
        Text("lamixVless", color = PxWhite, fontSize = 28.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun PxPower(running: Boolean, connecting: Boolean, onClick: () -> Unit) {
    val spin = rememberInfiniteTransition(label = "pxspin")
    val angle by spin.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(tween(1100, easing = LinearEasing)),
        label = "pxangle"
    )
    val level by animateFloatAsState(
        targetValue = if (running) 1f else if (connecting) 0.3f else 0f,
        animationSpec = tween(600),
        label = "pxlevel"
    )
    Box(
        modifier = Modifier
            .size(116.dp)
            .clip(CircleShape)
            .background(Color(0xFF0C0716))
            .clickable { onClick() },
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val stroke = 6.dp.toPx()
            val rad = size.minDimension / 2f - stroke / 2f
            drawCircle(color = PxPurple.copy(alpha = 0.06f + 0.50f * level), radius = size.minDimension / 2f)
            drawCircle(color = PxPurpleDeep.copy(alpha = 0.35f + 0.65f * level), radius = rad, style = Stroke(width = stroke))
            if (connecting && !running) {
                drawArc(
                    color = Color(0xFFD8B4FE),
                    startAngle = angle - 90f,
                    sweepAngle = 110f,
                    useCenter = false,
                    topLeft = Offset(stroke / 2f, stroke / 2f),
                    size = Size(size.width - stroke, size.height - stroke),
                    style = Stroke(width = stroke, cap = StrokeCap.Round)
                )
            }
            val c = Offset(size.width / 2f, size.height / 2f)
            val r = 24.dp.toPx()
            val ic = PxWhite.copy(alpha = 0.55f + 0.45f * level)
            drawArc(
                color = ic,
                startAngle = -55f,
                sweepAngle = 290f,
                useCenter = false,
                topLeft = Offset(c.x - r, c.y - r),
                size = Size(r * 2f, r * 2f),
                style = Stroke(width = 5.dp.toPx(), cap = StrokeCap.Round)
            )
            drawLine(
                color = ic,
                start = Offset(c.x, c.y - r - 5.dp.toPx()),
                end = Offset(c.x, c.y - 5.dp.toPx()),
                strokeWidth = 5.dp.toPx(),
                cap = StrokeCap.Round
            )
        }
    }
}

@Composable
private fun PxServerRow(
    flag: String,
    title: String,
    sub: String?,
    selected: Boolean,
    ms: Long,
    testing: Boolean,
    onClick: () -> Unit,
) {
    val shape = RoundedCornerShape(18.dp)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(if (selected) PxPurple.copy(alpha = 0.16f) else Color.White.copy(alpha = 0.05f))
            .border(if (selected) 1.dp else 0.dp, if (selected) PxPurple.copy(alpha = 0.7f) else Color.Transparent, shape)
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(flag, fontSize = 22.sp, color = PxPurple)
        Spacer(Modifier.size(12.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = PxWhite, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            if (sub != null) Text(sub, color = PxWhiteDim, fontSize = 12.sp)
        }
        if (testing) {
            CircularProgressIndicator(modifier = Modifier.size(18.dp), color = PxPurple, strokeWidth = 2.dp)
        } else if (ms > 0L) {
            Text("$ms ms", color = PxPurple, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        }
    }
}

@Composable
private fun PxNetRow(label: String, active: Boolean, ms: Long, testing: Boolean, onClick: () -> Unit) {
    val shape = RoundedCornerShape(16.dp)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(if (active) PxPurple.copy(alpha = 0.16f) else Color.White.copy(alpha = 0.04f))
            .border(if (active) 1.dp else 0.dp, if (active) PxPurple.copy(alpha = 0.6f) else Color.Transparent, shape)
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 11.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            label,
            color = if (active) PxWhite else PxWhiteDim,
            fontSize = 15.sp,
            fontWeight = FontWeight.Medium,
            modifier = Modifier.weight(1f)
        )
        if (testing) {
            CircularProgressIndicator(modifier = Modifier.size(18.dp), color = PxPurple, strokeWidth = 2.dp)
        } else if (ms > 0L) {
            Text("$ms ms", color = PxPurple, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        }
    }
}

@Composable
private fun PxEternal(name: String, bypass: Boolean, wifiLabel: String, bypassLabel: String, onPick: (Boolean) -> Unit) {
    val shape = RoundedCornerShape(18.dp)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(Color.White.copy(alpha = 0.05f))
            .padding(start = 16.dp, end = 8.dp, top = 8.dp, bottom = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(name, color = PxWhite, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
        for (isBypass in listOf(false, true)) {
            val on = bypass == isBypass
            Box(
                modifier = Modifier
                    .padding(start = 6.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .background(if (on) PxPurple else Color.White.copy(alpha = 0.08f))
                    .clickable { onPick(isBypass) }
                    .padding(horizontal = 14.dp, vertical = 8.dp)
            ) {
                Text(
                    if (isBypass) bypassLabel else wifiLabel,
                    color = if (on) PxWhite else PxWhiteDim,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

@Composable
private fun PxLangChip(lang: String, onPick: (String) -> Unit) {
    var open by remember { mutableStateOf(false) }
    Box {
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(22.dp))
                .background(PxCardHi)
                .clickable { open = true }
                .padding(horizontal = 18.dp, vertical = 10.dp)
        ) {
            Text(lang.uppercase() + "  ▾", color = PxWhite, fontSize = 16.sp, fontWeight = FontWeight.Medium)
        }
        DropdownMenu(expanded = open, onDismissRequest = { open = false }, containerColor = PxCardHi) {
            DropdownMenuItem(text = { Text("Русский", color = PxWhite) }, onClick = { open = false; onPick("ru") })
            DropdownMenuItem(text = { Text("English", color = PxWhite) }, onClick = { open = false; onPick("en") })
        }
    }
}

@Composable
private fun PxTopBar(title: String, onBack: () -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text("‹", color = PxPurple, fontSize = 34.sp, modifier = Modifier.clickable { onBack() }.padding(end = 10.dp))
        Text(title, color = PxWhite, fontSize = 24.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun PxBottomButton(label: String, modifier: Modifier, onClick: () -> Unit) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .background(PxCard)
            .border(1.dp, PxPurple.copy(alpha = 0.5f), RoundedCornerShape(20.dp))
            .clickable { onClick() }
            .padding(vertical = 16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(label, color = PxWhite, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
private fun PxPrimaryButton(label: String, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(22.dp))
            .background(Brush.horizontalGradient(listOf(PxPurple, PxPurpleDeep)))
            .clickable { onClick() }
            .padding(vertical = 16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(label, color = PxWhite, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
private fun PxToolCard(title: String, sub: String, modifier: Modifier, busy: Boolean = false, onClick: () -> Unit) {
    Column(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .background(PxCard)
            .clickable { onClick() }
            .padding(16.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(title, color = PxWhite, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
            if (busy) {
                Spacer(Modifier.size(10.dp))
                CircularProgressIndicator(modifier = Modifier.size(16.dp), color = PxPurple, strokeWidth = 2.dp)
            }
        }
        Spacer(Modifier.height(2.dp))
        Text(sub, color = PxWhiteDim, fontSize = 12.sp)
    }
}

@Composable
private fun PxGroup(title: String, content: @Composable () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(PxCard)
            .padding(vertical = 12.dp)
    ) {
        Text(
            title, color = PxPurple, fontSize = 14.sp, fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp)
        )
        content()
    }
}

@Composable
private fun PxRow(label: String, danger: Boolean = false, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 14.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(label, color = if (danger) Color(0xFFFF5C5C) else PxWhite, fontSize = 17.sp)
        Text("›", color = PxPurple, fontSize = 24.sp)
    }
}

@Composable
private fun PxOnboarding(
    lang: String,
    t: (String, String) -> String,
    onLang: (String) -> Unit,
    onApplyKey: (String, (Boolean) -> Unit) -> Unit,
    onTrial: ((Boolean) -> Unit) -> Unit,
    onPaste: () -> Unit,
    onBot: () -> Unit,
    onBack: (() -> Unit)? = null,
    note: String? = null,
) {
    val ctx = LocalContext.current
    var key by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    Column(
        modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            if (onBack != null) {
                Text("‹", color = PxPurple, fontSize = 34.sp, modifier = Modifier.clickable { onBack() }.padding(end = 10.dp))
            } else {
                Spacer(Modifier.size(1.dp))
            }
            PxLangChip(lang, onLang)
        }
        Spacer(Modifier.height(24.dp))
        PxBrand()
        Spacer(Modifier.weight(1f))
        Text(t("Введите ключ", "Enter your key"), color = PxWhite, fontSize = 24.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        Text(
            t("Скопируйте ключ из бота (команда /key) и нажмите «Вставить».", "Copy the key from the bot (command /key) and tap Paste."),
            color = PxWhiteDim, fontSize = 14.sp, textAlign = TextAlign.Center
        )
        Spacer(Modifier.height(20.dp))
        BasicTextField(
            value = key,
            onValueChange = { raw -> key = raw.filter { !it.isWhitespace() }.take(80) },
            maxLines = 3,
            textStyle = TextStyle(color = PxWhite, fontSize = 15.sp, fontWeight = FontWeight.Medium, textAlign = TextAlign.Center),
            cursorBrush = SolidColor(PxPurple),
            modifier = Modifier.fillMaxWidth(),
            decorationBox = { inner ->
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(18.dp))
                        .background(PxCard)
                        .border(1.dp, PxPurple.copy(alpha = 0.6f), RoundedCornerShape(18.dp))
                        .padding(vertical = 16.dp, horizontal = 12.dp),
                    contentAlignment = Alignment.Center
                ) {
                    if (key.isEmpty()) Text(t("Ключ из бота", "Key from the bot"), color = PxWhiteDim.copy(alpha = 0.4f), fontSize = 15.sp)
                    inner()
                }
            }
        )
        Spacer(Modifier.height(10.dp))
        TextButton(onClick = {
            try {
                val cbm = ctx.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val txt = cbm.primaryClip?.getItemAt(0)?.coerceToText(ctx)?.toString() ?: ""
                key = txt.filter { !it.isWhitespace() }.take(80)
            } catch (e: Exception) {
            }
        }) { Text(t("Вставить", "Paste"), color = PxPurple, fontWeight = FontWeight.SemiBold) }
        Spacer(Modifier.height(6.dp))
        PxPrimaryButton(if (busy) t("Проверяем…", "Checking…") else t("Продолжить", "Continue")) {
            if (!busy) {
                busy = true
                onApplyKey(key) { busy = false }
            }
        }
        Spacer(Modifier.height(10.dp))
        TextButton(onClick = {
            if (!busy) {
                busy = true
                onTrial { busy = false }
            }
        }) {
            Text(t("Пробный период: 3 дня и 3 ГБ", "Free trial: 3 days and 3 GB"), color = PxPurple, fontWeight = FontWeight.SemiBold)
        }
        if (note != null) {
            Spacer(Modifier.height(10.dp))
            Text(
                t("Ответ сервера: ", "Server reply: ") + note,
                color = Color(0xFFFF9A9A), fontSize = 13.sp, textAlign = TextAlign.Center
            )
        }
        Spacer(Modifier.weight(1f))
        TextButton(onClick = onBot) { Text(t("Получить ключ в боте", "Get a key in the bot"), color = PxWhite) }
        TextButton(onClick = onPaste) { Text(t("Вставить ссылку подписки", "Paste subscription link"), color = PxWhiteDim) }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.pxSection(
    header: String,
    list: List<ServersCache>,
    selectedGuid: String?,
    onAction: (MainAction) -> Unit,
    onPicked: () -> Unit,
) {
    if (list.isEmpty()) return
    if (header.isNotBlank()) {
        item(key = "h_$header") {
            Text(
                text = header,
                modifier = Modifier.padding(start = 4.dp, top = 6.dp),
                color = PxPurple,
                fontSize = 14.sp,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
    items(list, key = { it.guid }) { s ->
        val on = s.guid == selectedGuid
        val name = plamixCleanName(s.profile.remarks)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(20.dp))
                .background(if (on) PxPurple.copy(alpha = 0.14f) else PxCard)
                .border(if (on) 1.5.dp else 0.dp, if (on) PxPurple else Color.Transparent, RoundedCornerShape(20.dp))
                .clickable {
                    onAction(MainAction.SelectServer(s.guid))
                    onPicked()
                }
                .padding(horizontal = 16.dp, vertical = 16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(plamixFlag(name), fontSize = 26.sp)
            Spacer(Modifier.size(14.dp))
            Text(name, color = PxWhite, fontSize = 18.sp, fontWeight = FontWeight.Medium, modifier = Modifier.weight(1f))
            if (s.testDelayMillis > 0L) {
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(14.dp)).background(PxCardHi).padding(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Text("${s.testDelayMillis} ms", color = PxPurple, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}
"""
KT = KT.replace("__PLAMIX_API__", API_BASE)
wr(f"{APP}/src/main/java/com/v2ray/ang/ui/main/PlamixHome.kt", KT)
MS = f"{APP}/src/main/java/com/v2ray/ang/ui/main/MainScreen.kt"
s = rd(MS)
a = s.index("        Scaffold(\n")
b = s.rindex("\n    }\n}")
s = s[:a] + ("        PlamixHome(\n            mainViewModel = mainViewModel,\n            uiState = uiState,\n"
             "            onAction = onAction,\n            onNavigate = onNavigate,\n        )") + s[b:]
s = s.replace("    ModalNavigationDrawer(\n        drawerState = drawerState,\n", "    ModalNavigationDrawer(\n        drawerState = drawerState,\n        gesturesEnabled = false,\n")
wr(MS, s)

# ---- 7. уведомление: иконка-логотип, без «Перезапуск», «Отключить», плашка «Отключено / Подключить» ----
def glyph(size, color):
    g = pimg.copy()
    g.thumbnail((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", g.size, color + (255,)), ((size - g.size[0]) // 2, (size - g.size[1]) // 2), g.split()[3])
    return out
for root_, dirs_, files_ in os.walk(RES):
    for fn in files_:
        if fn in ("ic_stat_name.png", "ic_stat_proxy.png", "ic_stat_direct.png", "ic_stat_name_black.png"):
            pth = os.path.join(root_, fn)
            sz = Image.open(pth).size[0]
            glyph(sz, (0, 0, 0) if "black" in fn else (255, 255, 255)).save(pth)
NM = f"{APP}/src/main/java/com/v2ray/ang/handler/NotificationManager.kt"
t_ = rd(NM)
r_old = """            )
            .addAction(
                R.drawable.ic_restore_24dp,
                service.getString(R.string.title_service_restart),
                restartV2RayPendingIntent
            )"""
assert t_.count(r_old) == 1
t_ = t_.replace(r_old, "            )")
a_ = "        val service = getService() ?: return\n\n        // Reset last query time"
assert t_.count(a_) == 1
t_ = t_.replace(a_, "        val service = getService() ?: return\n        PlamixOffNotice.hide(service)\n\n        // Reset last query time")
c_ = "        service.stopForeground(Service.STOP_FOREGROUND_REMOVE)\n"
assert t_.count(c_) == 1
t_ = t_.replace(c_, c_ + "        PlamixOffNotice.show(service)\n")
wr(NM, t_)
wr(f"{APP}/src/main/java/com/v2ray/ang/handler/PlamixOffNotice.kt", r"""package com.v2ray.ang.handler

import android.app.NotificationChannel
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.v2ray.ang.R
import com.v2ray.ang.ui.main.MainActivity
import com.v2ray.ang.ui.shortcut.ScStartActivity

/** Плашка в шторке, пока VPN выключен: «Отключено» и кнопка «Подключить». */
object PlamixOffNotice {
    private const val ID = 7701
    private const val CH = "plamix_off"

    fun show(ctx: Context) {
        try {
            val nm = ctx.getSystemService(Context.NOTIFICATION_SERVICE) as android.app.NotificationManager
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                nm.createNotificationChannel(
                    NotificationChannel(CH, "PlamixVless", android.app.NotificationManager.IMPORTANCE_LOW)
                )
            }
            val en = ctx.getSharedPreferences("plamix_ui", Context.MODE_PRIVATE).getString("lang", "ru") == "en"
            val flags = PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
            val open = PendingIntent.getActivity(ctx, 7701, Intent(ctx, MainActivity::class.java), flags)
            val start = PendingIntent.getActivity(ctx, 7702, Intent(ctx, ScStartActivity::class.java), flags)
            val n = NotificationCompat.Builder(ctx, CH)
                .setSmallIcon(R.drawable.ic_stat_name)
                .setContentTitle("PlamixVless")
                .setContentText(if (en) "Disconnected" else "Отключено")
                .setOngoing(true)
                .setShowWhen(false)
                .setOnlyAlertOnce(true)
                .setContentIntent(open)
                .addAction(0, if (en) "Connect" else "Подключить", start)
                .build()
            nm.notify(ID, n)
        } catch (e: Exception) {
        }
    }

    fun hide(ctx: Context) {
        try {
            (ctx.getSystemService(Context.NOTIFICATION_SERVICE) as android.app.NotificationManager).cancel(ID)
        } catch (e: Exception) {
        }
    }
}
""")
for d in os.listdir(RES):
    f = f"{RES}/{d}/strings.xml"
    if d.startswith("values") and os.path.isfile(f):
        word = "Отключить" if d == "values-ru" else ("Disconnect" if d == "values" else None)
        if word:
            wr(f, re.sub(r'(<string name="notification_action_stop_v2ray"[^>]*>)[^<]*', r'\1' + word, rd(f)))
# ярлыки по долгому нажатию на иконку приложения убираем
wr(f"{RES}/xml/shortcuts.xml", '<?xml version="1.0" encoding="utf-8"?>\n<shortcuts xmlns:android="http://schemas.android.com/apk/res/android" />\n')

# ---- 8. идентификатор устройства (x-hwid) в запросах подписки, как у Happ ----
AM = f"{APP}/src/main/java/com/v2ray/ang/handler/AngConfigManager.kt"
am = rd(AM)
o_ = "            val requestHeaders = it.subscription.requestHeaders\n"
assert am.count(o_) == 1
wr(AM, am.replace(o_, "            val requestHeaders = PlamixHwid.headers(it.subscription.requestHeaders)\n"))
wr(f"{APP}/src/main/java/com/v2ray/ang/handler/PlamixHwid.kt", r"""package com.v2ray.ang.handler

import android.os.Build
import android.provider.Settings
import com.v2ray.ang.AngApplication
import org.json.JSONObject

/** Заголовки с идентификатором устройства для запросов подписки (панель без них отдаёт заглушку). */
object PlamixHwid {
    private fun ascii(v: String?): String = (v ?: "").filter { it.code in 32..126 }

    fun headers(existing: String?): String? {
        if (!existing.isNullOrBlank()) return existing
        return try {
            val ctx = AngApplication.application
            val id = Settings.Secure.getString(ctx.contentResolver, Settings.Secure.ANDROID_ID) ?: "plamix"
            val j = JSONObject()
            j.put("x-hwid", ascii(id))
            j.put("x-device-os", "Android")
            j.put("x-ver-os", ascii(Build.VERSION.RELEASE))
            j.put("x-device-model", ascii(Build.MODEL))
            j.toString()
        } catch (e: Exception) {
            existing
        }
    }
}
""")

print("plamix_patch: ok")
