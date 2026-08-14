from configure import mysql
from services.application_service import save_file
from services.candidate_service import save_file, generate_candidate_id

def save_candidate(form, files):

    candidate_id = generate_candidate_id()

    full_name = form["full_name"]
    contact_number = form["contact_number"]
    email = form["email"]
    target_role = form["target_role"]

    cv_file = save_file(files["cv_file"], "candidates")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO candidates
        (
            candidate_id,
            full_name,
            contact_number,
            email,
            target_role,
            cv_file
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
    """, (
        candidate_id,
        full_name,
        contact_number,
        email,
        target_role,
        cv_file
    ))

    mysql.connection.commit()
    cursor.close()
    
def get_all_candidates():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        ORDER BY uploaded_at DESC
    """)

    candidates = cursor.fetchall()

    cursor.close()

    return candidates

def update_candidate_status(candidate_id, status):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE candidates
        SET status=%s
        WHERE id=%s
    """,(status,candidate_id))

    mysql.connection.commit()

    cursor.close()