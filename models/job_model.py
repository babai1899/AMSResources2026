from configure import mysql


def add_job(data):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO jobs
        (
            mandate_id,
            employer,
            designation,
            industry,
            experience,
            location,
            specifications,
            status,
            created_by
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        data["mandate_id"],
        data["employer"],
        data["designation"],
        data["industry"],
        data["experience"],
        data["location"],
        data["specifications"],
        data["status"],
        data["created_by"]

    ))

    mysql.connection.commit()

    cursor.close()
    
def get_job(job_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE id=%s
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    cursor.close()

    return job
    
def get_all_jobs():

    cursor = mysql.connection.cursor()

    cursor.execute("""

        SELECT

            jobs.*,

            admins.first_name,
            admins.surname

        FROM jobs

        JOIN admins

        ON admins.id = jobs.created_by

        ORDER BY jobs.id DESC

    """)

    jobs = cursor.fetchall()

    cursor.close()

    return jobs

# Get Active Jobs for current-openings
def get_active_jobs():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE status='Active'
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    cursor.close()

    return jobs

# Update Job Status
def update_job_status(job_id, status):
    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status=%s
        WHERE id=%s
    """, (status, job_id))

    mysql.connection.commit()
    cursor.close()
    
# Delete Job
def delete_job(job_id):

    cursor = mysql.connection.cursor()

    cursor.execute(

        "DELETE FROM jobs WHERE id=%s",

        (job_id,)

    )

    mysql.connection.commit()

    cursor.close()

# Close Job
def close_job(job_id):

    cursor = mysql.connection.cursor()

    cursor.execute(

        """
        UPDATE jobs
        SET status='Closed'
        WHERE id=%s
        """,

        (job_id,)

    )

    mysql.connection.commit()

    cursor.close()

# Active a Closed Job    
def activate_job(job_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status='Active'
        WHERE id=%s
    """, (job_id,))

    mysql.connection.commit()
    cursor.close()
    
def get_job_by_mandate(mandate_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE mandate_id=%s
          AND status='Active'
    """, (mandate_id,))

    job = cursor.fetchone()

    cursor.close()

    return job

def get_job_by_id(job_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE id=%s
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    cursor.close()

    return job