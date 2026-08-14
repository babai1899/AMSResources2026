from flask import Blueprint, render_template
from models.announcement_model import get_announcement
from models.gallery_model import get_public_gallery
from models.client_model import get_clients
from models.testimonial_model import get_active_testimonials

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    
    announcement = get_announcement()
    clients = get_clients()
    testimonials = get_active_testimonials()
    
    return render_template(
        "index.html",
        announcement=announcement,
        clients=clients,
        testimonials=testimonials
        )

@home_bp.route("/about")
def about():
    return render_template("about.html")

@home_bp.route("/gallery")
def gallery():
    
    gallery = get_public_gallery()
    
    return render_template("gallery.html", gallery=gallery)

@home_bp.route("/recruitment")
def recruitment():
    return render_template("recruitment.html")

@home_bp.route("/clients")
def clients():
    
    clients = get_clients()
    
    return render_template("clients.html", clients=clients)

@home_bp.route("/contact")
def contact():
    return render_template("contact.html")

@home_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@home_bp.route("/terms")
def terms():
    return render_template("terms.html")