from configure import mysql

from services.client_service import save_client_logo

import os

def add_client(name, country, logo, admin_id):

    filename = save_client_logo(logo)

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO clients
        (
            client_name,
            country,
            logo_file,
            created_by
        )
        VALUES(%s,%s,%s,%s)
    """,
    (
        name,
        country,
        filename,
        admin_id
    ))

    mysql.connection.commit()

    cursor.close()
    
def get_clients():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM clients
        ORDER BY client_name
    """)

    data = cursor.fetchall()

    cursor.close()

    return data

def delete_client(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT logo_file
        FROM clients
        WHERE id=%s
    """,(id,))

    row = cursor.fetchone()

    if row:

        path = os.path.join(
            "static/clients",
            row["logo_file"]
        )

        if os.path.exists(path):
            os.remove(path)

    cursor.execute("""
        DELETE FROM clients
        WHERE id=%s
    """,(id,))

    mysql.connection.commit()

    cursor.close()
    
def get_clients():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM clients
        ORDER BY client_name
    """)

    clients = cursor.fetchall()

    cursor.close()

    return clients

def get_client(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM clients
        WHERE id=%s
    """, (id,))

    client = cursor.fetchone()

    cursor.close()

    return client