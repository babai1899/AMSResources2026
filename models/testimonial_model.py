import os
from configure import mysql

# ----------------------------
# Add
# ----------------------------
def add_testimonial(
    full_name,
    designation,
    message,
    photo
):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO testimonials
        (
            full_name,
            designation,
            message,
            photo
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
    """,(

        full_name,
        designation,
        message,
        photo

    ))

    mysql.connection.commit()

    cursor.close()


# ----------------------------
# All
# ----------------------------
def get_all_testimonials():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM testimonials
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()

    cursor.close()

    return data


# ----------------------------
# Active
# ----------------------------
def get_active_testimonials():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM testimonials
        WHERE status='Active'
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()

    cursor.close()

    return data


# ----------------------------
# Single
# ----------------------------
def get_testimonial(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM testimonials
        WHERE id=%s
    """,(id,))

    data = cursor.fetchone()

    cursor.close()

    return data


# ----------------------------
# Update
# ----------------------------
def update_testimonial(
    id,
    full_name,
    designation,
    message,
    photo=None
):

    cursor = mysql.connection.cursor()

    if photo:

        cursor.execute("""

            UPDATE testimonials

            SET

                full_name=%s,

                designation=%s,

                message=%s,

                photo=%s

            WHERE id=%s

        """,(

            full_name,
            designation,
            message,
            photo,
            id

        ))

    else:

        cursor.execute("""

            UPDATE testimonials

            SET

                full_name=%s,

                designation=%s,

                message=%s

            WHERE id=%s

        """,(

            full_name,
            designation,
            message,
            id

        ))

    mysql.connection.commit()

    cursor.close()


# ----------------------------
# Status
# ----------------------------
def toggle_status(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""

        UPDATE testimonials

        SET status=

        IF(status='Active','Inactive','Active')

        WHERE id=%s

    """,(id,))

    mysql.connection.commit()

    cursor.close()


# ----------------------------
# Delete
# ----------------------------
def delete_testimonial(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""

        SELECT photo

        FROM testimonials

        WHERE id=%s

    """,(id,))

    image = cursor.fetchone()

    if image:

        path = os.path.join(
            "static/testimonials",
            image["photo"]
        )

        if os.path.exists(path):

            os.remove(path)

    cursor.execute("""

        DELETE FROM testimonials

        WHERE id=%s

    """,(id,))

    mysql.connection.commit()

    cursor.close()
