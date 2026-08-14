from flask import Blueprint, request, redirect, url_for, flash, session
from models.candidate_model import save_candidate

candidates_bp = Blueprint("candidates", __name__)

@candidates_bp.route("/dashboard/candidates/upload", methods=["POST"])
def upload_candidate():

    save_candidate(
        request.form,
        request.files
    )

    flash("Candidate uploaded successfully.", "success")

    return redirect(url_for("dashboard.dashboard"))