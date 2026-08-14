from configure import mysql


def get_dashboard_counts():

    cursor = mysql.connection.cursor()

    stats = {}

    # Total CV
    cursor.execute("""
        SELECT COUNT(*) total
        FROM candidates
    """)
    stats["total_cv"] = cursor.fetchone()["total"]

    # Today's CV
    cursor.execute("""
        SELECT COUNT(*) total
        FROM candidates
        WHERE DATE(uploaded_at)=CURDATE()
    """)
    stats["today_cv"] = cursor.fetchone()["total"]

    # Total Applications
    cursor.execute("""
        SELECT COUNT(*) total
        FROM applications
    """)
    stats["total_applications"] = cursor.fetchone()["total"]

    # Today's Applications
    cursor.execute("""
        SELECT COUNT(*) total
        FROM applications
        WHERE DATE(applied_at)=CURDATE()
    """)
    stats["today_applications"] = cursor.fetchone()["total"]

    # Active Jobs
    cursor.execute("""
        SELECT COUNT(*) total
        FROM jobs
        WHERE status='Active'
    """)
    stats["active_jobs"] = cursor.fetchone()["total"]

    # Closed Jobs
    cursor.execute("""
        SELECT COUNT(*) total
        FROM jobs
        WHERE status='Closed'
    """)
    stats["closed_jobs"] = cursor.fetchone()["total"]

    # Total Messages
    cursor.execute("""
        SELECT COUNT(*) total
        FROM contacts
    """)
    stats["total_messages"] = cursor.fetchone()["total"]

    # Weekly Messages
    cursor.execute("""
        SELECT COUNT(*) total
        FROM contacts
        WHERE created_at>=DATE_SUB(NOW(),INTERVAL 7 DAY)
    """)
    stats["weekly_messages"] = cursor.fetchone()["total"]

    cursor.close()

    return stats