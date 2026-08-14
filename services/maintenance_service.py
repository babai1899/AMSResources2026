import os
import zipfile
from datetime import datetime

import subprocess
from configure import Config

import tempfile

import shutil

from configure import mysql

DATABASE_NAME = "ams_db"

BACKUP_FOLDER = "backups/cv"

CV_FOLDER = "static/uploads/candidates"
UPLOAD_FOLDER = "static/uploads/candidates"
BACKUP_FOLDER = "backups"

def format_size(size):

    if size < 1024:
        return f"{size} B"

    elif size < 1024 * 1024:
        return f"{size/1024:.1f} KB"

    elif size < 1024 * 1024 * 1024:
        return f"{size/(1024*1024):.2f} MB"

    return f"{size/(1024*1024*1024):.2f} GB"

def get_maintenance_stats():

    # -------------------------
    # DATABASE SIZE
    # -------------------------

    cursor = mysql.connection.cursor()

    cursor.execute("""

        SELECT
        ROUND(SUM(data_length+index_length)/1024/1024,2) AS db_size

        FROM information_schema.TABLES

        WHERE table_schema=%s

    """,(DATABASE_NAME,))

    db = cursor.fetchone()

    cursor.close()
    
    db_size = f"{db['db_size'] if db and db['db_size'] else 0} MB"

    # -------------------------
    # Candidate Files
    # -------------------------

    file_count = 0

    if os.path.exists(UPLOAD_FOLDER):

        for _,_,files in os.walk(UPLOAD_FOLDER):

            file_count += len(files)

    # -------------------------
    # Last SQL Backup
    # -------------------------

    sql_time = "Never"

    cv_time = "Never"

    if os.path.exists(BACKUP_FOLDER):

        sql_files = []

        zip_files = []

        for f in os.listdir(BACKUP_FOLDER):

            path = os.path.join(BACKUP_FOLDER,f)

            if f.endswith(".sql"):

                sql_files.append(path)

            if f.endswith(".zip"):

                zip_files.append(path)

        if sql_files:

            latest=max(sql_files,key=os.path.getmtime)

            sql_time = os.path.getmtime(latest)

        if zip_files:

            latest=max(zip_files,key=os.path.getmtime)

            cv_time = os.path.getmtime(latest)

        import datetime

        if sql_time!="Never":

            sql_time=datetime.datetime.fromtimestamp(
                sql_time
            ).strftime("%d %b %Y %I:%M %p")

        if cv_time!="Never":

            cv_time=datetime.datetime.fromtimestamp(
                cv_time
            ).strftime("%d %b %Y %I:%M %p")

    return {

        "database_size":db_size,

        "candidate_files":file_count,

        "last_sql_backup":sql_time,

        "last_cv_backup":cv_time,
        
        "database_status": "Connected",
        
        "mail_status": "SMTP Connected",
        
        "system_status": "ONLINE"

    }

def create_candidate_backup():

    os.makedirs(
        BACKUP_FOLDER,
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "Candidate_Backup_%Y%m%d_%H%M%S.zip"
    )

    zip_path = os.path.join(
        BACKUP_FOLDER,
        filename
    )

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for root, dirs, files in os.walk(CV_FOLDER):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                archive_name = os.path.relpath(
                    file_path,
                    CV_FOLDER
                )

                zipf.write(
                    file_path,
                    archive_name
                )

    return zip_path

def get_candidate_folder_size():

    total_size = 0

    if os.path.exists(UPLOAD_FOLDER):

        for dirpath, _, filenames in os.walk(UPLOAD_FOLDER):

            for file in filenames:

                path = os.path.join(dirpath, file)

                if os.path.isfile(path):

                    total_size += os.path.getsize(path)

    return f"{round(total_size / 1024 / 1024, 2)} MB"

# ====== DATABASE BACKUP ======
SQL_BACKUP_FOLDER = "backups"

def create_database_backup():

    os.makedirs(
        SQL_BACKUP_FOLDER,
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "AMS_Database_%Y%m%d_%H%M%S.sql"
    )

    backup_path = os.path.join(
        SQL_BACKUP_FOLDER,
        filename
    )

    # Change this path if MySQL is installed elsewhere
    MYSQLDUMP = Config.MYSQLDUMP_PATH

    command = [

        MYSQLDUMP,

        "-h", Config.MYSQL_HOST,

        "-u", Config.MYSQL_USER,

        f"-p{Config.MYSQL_PASSWORD}",

        Config.MYSQL_DB,

        "--result-file=" + backup_path

    ]

    subprocess.run(
        command,
        check=True
    )

    return backup_path

# ====== Restore Database =======
def restore_database(file):

    MYSQL = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".sql"
    )

    file.save(temp.name)
    temp.close()

    command = [
        MYSQL,
        "-h", Config.MYSQL_HOST,
        "-u", Config.MYSQL_USER,
        f"-p{Config.MYSQL_PASSWORD}",
        Config.MYSQL_DB
    ]

    print(command)

    with open(temp.name, "rb") as sql:

        result = subprocess.run(
            command,
            stdin=sql,
            capture_output=True,
            text=True
        )

    os.remove(temp.name)

    if result.returncode != 0:
        raise Exception(result.stderr)
    
# RESET DATABASE
def remove_folder(folder):

    if os.path.exists(folder):

        shutil.rmtree(folder)

        os.makedirs(folder)
        
def reset_database():

    cursor=mysql.connection.cursor()

    tables=[

        "applications",

        "candidates",

        "jobs",

        "gallery",

        "clients",

        "testimonials",

        "contact_messages"

    ]

    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    for table in tables:

        cursor.execute(
            f"TRUNCATE TABLE {table}"
        )

    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

    mysql.connection.commit()

    cursor.close()

    remove_folder(
        "static/uploads/candidates"
    )

    remove_folder(
        "static/gallery"
    )

    remove_folder(
        "static/clients"
    )

    remove_folder(
        "static/testimonials"
    )
    
def get_latest_backup():

    backups = []

    if os.path.exists(SQL_BACKUP_FOLDER):

        backups += [
            os.path.join(SQL_BACKUP_FOLDER, f)
            for f in os.listdir(SQL_BACKUP_FOLDER)
            if f.endswith(".sql")
        ]

    if os.path.exists(CV_FOLDER):

        backups += [
            os.path.join(CV_FOLDER, f)
            for f in os.listdir(CV_FOLDER)
            if f.endswith(".zip")
        ]

    if not backups:

        return "Never"

    latest = max(backups, key=os.path.getmtime)

    return datetime.fromtimestamp(
        os.path.getmtime(latest)
    ).strftime("%d %b %Y %I:%M %p")