"""
图片转 base64 工具

用法:
    from tools import img2base64

    b64 = img2base64("photo.jpg")                         # 纯 base64 字符串
    b64 = img2base64("photo.jpg", format="data_uri")      # data URI 格式
    b64 = img2base64("photo.jpg", format="langchain")     # LangChain block dict
    b64 = img2base64("photo.jpg", format="langchain_url") # OpenAI 兼容 block dict

CLI:
    python tools/img2base64.py photo.jpg
    python tools/img2base64.py photo.jpg --data-uri
"""

import base64 as _base64
import sys
import os
from pathlib import Path
from typing import Literal

# ── MIME 类型映射 ──────────────────────────────────────────

MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".tiff": "image/tiff",
}


def get_mime_type(file_path: str) -> str:
    """根据文件扩展名推断 MIME 类型"""
    ext = Path(file_path).suffix.lower()
    if ext not in MIME_MAP:
        raise ValueError(
            f"不支持的图片格式: {ext}，支持的格式: {list(MIME_MAP.keys())}"
        )
    return MIME_MAP[ext]


# ── 核心函数 ──────────────────────────────────────────────


def _encode_file(file_path: str) -> str:
    """读取文件并返回 base64 编码字符串"""
    with open(file_path, "rb") as f:
        return _base64.b64encode(f.read()).decode("utf-8")


def to_raw(file_path: str) -> str:
    """返回纯 base64 字符串"""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"图片文件不存在: {file_path} " f"(绝对路径: {os.path.abspath(file_path)})"
        )
    return _encode_file(file_path)


def to_data_uri(file_path: str) -> str:
    """返回 data URI 格式: data:image/xxx;base64,..."""
    mime = get_mime_type(file_path)
    return f"data:{mime};base64,{to_raw(file_path)}"


def to_langchain(file_path: str) -> "dict[str, str]":
    """返回 LangChain ImageContentBlock 格式"""
    mime = get_mime_type(file_path)
    return {"type": "image", "base64": to_raw(file_path), "mime_type": mime}


def to_langchain_url(file_path: str) -> "dict[str, str]":
    """返回 OpenAI 兼容 image_url block 格式"""
    return {
        "type": "image_url",
        "image_url": {"url": to_data_uri(file_path)},
    }


# ── 主入口：img2base64 ─────────────────────────────────────


def img2base64(
    file_path: str,
    *,
    format: Literal["raw", "data_uri", "langchain", "langchain_url"] = "raw",
):
    """将图片转为 base64。

    Args:
        file_path: 图片文件路径（支持相对路径和绝对路径）
        format:
            "raw"           — 纯 base64 字符串（默认）
            "data_uri"      — data:image/xxx;base64,... 格式
            "langchain"     — LangChain ImageContentBlock dict
            "langchain_url" — OpenAI 兼容 image_url block dict

    Returns:
        str 或 dict，取决于 format 参数

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的图片格式
    """
    if format == "data_uri":
        return to_data_uri(file_path)
    elif format == "langchain":
        return to_langchain(file_path)
    elif format == "langchain_url":
        return to_langchain_url(file_path)
    else:
        return to_raw(file_path)


# ── CLI ─────────────────────────────────────────────────────


def _cli():
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="图片转 base64 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("image", nargs="?", help="图片文件路径")
    parser.add_argument("--data-uri", action="store_true")
    parser.add_argument("--langchain", action="store_true")
    parser.add_argument("--langchain-url", action="store_true")
    parser.add_argument("--copy", action="store_true", help="复制到剪贴板")

    args = parser.parse_args()

    if not args.image:
        parser.print_help()
        sys.exit(0)

    try:
        mime = get_mime_type(args.image)
        b64 = to_raw(args.image)
        size_kb = os.path.getsize(args.image) / 1024

        print(f"# 文件: {args.image} ({size_kb:.1f} KB, {mime})")
        print(f"# base64 长度: {len(b64)} 字符\n")

        if args.langchain:
            block = to_langchain(args.image)
            print("## LangChain content block:")
            print(json.dumps(block, indent=2, ensure_ascii=False))
            output = json.dumps(block, ensure_ascii=False)
        elif args.langchain_url:
            block = to_langchain_url(args.image)
            print("## LangChain image_url block (OpenAI 兼容):")
            print(json.dumps(block, indent=2, ensure_ascii=False))
            output = json.dumps(block, ensure_ascii=False)
        elif args.data_uri:
            output = to_data_uri(args.image)
            print(output)
        else:
            output = b64
            print(output)

        if args.copy:
            try:
                import pyperclip

                pyperclip.copy(output)
                print("\n✅ 已复制到剪贴板")
            except ImportError:
                print("\n⚠️  未安装 pyperclip（pip install pyperclip）")

    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
