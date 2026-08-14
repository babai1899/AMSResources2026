from flask import Blueprint
from flask import request
from flask import jsonify
from flask import render_template, session

from utils.decorators import login_required

from services.upload_service import save_testimonial_image

from models.testimonial_model import *
from services.notification_service import *

testimonial_bp = Blueprint("testimonial", __name__)

#====== UPLOAD ======
@testimonial_bp.route("/dashboard/testimonial/upload", methods=["POST"])
@login_required
def upload_testimonial():

    try:

        file = request.files["photo"]

        filename = save_testimonial_image(file)

        full_name = request.form["full_name"]

        add_testimonial(
            full_name,
            request.form["designation"],
            request.form["message"],
            filename
        )

        notify_testimonial_added(
            full_name,
            session["admin"]["id"]
        )

        return jsonify(success=True)

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify(
            success=False,
            message=str(e)
        ), 500

# ====== SINGLE ======
@testimonial_bp.route("/dashboard/testimonial/<int:id>")
@login_required
def single(id):

    return jsonify(
        get_testimonial(id)
    )


# ====== DELETE ======
@testimonial_bp.route("/dashboard/testimonial/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    testimonial = get_testimonial(id)

    if testimonial:

        notify_testimonial_deleted(
            testimonial["full_name"],
            session["admin"]["id"]
        )

    delete_testimonial(id)

    return jsonify(success=True)


# ====== TOGGLE STATUS ======
@testimonial_bp.route("/dashboard/testimonial/status/<int:id>", methods=["POST"])
@login_required
def status(id):

    toggle_status(id)

    testimonial = get_testimonial(id)

    if testimonial:

        notify_system(
            f'Testimonial status changed for "{testimonial["full_name"]}".'
        )

    return jsonify(success=True)


# ====== UPDATE ======
@testimonial_bp.route("/dashboard/testimonial/update/<int:id>", methods=["POST"])
@login_required
def update(id):

    photo = None

    if "photo" in request.files and request.files["photo"].filename != "":

        photo = save_testimonial_image(
            request.files["photo"]
        )

    full_name = request.form["full_name"]

    update_testimonial(
        id,
        full_name,
        request.form["designation"],
        request.form["message"],
        photo
    )

    notify_testimonial_updated(
        full_name,
        session["admin"]["id"]
    )

    return jsonify(success=True)

@testimonial_bp.route("/dashboard/testimonials")
@login_required
def list_testimonials():

    testimonials = get_all_testimonials()

    return render_template(
        "dashboard/partials/_testimonial_cards.html",
        testimonials=testimonials
    )