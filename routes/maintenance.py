import os
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash

from utils.decorators import login_required
from models.admin_model import get_admin_by_email

from flask import send_file

from services.maintenance_service import *

from services.notification_service import *

maintenance_bp = Blueprint("maintenance", __name__)


@maintenance_bp.route("/dashboard/maintenance/verify", methods=["POST"])
@login_required
def verify_admin_password():

    password = request.form.get("password")

    admin_session = session.get("admin")

    if not admin_session:

        return jsonify(
            success=False,
            message="Session expired."
        )

    admin = get_admin_by_email(
        admin_session["email"]
    )

    if not admin:

        return jsonify(
            success=False,
            message="Administrator not found."
        )

    if not check_password_hash(
        admin["password"],
        password
    ):

        return jsonify(
            success=False,
            message="Incorrect administrator password."
        )

    session["maintenance_verified"] = True
    session.modified = True
    
    print("VERIFY ROUTE")
    print(dict(session))

    return jsonify(
        success=True
    )
    
# ====== DOWNLOAD CV BACKUP =======
@maintenance_bp.route(
    "/dashboard/maintenance/download-cv",
    methods=["POST"]
)
@login_required
def download_cv_backup():

    if not session.get("maintenance_verified"):

        return jsonify(
            success=False,
            message="Administrator verification required."
        ),403

    try:

        zip_file = create_candidate_backup()

        session.pop("maintenance_verified", None)
        
        notify_candidate_backup(
            session["admin"]["id"]
        )

        return send_file(
            zip_file,
            as_attachment=True,
            download_name="AMS_Candidate_Backup.zip"
        )

    except Exception as e:

        return jsonify(
            success=False,
            message=str(e)
        ),500
        
# DATABASE BACKUP
@maintenance_bp.route("/dashboard/maintenance/download-db", methods=["POST"])
@login_required
def download_database():

    if not session.get("maintenance_verified"):
        print("Maintenance verification failed")
        return jsonify(
            success=False,
            message="Administrator verification required."
        ), 403

    try:

        backup = create_database_backup()
        
        notify_database_backup(
            session["admin"]["id"]
        )

        session.pop("maintenance_verified", None)

        return send_file(
            backup,
            as_attachment=True,
            download_name="AMS_Database_Backup.sql"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify(
            success=False,
            message=str(e)
        ), 500
        
# ====== RESTORE DATABASE ======
@maintenance_bp.route(
    "/dashboard/maintenance/restore",
    methods=["POST"]
)
@login_required
def restore_database_route():

    if not session.get("maintenance_verified"):

        return jsonify(
            success=False,
            message="Administrator verification required."
        ),403

    if "sql_file" not in request.files:

        return jsonify(
            success=False,
            message="Please choose a SQL file."
        )

    file=request.files["sql_file"]

    if file.filename=="":

        return jsonify(
            success=False,
            message="No file selected."
        )

    try:

        restore_database(file)
        
        notify_database_restore(
            session["admin"]["id"]
        )

        session.pop(
            "maintenance_verified",
            None
        )

        return jsonify(
            success=True,
            message="Database restored successfully."
        )

    except Exception as e:

        return jsonify(
            success=False,
            message=str(e)
        ),500
        
# ====== RESET DATABASE ======
@maintenance_bp.route("/dashboard/maintenance/reset", methods=["POST"])
@login_required
def reset_system():

    if not session.get("maintenance_verified"):

        return jsonify(
            success=False,
            message="Administrator verification required."
        ),403

    if request.form.get("confirm")!="DELETE":

        return jsonify(
            success=False,
            message="Type DELETE to continue."
        )

    try:

        reset_database()
        
        notify_database_reset(
            session["admin"]["id"]
        )

        session.pop(
            "maintenance_verified",
            None
        )

        return jsonify(

            success=True,

            message="System reset successfully."

        )

    except Exception as e:

        return jsonify(

            success=False,

            message=str(e)

        ),500
        
# ===== Stats =======
@maintenance_bp.route("/dashboard/maintenance/stats")
@login_required
def maintenance_stats():

    try:

        data = get_maintenance_stats()

        return jsonify(
            success=True,
            data=data
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify(
            success=False,
            message=str(e)
        ),500