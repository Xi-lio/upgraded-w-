import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ROOT = r"C:\Users\MR\WorkBuddy\2026-10-12-17-17-56\week05_pendulum_sim"
OUT = os.path.join(ROOT, "screenshots")
os.makedirs(OUT, exist_ok=True)

targets = [
    ("index.html", "01_main_pendulum.png", (940, 900)),
    ("bonus_a_double_pendulum/index.html", "02_bonus_a_double_pendulum.png", (940, 880)),
    ("bonus_b_celestial_persistence/index.html", "03_bonus_b_celestial.png", (940, 880)),
    ("starter_code/03_buggy_practice/index.html", "04_task04_buggy_before.png", (940, 880)),
    ("task04_repair/index.html", "05_task04_repair_after.png", (940, 880)),
]

for rel, outname, (w, h) in targets:
    src = os.path.join(ROOT, rel.replace("/", os.sep))
    dst = os.path.join(OUT, outname)
    url = "file:///" + src.replace("\\", "/")
    userdir = os.path.join(OUT, "_edgeprofile_" + outname.replace(".png", ""))

    cmd = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={userdir}",
        f"--window-size={w},{h}",
        "--virtual-time-budget=2500",
        f"--screenshot={dst}",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    ok = os.path.exists(dst)
    size = os.path.getsize(dst) if ok else 0
    print(f"{'OK  ' if ok else 'FAIL'} {outname:38s} {size:>8d} bytes")
    if not ok:
        print("   stderr:", (r.stderr or "")[:300])
