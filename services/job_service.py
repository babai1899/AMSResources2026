from datetime import datetime
from configure import mysql

# Auto Generate Mandate ID
def generate_mandate_id():

    year = datetime.now().year

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT mandate_id
        FROM jobs
        WHERE mandate_id LIKE %s
        ORDER BY id DESC
        LIMIT 1
    """, (f"AMS-{year}-%",))

    last = cursor.fetchone()

    cursor.close()

    if last:

        last_number = int(last["mandate_id"].split("-")[-1])

        new_number = last_number + 1

    else:

        new_number = 1

    return f"AMS-{year}-{new_number:04d}"