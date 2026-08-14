from flask import Flask
from configure import Config, mysql, mail
from flask_mail import Message
from flask import session
from socketio_instance import socketio
import socket_events
from models.admin_model import get_admin_by_id

from routes.home import home_bp
from routes.auth import auth_bp
from routes.otp import otp_bp
from routes.jobs import jobs_bp
from routes.gallery import gallery_bp
from routes.contact import contact_bp
from routes.dashboard import dashboard_bp
from routes.applications import applications_bp
from routes.clients import clients_bp
from routes.testimonial import testimonial_bp
from routes.password import password_bp
from routes.maintenance import maintenance_bp
from routes.notification import notification_bp

app = Flask(__name__)

app.config.from_object(Config)

mysql.init_app(app)
mail.init_app(app)
socketio.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(otp_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(testimonial_bp)
app.register_blueprint(password_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(notification_bp)

print(app.url_map)

@app.context_processor
def inject_admin():

    admin = None

    if "admin_id" in session:
        admin = get_admin_by_id(session["admin_id"])

    return dict(admin=admin)


if __name__ == "__main__":
    socketio.run(app, debug=True)