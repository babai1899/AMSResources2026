from flask import Blueprint, request, redirect, url_for, session

from utils.decorators import login_required

from models.client_model import (
    add_client,
    delete_client,
    get_client
)

from services.notification_service import *

clients_bp = Blueprint("clients", __name__)

@clients_bp.route("/dashboard/client/upload", methods=["POST"])
@login_required
def upload_client():

    client_name = request.form["client_name"]
    country = request.form["country"]

    logo = request.files.get("logo")

    admin = session["admin"]

    add_client(
        client_name,
        country,
        logo,
        admin["id"]
    )
    
    notify_client_added(
        client_name,
        session["admin"]["id"]
    )

    return redirect(url_for("dashboard.dashboard"))

@clients_bp.route("/dashboard/client/delete/<int:id>", methods=["POST"])
@login_required
def remove_client(id):

    client = get_client(id)

    if client:

        notify_client_deleted(
            client["client_name"],
            session["admin"]["id"]
        )

    delete_client(id)

    return redirect(url_for("dashboard.dashboard"))