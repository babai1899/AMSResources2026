import os
import shutil

from dotenv import load_dotenv
from flask_mysqldb import MySQL
from flask_mail import Mail

load_dotenv()

mysql = MySQL()
mail = Mail()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

    # Automatically find mysqldump
    MYSQLDUMP_PATH = (
        os.getenv("MYSQLDUMP_PATH")
        or shutil.which("mysqldump")
        or r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
    )

    MYSQL_CURSORCLASS = "DictCursor"

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME