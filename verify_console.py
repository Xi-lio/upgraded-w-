"""
在真实浏览器引擎（Edge headless）中加载页面，注入错误捕获探针，
然后用 --dump-dom 取回结果，客观判定控制台是否有报错。

判定口径：
  - window error / unhandledrejection / console.error  -> 计入 ERROR
  - console.warn                                        -> 单独计入 WARN（不计为失败）
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
  window.__warn = [];
  window.addEventListener('error', function (e) {
    window.__err.push('ERROR: ' + e.message + ' @ ' + (e.filename || '') + ':' + e.lineno);
  });
  window.addEventListener('unhandledrejection', function (e) {
    window.__err.push('REJECTION: ' + e.reason);
  });
  var oe = console.error, ow = console.warn;
  console.error = function () {
    window.__err.push('console.error: ' + Array.prototype.join.call(arguments, ' '));
    oe.apply(console, arguments);
  };
  console.warn = function () {
    window.__warn.push('console.warn: ' + Array.prototype.join.call(arguments, ' '));
    ow.apply(console, arguments);
  };
  setTimeout(function () {
    var d = document.createElement('div');
    d.id = '__diagnostics__';
    d.textContent = 'ERRORS=' + window.__err.length +
                    ' | WARNINGS=' + window.__warn.length +
                    ' | DETAIL=' + window.__err.concat(window.__warn).join(' ;; ');
    document.body.appendChild(d);
  }, 1800);
})();
</script>
"""

targets = [
    "index.html",
    "starter_code/04_fixed_solution/index.html",
    "bonus_a_double_pendulum/index.html",
    "bonus_b_celestial_persistence/index.html",
]

all_ok = True
for rel in targets:
    src = os.path.join(ROOT, rel.replace("/", os.sep))
    html = open(src, encoding="utf-8").read()
    probed = html.replace("<head>", "<head>\n" + PROBE, 1)
    probe_path = os.path.join(TMP, rel.replace("/", "__"))
    open(probe_path, "w", encoding="utf-8").write(probed)

    url = "file:///" + probe_path.replace("\\", "/")
    cmd = [
        EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={os.path.join(TMP, 'profile')}",
        "--window-size=900,800",
        "--virtual-time-budget=4000",
        "--dump-dom", url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    dom = r.stdout or ""
    m = re.search(r'<div id="__diagnostics__">(.*?)</div>', dom, re.S)
    if not m:
        print(f"FAIL  {rel}  —— 探针未回写（页面可能未正常执行）")
        all_ok = False
        continue

    text = m.group(1)
    errors = int(re.search(r"ERRORS=(\d+)", text).group(1))
    warns = int(re.search(r"WARNINGS=(\d+)", text).group(1))
    detail = text.split("DETAIL=", 1)[1] if "DETAIL=" in text else ""

    verdict = "PASS" if errors == 0 else "FAIL"
    if errors != 0:
        all_ok = False
    print(f"{verdict}  {rel}")
    print(f"      控制台错误 {errors} 条 / 警告 {warns} 条")
    if errors and detail.strip():
        print(f"      详情: {detail[:400]}")

print()
print("总体判定：" + ("全部页面控制台 0 报错 ✅" if all_ok else "存在报错 ❌"))
