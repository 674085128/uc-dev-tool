#!/usr/bin/env python3
"""
UC-dev-tool 自更新脚本。

原理（对应公司工具"每次对话检查最新版本自动更新"）：
  1. 读本地 VERSION 文件
  2. 查 GitHub 远程 VERSION 文件
  3. 对比，不同则 git pull 更新

用法：
  python update.py

说明：Claude 宿主没有"每次对话自动跑脚本"的钩子，所以本脚本需要你
定期手动运行（或加入定时任务）。运行一次 = 完成一次"检查+更新"。
"""
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = "674085128/uc-dev-tool"
BRANCH = "main"

# 仓库根目录 = 本脚本所在目录
REPO_DIR = Path(__file__).resolve().parent
VERSION_FILE = REPO_DIR / "VERSION"


def read_local_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def read_remote_version() -> str:
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/VERSION"
    with urllib.request.urlopen(url, timeout=15) as resp:
        return resp.read().decode("utf-8").strip()


def main() -> int:
    local = read_local_version()
    print(f"本地版本: {local}")

    try:
        remote = read_remote_version()
    except Exception as e:
        print(f"[!] 无法连接 GitHub 获取远程版本：{e}")
        print("    请检查网络后重试。")
        return 1

    print(f"远程版本: {remote}")

    if local == remote:
        print("[✓] 已是最新版本，无需更新。")
        return 0

    print(f"[!] 发现新版本 {remote}，正在更新...")
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), "pull", "--ff-only"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("[✓] 更新完成。")
        if result.stdout:
            print(result.stdout.strip())
        return 0

    print("[!] git pull 失败，可能是本地有改动或不是通过 git clone 获取的。")
    print("    手动更新方式：")
    print(f"    cd {REPO_DIR}")
    print("    git pull")
    if result.stderr:
        print(result.stderr.strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
