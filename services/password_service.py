import random
from datetime import datetime, timedelta

from flask import session

from services.email_service import send_email


# -----------------------------
# Generate OTP
# -----------------------------
def generate_password_otp():

    return str(random.randint(100000,999999))


# -----------------------------
# Save OTP
# -----------------------------
def save_password_otp(email):

    otp = generate_password_otp()

    session["password_reset_email"] = email
    session["password_reset_otp"] = otp
    session["password_reset_expiry"] = (
        datetime.now() + timedelta(minutes=5)
    ).timestamp()
    
    session["password_otp_verified"] = False
    session.modified = True

    send_email(

        to=email,

        subject="AMS Resources - Password Reset OTP",

        body=f"""
    Dear User,

    Your OTP for changing your password is

    {otp}

    This OTP is valid for 5 minutes.

    Regards,

    AMS Resources
    """
        )
    
    print("OTP email sent")

    return otp


# -----------------------------
# Verify OTP
# -----------------------------
def verify_password_otp(user_otp):

    otp = session.get("password_reset_otp")
    expiry = session.get("password_reset_expiry")

    if not otp:
        return False

    if datetime.now().timestamp() > expiry:
        return False

    if otp != user_otp:
        return False

    session["password_otp_verified"] = True

    # OTP cannot be reused
    session.pop("password_reset_otp", None)
    session.pop("password_reset_expiry", None)

    session.modified = True

    return True

# -----------------------------
# Clear OTP
# -----------------------------
def clear_password_session():

    session.pop("password_reset_email", None)
    session.pop("password_reset_otp", None)
    session.pop("password_reset_expiry", None)
    session.pop("password_otp_verified", None)