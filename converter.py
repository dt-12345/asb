try:
    from zstd import *
except ImportError:
    raise ImportError("zstd.py not found")
try:
    from asb import *
except ImportError:
    raise ImportError("asb.py not found")
try:
    from baev import *
except ImportError:
    raise ImportError("baev.py not found")

import os
from pathlib import Path
from functools import lru_cache

@lru_cache
def get_ctx(romfs_path):
    if not os.path.exists("romfs.txt"):
        with open("romfs.txt", "w") as f:
            pass
    if romfs_path == "":
        romfs_path = Path("romfs.txt").read_text("utf-8")
        if romfs_path == "":
            raise ValueError("Please provide a romfs path")
    return ZstdDecompContext(os.path.join(romfs_path, "Pack/ZsDic.pack.zs"))

def decompress(filepath, romfs_path):
    return get_ctx(romfs_path).decompress(filepath)

def compress(filepath, romfs_path=""):
    return get_ctx(romfs_path).compress(filepath)

# the baev file here needs to be a AsNode baev file and not an Animation one
def asb_to_json(filepath, output_dir="", romfs_path="", baev_path=""):
    if romfs_path != "":
        with open("romfs.txt", "w", encoding="utf-8") as f:
            f.write(romfs_path)
    if filepath.endswith(".zs") or filepath.endswith(".zstd"):
        data = decompress(filepath, romfs_path)
    else:
        data = Path(filepath).read_bytes()
    file = ASB.from_binary(data)
    if baev_path != "":
        if baev_path.endswith(".zs") or baev_path.endswith(".zstd"):
            file.import_baev(decompress(baev_path, romfs_path))
        elif baev_path.endswith(".baev"):
            file.import_baev(Path(baev_path).read_bytes())
        else:
            file.import_baev(json.loads(Path(baev_path).read_text("utf-8")))
    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)
    file.to_json(output_dir)

def json_to_asb(filepath, output_dir="", compress_file=False, romfs_path=""):
    if romfs_path != "":
        with open("romfs.txt", "w", encoding="utf-8") as f:
            f.write(romfs_path)
    file = ASB.from_dict(json.loads(Path(filepath).read_text("utf-8")))
    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)
    if compress_file:
        file.to_binary()
        data = compress(file.filename + ".asb", romfs_path)
        with open(os.path.join(output_dir, file.filename + ".asb.zs"), "wb") as f:
            f.write(data)
        os.remove(file.filename + ".asb")
        if os.path.exists(file.filename + ".baev"):
            data = compress(file.filename + ".baev", romfs_path)
            with open(os.path.join(output_dir, file.filename + ".baev.zs"), "wb") as f:
                f.write(data)
            os.remove(file.filename + ".baev")
    else:
        file.to_binary(output_dir)

def baev_to_json(filepath, output_dir="", romfs_path=""):
    if romfs_path != "":
        with open("romfs.txt", "w", encoding="utf-8") as f:
            f.write(romfs_path)
    if filepath.endswith(".zs") or filepath.endswith(".zstd"):
        data = decompress(filepath, romfs_path)
    else:
        data = Path(filepath).read_bytes()
    file = BAEV.from_binary(data, os.path.basename(filepath).replace(".baev", "").replace(".zs", ""))
    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)
    file.to_json(output_dir)

def json_to_baev(filepath, output_dir="", compress_file=False, romfs_path=""):
    if romfs_path != "":
        with open("romfs.txt", "w", encoding="utf-8") as f:
            f.write(romfs_path)
    file = BAEV.from_dict(json.loads(Path(filepath).read_text("utf-8")), os.path.basename(filepath).replace(".json", ""))
    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)
    if compress_file:
        file.to_binary()
        data = compress(file.filename + ".baev", romfs_path)
        with open(os.path.join(output_dir, file.filename + ".baev.zs"), "wb") as f:
            f.write(data)
        os.remove(file.filename + ".baev")
    else:
        file.to_binary(output_dir)