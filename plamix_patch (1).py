# plamix_patch.py - перебрендинг клиента (PlamixVless): имя, пакет, фиолетовая тема, иконка.
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
LOGO_B64 = "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"
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
KT = r"""package com.v2ray.ang.ui.main

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.systemBarsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.v2ray.ang.dto.entities.ServersCache
import com.v2ray.ang.extension.toTrafficString
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

private const val PLAMIX_BOT_URL = "https://t.me/Zynoravlessrobot_bot"
private val PlamixEmptyServers: StateFlow<List<ServersCache>> = MutableStateFlow(emptyList())

private fun plamixCleanName(remarks: String): String =
    remarks
        .replace(Regex("\\s*\\|?\\s*\\[(WIFI|LTE)\\]", RegexOption.IGNORE_CASE), "")
        .replace(Regex("\\s*#\\d+"), "")
        .trim()

@Composable
fun PlamixHome(
    mainViewModel: MainViewModel,
    uiState: MainUiState,
    onAction: (MainAction) -> Unit,
    onMenu: () -> Unit,
) {
    val groups = uiState.groups
    val group = groups.firstOrNull { it.id == uiState.selectedGroupId } ?: groups.firstOrNull()
    val serversFlow: StateFlow<List<ServersCache>> =
        if (group != null) mainViewModel.serversForGroup(group.id) else PlamixEmptyServers
    val servers by serversFlow.collectAsStateWithLifecycle()
    val visible = servers.filter { (it.profile.server ?: "") != "0.0.0.0" }
    val selected = visible.firstOrNull { it.guid == uiState.selectedGuid }
    val isRunning = uiState.isRunning
    var showServers by remember { mutableStateOf(false) }

    val info = group?.usageInfo
    val title = info?.title ?: "Тариф"
    var planLine = "Подписка не загружена"
    var leftFraction = 0f
    if (info != null) {
        val parts = ArrayList<String>()
        if (info.total > 0L) {
            val used = info.upload + info.download
            parts.add("Осталось " + (info.total - used).coerceAtLeast(0L).toTrafficString())
            leftFraction = (1f - used.toFloat() / info.total.toFloat()).coerceIn(0f, 1f)
        } else {
            parts.add("Трафик без лимита")
            leftFraction = 1f
        }
        if (info.expire > 0L) {
            val days = ((info.expire * 1000L - System.currentTimeMillis()) / 86400000L).coerceAtLeast(0L)
            parts.add("на $days дн.")
        }
        planLine = parts.joinToString(" ")
    }

    val shownFraction = leftFraction
    val accent = MaterialTheme.colorScheme.primary
    val ring = if (isRunning) accent else MaterialTheme.colorScheme.outline

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .systemBarsPadding()
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 24.dp, vertical = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Surface(
                shape = RoundedCornerShape(28.dp),
                color = MaterialTheme.colorScheme.background,
                border = BorderStroke(2.dp, accent)
            ) {
                Text(
                    text = "PlamixVless",
                    modifier = Modifier.padding(horizontal = 28.dp, vertical = 10.dp),
                    color = accent,
                    fontSize = 26.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            Spacer(Modifier.height(36.dp))
            Text(text = title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Spacer(Modifier.height(4.dp))
            Text(
                text = planLine,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(Modifier.height(10.dp))
            LinearProgressIndicator(
                progress = { shownFraction },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(5.dp)
                    .clip(RoundedCornerShape(3.dp)),
                color = accent,
                trackColor = MaterialTheme.colorScheme.surfaceVariant
            )
            TextButton(onClick = { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }) {
                Text("УЛУЧШИТЬ ТАРИФ", fontWeight = FontWeight.SemiBold)
            }

            Spacer(Modifier.weight(1f))

            if (visible.isEmpty()) {
                Text(
                    text = "Добавьте ключ",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.SemiBold
                )
                Spacer(Modifier.height(8.dp))
                Text(
                    text = "Скопируйте ссылку-подписку из бота и нажмите кнопку ниже.",
                    textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(Modifier.height(20.dp))
                Button(onClick = { onAction(MainAction.ImportClipboard) }) {
                    Text("Вставить из буфера")
                }
                TextButton(onClick = { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }) {
                    Text("Получить ключ в боте")
                }
            } else {
                Box(
                    modifier = Modifier
                        .size(220.dp)
                        .clip(CircleShape)
                        .background(if (isRunning) accent.copy(alpha = 0.14f) else MaterialTheme.colorScheme.surfaceContainer)
                        .clickable { onAction(MainAction.ToggleService) },
                    contentAlignment = Alignment.Center
                ) {
                    Canvas(modifier = Modifier.fillMaxSize()) {
                        val stroke = 8.dp.toPx()
                        drawCircle(
                            color = ring,
                            radius = size.minDimension / 2f - stroke / 2f,
                            style = Stroke(width = stroke)
                        )
                        val c = Offset(size.width / 2f, size.height / 2f)
                        val r = 38.dp.toPx()
                        drawArc(
                            color = ring,
                            startAngle = -55f,
                            sweepAngle = 290f,
                            useCenter = false,
                            topLeft = Offset(c.x - r, c.y - r),
                            size = Size(r * 2f, r * 2f),
                            style = Stroke(width = 8.dp.toPx(), cap = StrokeCap.Round)
                        )
                        drawLine(
                            color = ring,
                            start = Offset(c.x, c.y - r - 6.dp.toPx()),
                            end = Offset(c.x, c.y - 6.dp.toPx()),
                            strokeWidth = 8.dp.toPx(),
                            cap = StrokeCap.Round
                        )
                    }
                }
                Spacer(Modifier.height(24.dp))
                Text(
                    text = if (isRunning) "VPN подключён" else "Нажмите, чтобы подключиться",
                    style = MaterialTheme.typography.titleMedium,
                    color = if (isRunning) accent else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(Modifier.height(20.dp))
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = MaterialTheme.colorScheme.surfaceContainerHigh,
                    modifier = Modifier.clickable { showServers = true }
                ) {
                    Text(
                        text = if (selected != null) plamixCleanName(selected.profile.remarks) else "Выберите сервер",
                        modifier = Modifier.padding(horizontal = 22.dp, vertical = 12.dp),
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
            }

            Spacer(Modifier.weight(1f))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                TextButton(onClick = { showServers = true }) { Text("Серверы") }
                TextButton(onClick = { onAction(MainAction.OpenSubscriptionLink(PLAMIX_BOT_URL)) }) { Text("Подарок") }
                TextButton(onClick = onMenu) { Text("Меню") }
            }
        }
    }

    if (showServers) {
        val wifi = visible.filter { it.profile.remarks.contains("WIFI", ignoreCase = true) }
        val lte = visible.filter { it.profile.remarks.contains("LTE", ignoreCase = true) }
        val other = visible.filter { s -> s !in wifi && s !in lte }
        Dialog(onDismissRequest = { showServers = false }) {
            Surface(shape = RoundedCornerShape(24.dp), color = MaterialTheme.colorScheme.surfaceContainerHigh) {
                Column(modifier = Modifier.padding(vertical = 16.dp)) {
                    Text(
                        text = "Выбор сервера",
                        modifier = Modifier.padding(horizontal = 20.dp),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(Modifier.height(8.dp))
                    LazyColumn {
                        plamixSection("Wi-Fi", wifi, uiState.selectedGuid, onAction) { showServers = false }
                        plamixSection("Мобильный интернет", lte, uiState.selectedGuid, onAction) { showServers = false }
                        plamixSection("Серверы", other, uiState.selectedGuid, onAction) { showServers = false }
                    }
                }
            }
        }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.plamixSection(
    header: String,
    list: List<ServersCache>,
    selectedGuid: String?,
    onAction: (MainAction) -> Unit,
    onPicked: () -> Unit,
) {
    if (list.isEmpty()) return
    item(key = "h_$header") {
        Text(
            text = header,
            modifier = Modifier.padding(start = 20.dp, end = 20.dp, top = 12.dp, bottom = 4.dp),
            color = androidx.compose.material3.MaterialTheme.colorScheme.primary,
            fontWeight = FontWeight.SemiBold
        )
    }
    items(list, key = { it.guid }) { s ->
        val on = s.guid == selectedGuid
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clickable {
                    onAction(MainAction.SelectServer(s.guid))
                    onPicked()
                }
                .padding(horizontal = 20.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = plamixCleanName(s.profile.remarks),
                fontWeight = if (on) FontWeight.Bold else FontWeight.Normal,
                color = if (on) androidx.compose.material3.MaterialTheme.colorScheme.primary
                else androidx.compose.material3.MaterialTheme.colorScheme.onSurface
            )
            if (s.testDelayMillis > 0L) {
                Text(
                    text = "${s.testDelayMillis} мс",
                    color = androidx.compose.material3.MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
"""
wr(f"{APP}/src/main/java/com/v2ray/ang/ui/main/PlamixHome.kt", KT)
MS = f"{APP}/src/main/java/com/v2ray/ang/ui/main/MainScreen.kt"
s = rd(MS)
a = s.index("        Scaffold(\n")
b = s.rindex("\n    }\n}")
s = s[:a] + ("        PlamixHome(\n            mainViewModel = mainViewModel,\n            uiState = uiState,\n"
             "            onAction = onAction,\n            onMenu = { scope.launch { drawerState.open() } },\n        )") + s[b:]
wr(MS, s)

print("plamix_patch: ok")
