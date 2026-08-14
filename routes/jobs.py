from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from models.job_model import *
from services.job_service import generate_mandate_id
from models.job_model import *
from utils.decorators import login_required
from services.notification_service import *

jobs_bp = Blueprint("jobs", __name__)
    
# ====== ADD JOB ======
@jobs_bp.route("/dashboard/jobs/add", methods=["POST"])
def add_new_job():

    data = {

        "mandate_id": generate_mandate_id(),
        "employer": request.form["employer"],
        "designation": request.form["designation"],
        "industry": request.form["industry"],
        "experience": request.form["experience"],
        "location": request.form["location"],
        "specifications": request.form["specifications"],
        "status": "Active",
        "created_by": session["admin"]["id"]

    }

    add_job(data)

    # Create notification
    notify_job_created(
        data["designation"],
        session["admin"]["id"]
    )

    return redirect(url_for("dashboard.dashboard"))

@jobs_bp.route("/dashboard/jobs/delete/<int:job_id>", methods=["POST"])
def delete(job_id):

    job = get_job_by_id(job_id)   # Fetch job before deleting

    delete_job(job_id)

    notify_job_deleted(
        job["designation"],
        session["admin"]["id"]
    )

    return jsonify({
        "success": True
    })

# ====== CLOSE JOB ======
@jobs_bp.route("/dashboard/jobs/close/<int:id>", methods=["POST"])
@login_required
def close(id):

    designation = get_job_by_id(id)   # Fetch before closing

    close_job(id)

    notify_job_closed(
        designation,
        session["admin"]["id"]
    )

    return jsonify(
        success=True,
        message="Job closed."
    )

@jobs_bp.route("/current-openings")
def current_openings():

    jobs = get_active_jobs()

    return render_template(
        "current-openings.html",
        jobs=jobs
    )

# Update Job Status
@jobs_bp.route("/dashboard/jobs/status", methods=["POST"])
@login_required
def change_job_status():

    job_id = request.form.get("job_id")
    status = request.form.get("status")

    job = get_job(job_id)      # Fetch current job details

    update_job_status(job_id, status)

    if status == "Active":

        notify_job_activated(
            job["designation"],
            session["admin"]["id"]
        )

    elif status == "Closed":

        notify_job_closed(
            job["designation"],
            session["admin"]["id"]
        )

    return jsonify({
        "success": True
    })

# ====== ACTIVATE JOB ======
@jobs_bp.route("/dashboard/jobs/activate/<int:id>", methods=["POST"])
@login_required
def activate(id):

    activate_job(id)

    return jsonify(

        success=True,

        message="Job activated."

    )

# ====== LOAD JOBS ROUTE ======
@jobs_bp.route("/dashboard/jobs/list")
@login_required
def jobs_list():

    jobs = get_all_jobs()

    return jsonify(

        success=True,

        jobs=jobs

    )
    