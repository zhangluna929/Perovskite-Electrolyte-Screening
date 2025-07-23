#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data_fetcher.py

提供从 Materials Project 下载 CIF 结构文件的实用函数。
需要环境变量 `MP_API_KEY` 或命令行 `--api-key` 传入。

用法示例：
    python src/utils/data_fetcher.py --mp-ids mp-1902 mp-5827 \
           --save-dir data/raw_materials/ --api-key YOUR_KEY

作者：LunaZhang
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List

from pymatgen.ext.matproj import MPRester

DEFAULT_SAVE_DIR = Path("data/raw_materials")
DEFAULT_SAVE_DIR.mkdir(parents=True, exist_ok=True)

def download_cif(mp_id: str, api_key: str, save_dir: Path = DEFAULT_SAVE_DIR) -> Path:
    """下载单个 Materials Project 结构并保存为 CIF。

    Parameters
    ----------
    mp_id : str
        Materials Project ID (如 "mp-1902").
    api_key : str
        个人 Materials Project API Key。
    save_dir : Path
        保存目录，默认为 data/raw_materials/。

    Returns
    -------
    Path
        保存的 CIF 文件路径。
    """
    save_dir.mkdir(parents=True, exist_ok=True)

    with MPRester(api_key) as mpr:
        structure = mpr.get_structure_by_material_id(mp_id)
        cif_path = save_dir / f"{mp_id}.cif"
        structure.to(fmt="cif", filename=cif_path)
        print(f"✓ 下载并保存 {mp_id} → {cif_path.relative_to(Path.cwd())}")
        return cif_path

def batch_download(mp_ids: List[str], api_key: str, save_dir: Path = DEFAULT_SAVE_DIR):
    """批量下载多个 mp-ids CIF 文件。"""
    for mp_id in mp_ids:
        try:
            download_cif(mp_id, api_key, save_dir)
        except Exception as exc:
            print(f"✗ 下载 {mp_id} 失败: {exc}")


def _parse_cli():
    parser = argparse.ArgumentParser(description="Download CIFs from Materials Project")
    parser.add_argument("--mp-ids", nargs="+", required=True, help="List of mp-ids to download")
    parser.add_argument(
        "--save-dir", default=str(DEFAULT_SAVE_DIR), help="Directory to save cif files"
    )
    parser.add_argument("--api-key", default=os.getenv("MP_API_KEY"), help="Materials Project API key")
    return parser.parse_args()


def main():
    args = _parse_cli()
    if args.api_key is None:
        raise RuntimeError("未提供 Materials Project API Key，请设置 MP_API_KEY 环境变量或使用 --api-key")

    save_dir = Path(args.save_dir)
    batch_download(args.mp_ids, args.api_key, save_dir)

if __name__ == "__main__":
    main() 