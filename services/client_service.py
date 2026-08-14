import os
import uuid

UPLOAD_FOLDER = "static/clients"

IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp"
}

def save_client_logo(file):

    ext = file.filename.rsplit(".",1)[1].lower()

    if ext not in IMAGE_EXTENSIONS:
        raise Exception("Invalid file.")

    filename = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return filename