from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify

from utils.decorators import login_required

from models.gallery_model import add_gallery_image, delete_gallery_image, get_gallery_image
from services.notification_service import *

gallery_bp = Blueprint("gallery",__name__)

@gallery_bp.route("/dashboard/gallery/upload", methods=["POST"])
@login_required
def upload_gallery():

    title = request.form["title"]

    media = request.files.get("media")

    if not media:
        return jsonify({
            "success": False,
            "message": "No file selected."
        })

    filename = media.filename

    admin = session["admin"]

    add_gallery_image(
        title,
        media,
        admin["id"]
    )

    notify_gallery_uploaded(
        filename,
        admin["id"]
    )

    return redirect(url_for("dashboard.dashboard"))


@gallery_bp.route("/dashboard/gallery/delete/<int:id>", methods=["POST"])
@login_required
def delete_gallery(id):

    try:

        image = get_gallery_image(id)

        if not image:
            return jsonify({
                "success": False,
                "message": "Image not found."
            })

        filename = image["title"] or image["filename"]

        delete_gallery_image(id)

        notify_gallery_deleted(
            filename,
            session["admin"]["id"]
        )

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("DELETE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500