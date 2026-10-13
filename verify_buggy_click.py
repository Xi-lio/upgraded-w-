"""
真实浏览器复现任务四故障：加载 03_buggy_practice，注入探针 + 自动点击「重置」按钮，
捕获 onclick 抛出的 ReferenceError，验证演练页确实会报错。
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ROOT = r"C:\Users\MR\WorkBuddy\2026-10-12-17-17-56\week05_pendulum_sim"
TMP = os.path.join(ROOT, "screenshots", "_probe")
os.makedirs(TMP, exist_ok=True)

PROBE = """<script>
(function () {
  window.__err = [];
  window.addEventListener('error', function (e) {
    window.__err.push(e.message + ' @ ' + (e.filename || '').split('/').pop() + ':' + e.lineno + ':' + e.colno);
  });
  setTimeout(function () {
    var btn = document.getElementById('resetBtn');
    if (btn) btn.click();                     // 自动触发 onclick，复现报错现场
    setTimeout(function () {
      var d = document.createElement('div');
      d.id = '__diagnostics__';
      d.textContent = 'CLICKED=' + (!!btn) + ' | ERROR_COUNT=' + window.__err.length +
                      ' | DETAIL=' + window.__err.join(' ;; ');
      document.body.appendChild(d);
    }, 300);
  }, 1200);
})();
</script>
"""

src = os.path.join(ROOT, "starter_code", "03_buggy_practice", "index.html")
html = open(src, encoding="utf-8").read()
probed = html.replace("<head>", "<head>\n" + PROBE, 1)
probe_path = os.path.join(TMP, "buggy_probe.html")
open(probe_path, "w", encoding="utf-8").write(probed)

url = "file:///" + probe_path.replace("\\", "/")
cmd = [
    EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
    "--no-default-browser-check",
    f"--user-data-dir={os.path.join(TMP, 'profile2')}",
    "--window-size=900,800",
    "--virtual-time-budget=4000",
    "--dump-dom", url,
]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
dom = r.stdout or ""
m = re.search(r'<div id="__diagnostics__">(.*?)</div>', dom, re.S)

if not m:
    print("FAIL —— 探针未回写")
    sys.exit(1)

text = m.group(1)
clicked = "CLICKED=true" in text
count = int(re.search(r"ERROR_COUNT=(\d+)", text).group(1))
detail = text.split("DETAIL=", 1)[1] if "DETAIL=" in text else ""

print(f"按钮是否被自动点击    : {clicked}")
print(f"捕获到的报错条数      : {count}")
print(f"报错内容              : {detail}")
print()
print("判定：" + ("PASS —— 故障页确实抛出了 ReferenceError，演练有效 ✅"
                if count > 0 else "FAIL —— 未复现报错 ❌"))
