"""
任务四 ReAct 闭环自愈 —— 针对用户提供的 Downloads/index.html 执行完整闭环：

  ① 观察 (Observe)  : 真实浏览器加载 + 自动点击「重置摆动」，抓取报错堆栈
  ② 思考 (Think)    : 定位调用点与定义点的标识符不一致
  ③ 行动 (Act)      : 外科手术式一行修复（统一标识符）
  ④ 再观察 (Verify) : 重新加载 + 再次点击，确认控制台 0 报错且功能恢复
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SRC = r"C:\Users\MR\Downloads\index.html"
OUTDIR = r"C:\Users\MR\WorkBuddy\2026-10-12-17-17-56\week05_pendulum_sim\task04_repair"
os.makedirs(OUTDIR, exist_ok=True)
TMP = os.path.join(OUTDIR, "_tmp")
os.makedirs(TMP, exist_ok=True)

PROBE = """<script>
(function () {
  window.__err = [];
  window.addEventListener('error', function (e) {
    window.__err.push(e.message + ' @ line ' + e.lineno + ':' + e.colno);
  });
  setTimeout(function () {
    var btn = document.getElementById('resetBtn');
    var before = { angle: (typeof angle !== 'undefined') ? angle : null };
    if (btn) btn.click();
    setTimeout(function () {
      var after = { angle: (typeof angle !== 'undefined') ? angle : null };
      var d = document.createElement('div');
      d.id = '__diagnostics__';
      d.textContent = 'CLICKED=' + (!!btn) +
                      ' | ERROR_COUNT=' + window.__err.length +
                      ' | ANGLE_BEFORE=' + before.angle +
                      ' | ANGLE_AFTER=' + after.angle +
                      ' | DETAIL=' + window.__err.join(' ;; ');
      document.body.appendChild(d);
    }, 300);
  }, 1200);
})();
</script>
"""


def run_probe(html: str, tag: str):
    probed = html.replace("<head>", "<head>\n" + PROBE, 1)
    p = os.path.join(TMP, tag + ".html")
    open(p, "w", encoding="utf-8").write(probed)
    url = "file:///" + p.replace("\\", "/")
    cmd = [
        EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={os.path.join(TMP, 'profile_' + tag)}",
        "--window-size=900,800", "--virtual-time-budget=4000", "--dump-dom", url,
    ]
    dom = subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout or ""
    m = re.search(r'<div id="__diagnostics__">(.*?)</div>', dom, re.S)
    if not m:
        return None
    t = m.group(1)
    return {
        "errors": int(re.search(r"ERROR_COUNT=(\d+)", t).group(1)),
        "before": re.search(r"ANGLE_BEFORE=([\-\d.]+)", t).group(1),
        "after": re.search(r"ANGLE_AFTER=([\-\d.]+)", t).group(1),
        "detail": (t.split("DETAIL=", 1)[1] if "DETAIL=" in t else "").strip(),
    }


src_html = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- ① 观察
print("=" * 68)
print("① 观察 (Observe) —— 在真实浏览器中复现故障")
print("=" * 68)
r1 = run_probe(src_html, "before")
if r1 is None:
    print("探针未回写，无法继续")
    sys.exit(1)
print(f"  自动点击重置按钮      : 已执行")
print(f"  捕获报错条数          : {r1['errors']}")
print(f"  报错内容              : {r1['detail']}")
print(f"  点击前摆角            : {r1['before']} rad")
print(f"  点击后摆角            : {r1['after']} rad")
ok_before = r1["errors"] > 0 and r1["before"] == r1["after"]
print(f"  结论                  : {'故障确已复现（报错且复位失效）' if ok_before else '未复现'}")

# ---------------------------------------------------------------- ② 思考
print()
print("=" * 68)
print("② 思考 (Think) —— 根因定位")
print("=" * 68)
call_site = re.search(r'onclick="([A-Za-z_$][\w$]*)\(\)"', src_html)
defs = re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(", src_html)
called = call_site.group(1)
print(f"  调用点 (HTML onclick) : {called}()  —— 全局作用域查找")
print(f"  源码中已定义的函数    : {', '.join(defs)}")
print(f"  是否存在同名定义      : {'是' if called in defs else '否  ← 这就是根因'}")
print()
print("  根因：onclick 属性在全局作用域解析标识符，而脚本只定义了")
print("        resetSimulationState，从未定义 resetAnimation。")
print("        调用点与定义点的标识符不一致 → 运行时 ReferenceError。")
print("        与物理公式无关，属纯作用域/命名问题。")

# ---------------------------------------------------------------- ③ 行动
print()
print("=" * 68)
print("③ 行动 (Act) —— 外科手术式修复")
print("=" * 68)

# 方案：把函数定义重命名为 onclick 期望的标识符（与官方 04_fixed_solution 一致）
fixed = src_html.replace(
    "function resetSimulationState() {",
    "function resetAnimation() {",
    1,
)
# 同步更新注释，避免注释与代码不符
fixed = fixed.replace(
    "// 注意：这里函数名故意写成了 resetSimulationState，导致上面 onclick 调用的 resetAnimation 未定义！",
    "// 修复：函数名与 onclick 调用的标识符统一为 resetAnimation，调用链闭合",
    1,
)
changed = fixed != src_html
print(f"  修改行数              : {'1 处函数声明 + 1 处注释' if changed else '无'}")
print("  diff:")
for i, (a, b) in enumerate(zip(src_html.splitlines(), fixed.splitlines()), 1):
    if a != b:
        print(f"    line {i}")
        print(f"      - {a.strip()}")
        print(f"      + {b.strip()}")

out_path = os.path.join(OUTDIR, "index.html")
open(out_path, "w", encoding="utf-8", newline="\n").write(fixed)
print(f"  已写出                : {out_path}")

# ---------------------------------------------------------------- ④ 再观察
print()
print("=" * 68)
print("④ 再观察 (Verify) —— 回归验证")
print("=" * 68)
r2 = run_probe(fixed, "after")
if r2 is None:
    print("探针未回写")
    sys.exit(1)
print(f"  自动点击重置按钮      : 已执行")
print(f"  捕获报错条数          : {r2['errors']}")
print(f"  报错内容              : {r2['detail'] or '(无)'}")
print(f"  点击前摆角            : {r2['before']} rad")
print(f"  点击后摆角            : {r2['after']} rad")
reset_ok = abs(float(r2["after"]) - 0.7853981633974483) < 1e-9
print(f"  复位功能              : {'已恢复（精准回到 π/4 = 45°）' if reset_ok else '仍异常'}")
print()
verdict = r2["errors"] == 0 and reset_ok
print("最终判定：" + ("PASS —— 控制台 0 报错且重置功能恢复，自愈闭环完成 ✅"
                    if verdict else "FAIL ❌"))
