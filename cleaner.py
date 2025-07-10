import os

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
    "zip": ["zip", "xlsx", "docx", "pptx"],
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
            return ftype
    return "unknown"


def check_file_type(file) -> str:
    """
    Validates file by comparing its extension to its signature.
    """
    file.file.seek(0)
    signature_bytes = file.file.read(20)  # first 20 bytes
    print(f"Signature Bytes: {signature_bytes}")
    file.file.seek(0)
    actual_type = get_file_signature(signature_bytes)

    if actual_type == "unknown":
        return "unknown"

    ext = os.path.splitext(file.filename)[1].lower().strip(".")
    valid_extensions = EXTENSION_MAP.get(actual_type, [])

    if ext not in valid_extensions:
        return f"mismatch (extension: .{ext}, signature: {actual_type})"

    return actual_type
