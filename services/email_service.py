from flask_mail import Message
from configure import mail

# ---------------------------
# SEND REGISTRATION OTP
# ---------------------------
def send_registration_otp(email, otp):

    msg = Message(
        subject="AMS Resources - Email Verification",
        recipients=[email]
    )

    msg.body = f"""
Dear User,

Your One-Time Password (OTP) for AMS Resources registration is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this registration, please ignore this email.

Regards,

AMS Resources
"""

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print("OTP Mail Error:", e)
        return False


# ---------------------------
# SEND GENERAL EMAIL
# ---------------------------
def send_email(to, subject, body):

    try:
        msg = Message(
            subject=subject,
            recipients=[to]
        )

        msg.body = body

        mail.send(msg)

        print("Mail Sent Successfully")

    except Exception as e:
        print("MAIL ERROR:", repr(e))
        raise