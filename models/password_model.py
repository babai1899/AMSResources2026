from configure import mysql


# ---------------------------------
# Get Admin by Email
# ---------------------------------
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


# ---------------------------------
# Update Password
# ---------------------------------
def update_admin_password(admin_id, password):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE admins
        SET password=%s
        WHERE id=%s
    """, (
        password,
        admin_id
    ))

    mysql.connection.commit()

    cursor.close()