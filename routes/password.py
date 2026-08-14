from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session

from werkzeug.security import generate_password_hash

from utils.decorators import login_required

from models.password_model import *

from services.password_service import *

from services.notification_service import *

password_bp = Blueprint("password", __name__)

# ====== Send OTP ======
@password_bp.route("/dashboard/password/send-otp", methods=["POST"])
@login_required
def send_password_otp():

    admin_session = session.get("admin")

    if not admin_session:
        return jsonify(
            success=False,
            message="Session expired. Please login again."
        )

    email = admin_session["email"]

    admin = get_admin_by_email(email)

    if not admin:
        return jsonify(
            success=False,
            message="User not found."
        )

    # Store email for later use
    session["password_reset_email"] = email

    # Reset verification flag every time a new OTP is sent
    session["password_otp_verified"] = False

    session.modified = True

    save_password_otp(email)

    return jsonify(
        success=True,
        message="OTP sent successfully."
    )
        
# ====== Verify OTP ======
@password_bp.route("/dashboard/password/verify-otp", methods=["POST"])
@login_required
def verify_otp():

    otp = request.form.get("otp")

    result = verify_password_otp(otp)

    print("verify_password_otp() returned:", result)

    if result:

        session["password_otp_verified"] = True
        session.modified = True

        print("OTP VERIFIED SUCCESS")
        print(dict(session))

        return jsonify(
            success=True,
            message="OTP verified successfully."
        )

    return jsonify(
        success=False,
        message="Invalid or expired OTP."
    )
    
# ====== Change Password ======
@password_bp.route("/dashboard/password/change", methods=["POST"])
@login_required
def change_password():

    if not session.get("password_otp_verified"):

        return jsonify(
            success=False,
            message="Please verify OTP first."
        )

    password = request.form.get("password")
    confirm = request.form.get("confirm")

    # Confirm password check
    if password != confirm:

        return jsonify(
            success=False,
            message="Passwords do not match."
        )

    # ==========================
    # PASSWORD VALIDATION START
    # ==========================

    import re

    if len(password) < 8:
        return jsonify(
            success=False,
            message="Password must be at least 8 characters."
        )

    if not re.search(r"[A-Z]", password):
        return jsonify(
            success=False,
            message="Password must contain an uppercase letter."
        )

    if not re.search(r"[0-9]", password):
        return jsonify(
            success=False,
            message="Password must contain a number."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\];'`~]", password):
        return jsonify(
            success=False,
            message="Password must contain a special character."
        )

    # ==========================
    # PASSWORD VALIDATION END
    # ==========================

    admin = get_admin_by_email(
        session["password_reset_email"]
    )

    hashed = generate_password_hash(password)

    update_admin_password(
        admin["id"],
        hashed
    )

    clear_password_session()

    session.clear()
    
    notify_password_changed(
        session["admin"]["username"]
    )

    return jsonify(
        success=True,
        message="Password changed successfully. Please login again."
    )