from configure import mysql


def admin_exists(username, email):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id
        FROM admins
        WHERE username=%s
        OR email=%s
    """, (username, email))

    admin = cursor.fetchone()

    cursor.close()

    return admin


def get_admin_by_id(admin_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM admins
        WHERE id=%s
    """, (admin_id,))

    admin = cursor.fetchone()

    cursor.close()

    return admin


def insert_admin(data):

    cursor = mysql.connection.cursor()

    cursor.execute("""

        INSERT INTO admins(

            title,
            first_name,
            surname,
            username,
            email,
            password,
            role

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s)

    """, (

        data["title"],
        data["first_name"],
        data["surname"],
        data["username"],
        data["email"],
        data["password"],
        data["role"]

    ))

    mysql.connection.commit()

    cursor.close()
    
def get_admin_by_email(email):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM admins
        WHERE email=%s
    """, (email,))

    admin = cursor.fetchone()

    cursor.close()

    return admin