from configure import mysql


# =====================================================
# Keep Latest 200 Notifications
# =====================================================

def cleanup_notifications(limit=200):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        DELETE FROM notifications
        WHERE id NOT IN
        (
            SELECT id FROM
            (
                SELECT id
                FROM notifications
                ORDER BY id DESC
                LIMIT %s
            ) x
        )
        """,
        (limit,)
    )

    mysql.connection.commit()

    cursor.close()


# =====================================================
# Create Notification
# =====================================================

def create_notification(
        category,
        action,
        title,
        message,
        icon,
        color,
        priority="normal",
        link=None,
        created_by=None
):

    cursor = mysql.connection.cursor()
    
    print("Creating notification...")

    try:
        cursor.execute(
            """
            INSERT INTO notifications
            (
                category,
                action,
                title,
                message,
                icon,
                color,
                priority,
                link,
                created_by
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                category,
                action,
                title,
                message,
                icon,
                color,
                priority,
                link,
                created_by
            )
        )

        mysql.connection.commit()
        print("Notification inserted.")

    except Exception as e:
        print("Notification Error:", e)
        mysql.connection.rollback()

    finally:
        cursor.close()

    cleanup_notifications()


# =====================================================
# Get Latest Notifications
# =====================================================

def get_notifications(limit=20):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            category,
            action,
            title,
            message,
            icon,
            color,
            priority,
            link,
            created_by,
            is_read,
            created_at
        FROM notifications
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (limit,)
    )

    data = cursor.fetchall()

    cursor.close()

    return data


# =====================================================
# Get Unread Count
# =====================================================

def get_unread_notification_count():

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM notifications
        WHERE is_read=0
        """
    )

    result = cursor.fetchone()

    cursor.close()

    return result["total"] if result else 0


# =====================================================
# Mark One Read
# =====================================================

def mark_notification_read(notification_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE notifications
        SET is_read=1
        WHERE id=%s
        """,
        (notification_id,)
    )

    mysql.connection.commit()

    cursor.close()


# =====================================================
# Mark All Read
# =====================================================

def mark_all_notifications_read():

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE notifications
        SET is_read=1
        WHERE is_read=0
        """
    )

    mysql.connection.commit()

    cursor.close()


# =====================================================
# Delete One Notification
# =====================================================

def delete_notification(notification_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        DELETE FROM notifications
        WHERE id=%s
        """,
        (notification_id,)
    )

    mysql.connection.commit()

    cursor.close()


# =====================================================
# Clear All Notifications
# =====================================================

def clear_notifications():

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        DELETE FROM notifications
        """
    )

    mysql.connection.commit()

    cursor.close()


# =====================================================
# Get Notification By ID
# =====================================================

def get_notification(notification_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM notifications
        WHERE id=%s
        """,
        (notification_id,)
    )

    data = cursor.fetchone()

    cursor.close()

    return data


# =====================================================
# Delete Notifications Older Than X Days
# (Optional Scheduler)
# =====================================================

def delete_old_notifications(days=90):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        DELETE FROM notifications
        WHERE created_at <
        DATE_SUB(NOW(),INTERVAL %s DAY)
        """,
        (days,)
    )

    mysql.connection.commit()

    cursor.close()