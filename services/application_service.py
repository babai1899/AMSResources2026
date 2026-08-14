import os
from werkzeug.utils import secure_filename
from configure import mysql
from datetime import datetime

UPLOAD_FOLDER = "static/uploads"

def save_file(file, folder):

    if not file or file.filename == "":
        return ""

    filename = secure_filename(file.filename)

    path = os.path.join(
        UPLOAD_FOLDER,
        folder
    )

    os.makedirs(path, exist_ok=True)

    file.save(os.path.join(path, filename))

    return f"{folder}/{filename}"

def generate_application_id():

    year = datetime.now().year

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE YEAR(applied_at)=%s
    """, (year,))

    total = cursor.fetchone()["total"] + 1

    cursor.close()

    return f"APP-{year}-{total:04d}"