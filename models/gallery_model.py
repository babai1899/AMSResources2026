from configure import mysql
from services.gallery_service import save_gallery_media
import os

def get_gallery():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM gallery
        ORDER BY id DESC
    """)

    images = cursor.fetchall()

    cursor.close()

    return images

def add_gallery_image(title, file, admin_id):

    filename, media_type = save_gallery_media(file)

    cursor = mysql.connection.cursor()

    cursor.execute("""
    INSERT INTO gallery
    (
        title,
        media_file,
        media_type,
        uploaded_by
    )
    VALUES
    (%s,%s,%s,%s)
    """,
    (
        title,
        filename,
        media_type,
        admin_id
    ))

    mysql.connection.commit()

    cursor.close()

def delete_gallery_image(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT media_file
        FROM gallery
        WHERE id=%s
    """, (id,))

    media = cursor.fetchone()

    if media:

        path = os.path.join(
            "static/gallery",
            media["media_file"]
        )

        if os.path.exists(path):
            os.remove(path)

    cursor.execute("""
        DELETE FROM gallery
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()
    cursor.close()
    
# =========== PUBLIC ===========
def get_public_gallery():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            media_file,
            media_type
        FROM gallery
        ORDER BY id DESC
    """)

    gallery = cursor.fetchall()

    cursor.close()

    return gallery

def get_gallery_image(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM gallery
        WHERE id=%s
        """,
        (id,)
    )

    data = cursor.fetchone()

    cursor.close()

    return data