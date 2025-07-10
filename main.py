from cleaner import check_file_type
from filemanager import MediaService
from database import create_table, post_filemeta

create_table()

class FileWrapper:
    def __init__(self, path: str):
        self.filename = path.split("/")[-1]
        self.file = open(path, "rb")

    def close(self):
        self.file.close()

def secure_upload(file):
    try:
        detected_type = check_file_type(file)

        if detected_type == "unknown":
            raise ValueError("Unsupported or unknown file type.")
        if detected_type.startswith("mismatch"):
            raise ValueError(f"File extension doesn't match content: {detected_type}")

        # Upload to MinIO
        upload_url = MediaService.upload(file)

        # Save metadata to SQLite
        post_filemeta(name=file.filename, file_type=detected_type, signature=get_signature_string(file))

        return upload_url
    except ValueError as error:
        return f"Error while verifying encoding and file type: {error}"

def get_signature_string(file):
    file.file.seek(0)
    signature_bytes = file.file.read(20)
    file.file.seek(0)
    return signature_bytes.hex().upper()

if __name__ == "__main__":
    file = FileWrapper("test.xlsx")
    try:
        result = secure_upload(file)
        print(result)
    finally:
        file.close()
