"""
音频转 base64 工具

用法:
    from tools import audio2base64
    b64 = audio2base64("recording.wav")

CLI:
    python tools/audio2base64.py recording.wav
"""

import base64
from pathlib import Path
import sys
import os


def audio2base64(file_path: str) -> str:
    """将音频文件转为 base64 字符串。

    Args:
        file_path: 音频文件路径

    Returns:
           base64 编码字符串

    Raises:
        FileNotFoundError: 文件不存在
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"文件不存在: {file_path} (绝对路径: {path.resolve()})")

    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ── CLI ─────────────────────────────────────────────────────


def _cli():
    import argparse

    parser = argparse.ArgumentParser(description="音频转 base64 工具")
    parser.add_argument("audio", nargs="?", help="音频文件路径")
    args = parser.parse_args()

    if not args.audio:
        parser.print_help()
        sys.exit(0)

    try:
        b64 = audio2base64(args.audio)
        size_kb = os.path.getsize(args.audio) / 1024

        print(f"# 文件: {args.audio} ({size_kb:.1f} KB)")
        print(f"# base64 长度: {len(b64)} 字符\n")
        print(b64)

    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
