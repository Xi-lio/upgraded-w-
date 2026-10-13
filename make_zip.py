"""打包实验交付物为 Week05_Lab_学号姓名.zip（含 .git 提交历史，排除浏览器临时目录）"""
import os
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"C:\Users\MR\WorkBuddy\2026-10-12-17-17-56\week05_pendulum_sim"
DST = r"C:\Users\MR\WorkBuddy\2026-10-12-17-17-56\Week05_Lab_学号姓名.zip"
ARC_TOP = "Week05_Lab_学号姓名"

EXCLUDE_DIRS = {"screenshots/_probe", "task04_repair/_tmp"}
EXCLUDE_PREFIXES = ("screenshots/_edgeprofile_", "screenshots/_probe")


def should_skip(rel_posix: str) -> bool:
    parts = rel_posix.split("/")
    for p in parts:
        if p.startswith("_edgeprofile_") or p == "_tmp" or p == "_probe":
            return True
    if rel_posix.startswith(EXCLUDE_PREFIXES):
        return True
    if any(rel_posix == d or rel_posix.startswith(d + "/") for d in EXCLUDE_DIRS):
        return True
    if "__MACOSX" in parts:
        return True
    # 临时草稿文件
    base = parts[-1]
    if base.startswith("_") and base.endswith(".txt"):
        return True
    return False


if os.path.exists(DST):
    os.remove(DST)

count = 0
with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if not d.startswith("_edgeprofile_") and d not in ("_probe", "_tmp")]
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, SRC).replace("\\", "/")
            if should_skip(rel):
                continue
            z.write(full, ARC_TOP + "/" + rel)
            count += 1

size = os.path.getsize(DST)
print("输出文件 :", DST)
print("条目数量 :", count)
print("压缩体积 :", f"{size/1024:.1f} KB")

# 列出顶层结构，便于核对
with zipfile.ZipFile(DST) as z:
    names = z.namelist()
print("\n--- 顶层条目 ---")
tops = sorted({n.split("/")[1] for n in names if len(n.split("/")) > 1 and n.split("/")[1]})
for t in tops:
    print(" ", t)

git_files = [n for n in names if "/.git/" in n]
print(f"\n.git 历史文件数 : {len(git_files)}（含提交记录，可供教师核验 Commit 历史）")
