# OTP Verification
from flask import Blueprint, request, session, jsonify, url_for

from werkzeug.security import generate_password_hash

from configure import mysql

from services.otp_service import (
    verify_otp,
    generate_otp,
    save_otp
)

from services.email_service import send_registration_otp

from models.admin_model import insert_admin


otp_bp = Blueprint("otp", __name__)


# ======================================
# VERIFY REGISTRATION OTP
# ======================================

@otp_bp.route("/verify-otp", methods=["POST"])
def verify_registration_otp():

    user_otp = request.form.get(
        "otp",
        ""
    ).strip()

    status, message = verify_otp(
        session,
        user_otp
    )

    if not status:

        return jsonify({
            "success": False,
            "message": message
        })


    # -----------------------------
    # Get registration data
    # -----------------------------

    registration = session.get(
        "registration_data"
    )

    if not registration:

        return jsonify({
            "success": False,
            "message": "Registration session expired."
        })


    cursor = mysql.connection.cursor()


    # -----------------------------
    # Check duplicate username/email
    # -----------------------------

    cursor.execute("""
        SELECT id
        FROM admins
        WHERE username=%s
           OR email=%s
    """, (
        registration["username"],
        registration["email"]
    ))


    if cursor.fetchone():

        cursor.close()

        return jsonify({
            "success": False,
            "message": "Username or Email already exists."
        })


    # -----------------------------
    # Hash password
    # -----------------------------

    hashed_password = generate_password_hash(
        registration["password"]
    )


    # -----------------------------
    # Insert user
    # -----------------------------

    cursor.execute("""
        INSERT INTO admins
        (
            title,
            first_name,
            surname,
            username,
            email,
            password,
            role
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
    """, (

        registration["title"],
        registration["first_name"],
        registration["surname"],
        registration["username"],
        registration["email"],
        hashed_password,
        registration["role"]

    ))


    mysql.connection.commit()

    cursor.close()


    # -----------------------------
    # Clear registration session
    # -----------------------------

    session.pop(
        "registration_data",
        None
    )


    return jsonify({
        "success": True,
        "message": "Registration completed successfully.",
        "redirect": url_for("auth.login")
    })

# ======================================
# RESEND OTP
# ======================================

@otp_bp.route("/resend-otp", methods=["POST"])
def resend_registration_otp():

    registration = session.get("registration_data")

    if not registration:

        return jsonify({
            "success": False,
            "message": "Registration session expired."
        })

    otp = generate_otp()

    save_otp(session, otp)

    send_registration_otp(
        registration["email"],
        otp
    )

    return jsonify({
        "success": True,
        "message": "OTP has been sent again."
    })