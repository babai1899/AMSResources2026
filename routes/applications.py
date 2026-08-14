# Apply, Biodata
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.job_model import get_job_by_mandate
from models.application_model import save_application
from models.candidate_model import save_candidate
from services.notification_service import *

applications_bp = Blueprint("applications", __name__)

# ===============================
# Apply Page
# ===============================
@applications_bp.route("/apply/<mandate_id>")
def apply(mandate_id):

    job = get_job_by_mandate(mandate_id)
    
    print(job)      # Debug

    return render_template(
        "apply.html",
        job=job
    )

# ========= SUBMIT APPLICATION =========
@applications_bp.route("/apply/<mandate_id>", methods=["POST"])
def submit_application(mandate_id):

    job = get_job_by_mandate(mandate_id)

    if not job:
        flash("Job not found.", "danger")
        return redirect(url_for("jobs.current_openings"))

    save_application(
        request.form,
        request.files,
        job
    )
    
    notify_application_received(
        request.form.get("full_name"),
        job["designation"]
    )

    flash("Application submitted successfully.", "application_success")

    return redirect(url_for("jobs.current_openings"))

# ===============================
# Biodata Page
# ===============================
@applications_bp.route("/fill-biodata", methods=["GET", "POST"])
def fill_biodata():

    if request.method == "POST":

        save_candidate(
            request.form,
            request.files
        )
        
        notify_biodata_received(
            request.form.get("full_name")
        )

        flash("CV uploaded successfully.", "cv_success")

        return redirect(url_for("applications.fill_biodata"))

    return render_template("fill-biodata.html")