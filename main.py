from cleaner import check_file_type
from filemanager import MediaService


def secure_upload(file):
    try:
        detected_type = check_file_type(file)

        if detected_type == "unknown":
            raise ValueError("Unsupported or unknown file type.")
        if detected_type.startswith("mismatch"):
            raise ValueError(f"File extension doesn't match content: {detected_type}")

        return MediaService.upload(file)
    except ValueError as error:
        return f"Error while verifying encoding and file type: {error}"
