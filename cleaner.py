import os
import zipfile
from io import BytesIO

FILE_SIGNATURES = {
    b"\xFF\xD8\xFF": "jpeg",
    b"\x89PNG\r\n\x1A\n": "png",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
    b"\x42\x4D": "bmp",
    b"\x49\x49\x2A\x00": "tiff",
    b"\x4D\x4D\x00\x2A": "tiff",
    b"%PDF": "pdf",
    b"PK\x03\x04": "zip",
    b"Rar!\x1A\x07\x00": "rar",
    b"Rar!\x1A\x07\x01\x00": "rar",
    b"\x7FELF": "elf",
    b"MZ": "exe",
    b"\x00\x00\x00\x14ftyp": "mp4",
    b"\x1F\x8B\x08": "gzip",
    b"OggS": "ogg",
    b"ID3": "mp3",
    b"\xFF\xFB": "mp3",
}

EXTENSION_MAP = {
    "jpeg": ["jpg", "jpeg"],
    "png": ["png"],
    "gif": ["gif"],
    "bmp": ["bmp"],
    "tiff": ["tif", "tiff"],
    "pdf": ["pdf"],
    "docx": ["docx"],
    "xlsx": ["xlsx"],
    "pptx": ["pptx"],
    "zip": ["zip"],
    "rar": ["rar"],
    "elf": ["elf"],
    "exe": ["exe"],
    "mp4": ["mp4"],
    "gzip": ["gz"],
    "ogg": ["ogg"],
    "mp3": ["mp3"],
}


def get_file_signature(file_bytes: bytes) -> str:
    for sig, ftype in FILE_SIGNATURES.items():
        if file_bytes.startswith(sig):
            if ftype == "zip":
                try:
                    zip_file = zipfile.ZipFile(BytesIO(file_bytes))
                    names = zip_file.namelist()

                    if "[Content_Types].xml" in names:
                        if any(name.startswith("xl/") for name in names):
                            return "xlsx"
                        elif any(name.startswith("word/") for name in names):
                            return "docx"
                        elif any(name.startswith("ppt/") for name in names):
                            return "pptx"
                    return "zip"
                except Exception as e:
                    print("Zip check failed:", e)
                    return "zip"
            return ftype
    return "unknown"


def check_file_type(file) -> str:
    file.file.seek(0)
    file_bytes = file.file.read() 
    file.file.seek(0)

    print(f"Signature Bytes: {file_bytes[:20]}")

    actual_type = get_file_signature(file_bytes)

    if actual_type == "unknown":
        return "unknown"

    ext = os.path.splitext(file.filename)[1].lower().strip(".")
    valid_extensions = EXTENSION_MAP.get(actual_type, [])

    if ext not in valid_extensions:
        return f"mismatch (extension: .{ext}, signature: {actual_type})"

    return actual_type
