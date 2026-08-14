from configure import mysql
from services.application_service import save_file
from services.application_service import generate_application_id

def get_all_applications():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    cursor.close()

    return applications

def get_application_by_id(id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        WHERE id=%s
    """, (id,))

    application = cursor.fetchone()

    cursor.close()

    return application

def update_application_status(application_id, status):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE applications
        SET status=%s
        WHERE id=%s
    """, (status, application_id))

    mysql.connection.commit()
    cursor.close()
    
def save_application(form, files, job):
    
    application_id = generate_application_id()
    
    full_name = form["full_name"]
    passport_no = form["passport_no"]
    dob = form["dob"]
    age = form["age"]
    passport_type = form["passport_type"]
    phone = form["phone"]
    email = form["email"]
    gender = form["gender"]
    marital_status = form["marital_status"]
    address = form["address"]
    india_experience = form["india_experience"]
    gulf_experience = form["gulf_experience"]
    total_experience = form["total_experience"]
    qualification = form["qualification"]
    
    cv = save_file(files.get("cv"), "cv")
    passport = save_file(files.get("passport_copy"), "passport")
    photo = save_file(files.get("photo"), "photo")
    education = save_file(files.get("education_certificate"), "education")
    experience = save_file(files.get("experience_certificate"), "experience")
    trade = save_file(files.get("trade_certificate"), "trade")
    
    employer = job["employer"]
    designation = job["designation"]
    mandate_id = job["mandate_id"]
    
    cursor = mysql.connection.cursor()
    
    cursor.execute("""
        INSERT INTO applications
        (
        application_id,
        mandate_id,
        employer,
        designation,
        full_name,
        passport_no,
        dob,
        age,
        passport_type,
        phone,
        email,
        gender,
        marital_status,
        address,
        india_experience,
        gulf_experience,
        total_experience,
        qualification,
        cv_file,
        passport_copy,
        photo,
        education_certificate,
        experience_certificate,
        trade_certificate
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
        application_id,
        mandate_id,
        employer,
        designation,
        full_name,
        passport_no,
        dob,
        age,
        passport_type,
        phone,
        email,
        gender,
        marital_status,
        address,
        india_experience,
        gulf_experience,
        total_experience,
        qualification,
        cv,
        passport,
        photo,
        education,
        experience,
        trade
        ))
    
    mysql.connection.commit()
    cursor.close()
    
def delete_application_by_id(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cursor.close()