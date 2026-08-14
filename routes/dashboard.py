from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    session,
    request,
    url_for,
    jsonify
)
from utils.decorators import login_required
from models.job_model import get_all_jobs
from services.job_service import generate_mandate_id
from models.application_model import get_all_applications, update_application_status, get_application_by_id, delete_application_by_id
from models.announcement_model import (get_announcement, update_announcement)
from models.candidate_model import get_all_candidates, update_candidate_status
from models.gallery_model import get_gallery
from models.client_model import get_clients
from models.contact_model import *
from models.testimonial_model import *
from models.dashboard_model import get_dashboard_counts
from services.maintenance_service import *
from services.notification_service import *

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    admin = session.get("admin")

    jobs = get_all_jobs()

    mandate_id = generate_mandate_id()
    
    applications = get_all_applications()
    
    announcement = get_announcement()
    
    candidates = get_all_candidates()
    
    gallery = get_gallery()
    
    clients = get_clients()
    
    testimonials = get_all_testimonials()
    
    stats = get_dashboard_counts()
    
    messages = get_all_messages()
    unread_count = unread_messages_count()

    return render_template(
        "dashboard.html",
        admin=admin,
        stats=stats,
        jobs=jobs,
        mandate_id=mandate_id,
        applications=applications,
        announcement=announcement,
        candidates=candidates,
        gallery=gallery,
        clients=clients,
        messages=messages,
        unread_count=unread_count,
        testimonials=testimonials,
        page="jobs"
    )
    
# ===============================
# Update Application Status
# ===============================
@dashboard_bp.route("/dashboard/applications/status", methods=["POST"])
@login_required
def update_status():

    application_id = request.form.get("application_id")
    status = request.form.get("status")

    update_application_status(application_id, status)

    return jsonify({
        "success": True
    })
    
@dashboard_bp.route("/dashboard/application/<int:id>")
@login_required
def application_details(id):

    application = get_application_by_id(id)

    if not application:
        return jsonify({"success": False})

    return jsonify(application)

@dashboard_bp.route("/dashboard/application/delete/<int:id>", methods=["POST"])
@login_required
def delete_application(id):

    delete_application_by_id(id)

    return jsonify({
        "success": True
    })
    
# ========= ANNOUNCEMENT ==========
@dashboard_bp.route("/dashboard/announcement", methods=["POST"])
@login_required
def save_announcement():

    message = request.form.get("message")

    admin = session.get("admin")
    admin_id = admin["id"]

    update_announcement(message, admin_id)

    notify_announcement_updated(
        session["admin"]["id"]
    )

    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/dashboard/candidate/status", methods=["POST"])
@login_required
def update_candidate_status_route():

    candidate_id = request.form.get("candidate_id")
    status = request.form.get("status")

    update_candidate_status(candidate_id, status)

    return jsonify(success=True)

@dashboard_bp.route("/dashboard/message/<int:id>")
@login_required
def message_details(id):

    message = get_message(id)

    mark_message_read(id)

    return jsonify(message)
