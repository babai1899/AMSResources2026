from configure import mysql

def get_announcement():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM announcements
        LIMIT 1
    """)

    announcement = cursor.fetchone()

    cursor.close()

    return announcement


def update_announcement(message, admin_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE announcements
        SET
            message=%s,
            updated_by=%s
        WHERE id=1
    """, (message, admin_id))

    mysql.connection.commit()

    cursor.close()