from flask import Blueprint                     # Login, Register, Logout
from flask import (render_template, request, redirect, url_for, flash, session, jsonify)
from flask import request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from configure import mysql
from services.otp_service import generate_otp, save_otp
from services.email_service import send_registration_otp
from models.admin_model import admin_exists

auth_bp = Blueprint("auth", __name__)

# --------------------------
# ADMIN
# --------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")

    # POST request
    title = request.form.get("title")
    first_name = request.form.get("first_name")
    surname = request.form.get("surname")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    role = request.form.get("role")

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("auth.register"))
    
    # -----------------------------
    # Generate OTP
    # -----------------------------
    otp = generate_otp()

    save_otp(session, otp)

    # Store user data temporarily
    session["registration_data"] = {
        "title": title,
        "first_name": first_name,
        "surname": surname,
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    # -----------------------------
    # Send OTP Email
    # -----------------------------
    send_registration_otp(email, otp)

    flash("Registration successful.", "success")

    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and Password are required.", "danger")
        return redirect(url_for("auth.login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            first_name,
            surname,
            username,
            email,
            password,
            role
        FROM admins
        WHERE username=%s
    """, (username,))

    user = cursor.fetchone()
    cursor.close()

    if not user:
        flash("Invalid Username or Password.", "danger")
        return redirect(url_for("auth.login"))

    if not check_password_hash(user["password"], password):
        flash("Invalid Username or Password.", "danger")
        return redirect(url_for("auth.login"))

    # -------------------------
    # Login Successful
    # -------------------------

    session["admin"] = {
        "id": user["id"],
        "title": user["title"],
        "first_name": user["first_name"],
        "surname": user["surname"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

    flash("Login Successful.", "success")

    return redirect(url_for("dashboard.dashboard"))

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))