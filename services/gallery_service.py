import os
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/gallery"

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}

def save_gallery_media(file):

    ext = file.filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    if ext in IMAGE_EXTENSIONS:
        media_type = "image"
    elif ext in VIDEO_EXTENSIONS:
        media_type = "video"
    else:
        raise Exception("Unsupported file type")

    return filename, media_type