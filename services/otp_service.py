import random
import time


OTP_EXPIRY = 300          # 5 minutes
MAX_OTP_ATTEMPTS = 5


# ==========================================================
# Generate OTP
# ==========================================================

def generate_otp():
    """
    Generate a 6-digit OTP.
    """
    return str(random.randint(100000, 999999))


# ==========================================================
# Save OTP
# ==========================================================

def save_otp(session, otp):
    """
    Store registration OTP in Flask session.
    """

    session["registration_otp"] = str(otp)
    session["otp_created_at"] = int(time.time())
    session["otp_attempts"] = 0

    session.modified = True


# ==========================================================
# Verify OTP
# ==========================================================

def verify_otp(session, user_otp):
    """
    Verify registration OTP.

    Returns:
        (True, message)
        (False, message)
    """

    # Get stored OTP
    stored_otp = session.get("registration_otp")

    created_at = session.get(
        "otp_created_at"
    )

    # ------------------------------------------
    # OTP does not exist
    # ------------------------------------------

    if stored_otp is None:

        return (
            False,
            "OTP session expired. Please request a new OTP."
        )


    # ------------------------------------------
    # Creation timestamp missing
    # ------------------------------------------

    if created_at is None:

        session.pop(
            "registration_otp",
            None
        )

        session.pop(
            "otp_created_at",
            None
        )

        session.pop(
            "otp_attempts",
            None
        )

        return (
            False,
            "OTP session expired. Please request a new OTP."
        )


    # ------------------------------------------
    # Expiry check
    # ------------------------------------------

    elapsed = (
        int(time.time())
        - int(created_at)
    )

    if elapsed >= OTP_EXPIRY:

        session.pop(
            "registration_otp",
            None
        )

        session.pop(
            "otp_created_at",
            None
        )

        session.pop(
            "otp_attempts",
            None
        )

        session.modified = True

        return (
            False,
            "OTP expired. Please request a new OTP."
        )


    # ------------------------------------------
    # Attempt limit
    # ------------------------------------------

    attempts = int(
        session.get(
            "otp_attempts",
            0
        )
    )

    if attempts >= MAX_OTP_ATTEMPTS:

        return (
            False,
            "Too many incorrect attempts. Please request a new OTP."
        )


    # ------------------------------------------
    # Clean submitted OTP
    # ------------------------------------------

    submitted_otp = str(
        user_otp or ""
    ).strip()

    stored_otp = str(
        stored_otp
    ).strip()


    # ------------------------------------------
    # Empty OTP
    # ------------------------------------------

    if not submitted_otp:

        return (
            False,
            "Please enter the OTP."
        )


    # ------------------------------------------
    # OTP comparison
    # ------------------------------------------

    if submitted_otp != stored_otp:

        session["otp_attempts"] = (
            attempts + 1
        )

        session.modified = True

        remaining = (
            MAX_OTP_ATTEMPTS
            - attempts
            - 1
        )

        if remaining <= 0:

            return (
                False,
                "Too many incorrect attempts. Please request a new OTP."
            )

        return (
            False,
            f"Incorrect OTP. {remaining} attempt{'s' if remaining != 1 else ''} remaining."
        )


    # ------------------------------------------
    # SUCCESS
    # ------------------------------------------

    session.pop(
        "registration_otp",
        None
    )

    session.pop(
        "otp_created_at",
        None
    )

    session.pop(
        "otp_attempts",
        None
    )

    session.modified = True

    return (
        True,
        "OTP verified successfully."
    )