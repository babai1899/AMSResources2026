from configure import mysql


def add_contact(
    full_name,
    email,
    subject,
    message
):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO contacts
        (
            full_name,
            email,
            subject,
            message
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
    """, (

        full_name,
        email,
        subject,
        message

    ))

    mysql.connection.commit()

    cursor.close()
    
# ========= Messages in Dashboard ==========

def get_all_messages():
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM contacts
        ORDER BY created_at DESC
    """)

    messages = cursor.fetchall()

    cursor.close()

    return messages


def get_message(id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM contacts
        WHERE id=%s
    """, (id,))

    message = cursor.fetchone()

    cursor.close()

    return message


def mark_message_read(id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE contacts
        SET status='Read'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()
    cursor.close()
    
def mark_message_unread(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE contacts
        SET status='Unread'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()
    cursor.close()

def archive_message(id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE contacts
        SET status='Archived'
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()
    cursor.close()


def delete_message(id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM contacts
        WHERE id=%s
    """, (id,))

    mysql.connection.commit()
    cursor.close()
    
# ----------------------------
# Mark message as replied
# ----------------------------
def mark_as_replied(message_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE contacts
        SET status='Replied'
        WHERE id=%s
    """, (message_id,))

    mysql.connection.commit()
    cursor.close()
    
# ===== Count unread messages ======
def unread_messages_count():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM contacts
        WHERE status='Unread'
    """)

    total = cursor.fetchone()["total"]

    cursor.close()

    return total

# ===== Search messages ======
def search_messages(keyword):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM contacts
        WHERE
            full_name LIKE %s
            OR email LIKE %s
            OR subject LIKE %s
        ORDER BY created_at DESC
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    messages = cursor.fetchall()

    cursor.close()

    return messages

# ====== Get messages by status ======
def get_messages_by_status(status):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM contacts
        WHERE status=%s
        ORDER BY created_at DESC
    """, (status,))

    messages = cursor.fetchall()

    cursor.close()

    return messages
