from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from flask import session
from utils.decorators import login_required

from models.contact_model import (
    add_contact,
    get_message,
    mark_message_read,
    mark_as_replied,
    archive_message,
    delete_message,
    mark_message_unread,
    get_all_messages,
    get_messages_by_status,
    unread_messages_count
)
from services.email_service import send_email

from services.notification_service import *

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["POST"])
def submit_contact():

    full_name = request.form.get("full_name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    add_contact(
        full_name,
        email,
        subject,
        message
    )

    notify_message_received(
        full_name,
        subject
    )

    flash("Message sent successfully.", "contact_success")

    return redirect(url_for("home.home"))


@contact_bp.route("/dashboard/message/reply", methods=["POST"])
@login_required
def reply_message():

    try:
        message_id = request.form.get("message_id")
        reply = request.form.get("reply")

        message = get_message(message_id)

        send_email(
            to=message["email"],
            subject="Re: " + (message["subject"] or "Your Inquiry"),
            body=f"""
Dear {message['full_name']},

{reply}

-----------------------------------------

Regards,

AMS Resources
Nalini Apartment
172/1 Bidhanpally
Kolkata - 700084

Phone: 03324100189
Email: amsmanpower25@gmail.com
"""
        )

        mark_as_replied(message_id)

        notify_message_replied(
            message["full_name"],
            message["subject"],
            session["admin"]["id"]
        )

        flash("Reply sent successfully.", "success")

        return redirect(url_for("dashboard.dashboard"))

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@contact_bp.route("/dashboard/message/<int:id>")
@login_required
def get_single_message(id):

    message = get_message(id)

    mark_message_read(id)

    return jsonify(message)

@contact_bp.route("/dashboard/message/unread/<int:id>", methods=["POST"])
@login_required
def mark_unread(id):

    message = get_message(id)

    mark_message_unread(id)

    notify_system(
        f'Message from "{message["full_name"]}" marked as unread.'
    )

    return jsonify(success=True)

@contact_bp.route("/dashboard/message/archive/<int:id>", methods=["POST"])
@login_required
def archive(id):

    message = get_message(id)

    archive_message(id)

    notify_system(
        f'Message from "{message["full_name"]}" archived.'
    )

    return jsonify(success=True)

@contact_bp.route("/dashboard/message/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    message = get_message(id)

    notify_message_deleted(
        message["full_name"],
        message["subject"],
        session["admin"]["id"]
    )

    delete_message(id)

    return jsonify(success=True)
    
@contact_bp.route("/dashboard/messages/filter/<status>")
@login_required
def filter_messages(status):

    if status == "all":
        messages = get_all_messages()
    elif status == "unread":
        messages = get_messages_by_status("Unread")
    elif status == "archive":
        messages = get_messages_by_status("Archived")
    else:
        messages = []

    return jsonify(messages)

@contact_bp.route("/dashboard/messages/unread-count")
@login_required
def unread_count():

    return jsonify({
        "total": unread_messages_count()
    })