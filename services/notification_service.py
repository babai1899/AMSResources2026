from models.notification_model import create_notification
from socketio_instance import socketio


# ==========================================================
# Notification Categories
# ==========================================================

NOTIFICATION_TYPES = {

    "jobs": {
        "icon": "fa-briefcase",
        "color": "emerald",
        "link": "/dashboard/jobs"
    },
    
    "application": {
        "icon": "fa-file-alt",
        "color": "emerald",
        "link": "/dashboard/applications"
    },

    "candidate": {
        "icon": "fa-user",
        "color": "blue",
        "link": "/dashboard/candidates"
    },

    "users": {
        "icon": "fa-users",
        "color": "blue"
        ,
        "link": "/dashboard/users"
    },

    "gallery": {
        "icon": "fa-images",
        "color": "amber",
        "link": "/dashboard/gallery"
    },

    "testimonial": {
        "icon": "fa-comments",
        "color": "rose",
        "link": "/dashboard/testimonials"
    },

    "maintenance": {
        "icon": "fa-tools",
        "color": "amber",
        "link": "/dashboard/maintenance"
    },
    
    "company": {
        "icon": "fa-building",
        "color": "blue",
        "link": "/dashboard/companies"
    },
    
    "recruiter": {
        "icon": "fa-user-tie",
        "color": "indigo",
        "link": "/dashboard/recruiters"
    },
    
    "clients": {
        "icon": "fa-building",
        "color": "blue",
        "link": "/dashboard/clients"
    },
    
    "messages": {
        "icon": "fa-envelope",
        "color": "amber",
        "link": "/dashboard/messages"
    },
    
    "mail": {
        "icon": "fa-paper-plane",
        "color": "sky",
        "link": "/dashboard/mail"
    },

    "security": {
        "icon": "fa-shield-alt",
        "color": "red",
        "link": "/dashboard/settings"
    },

    "system": {
        "icon": "fa-server",
        "color": "slate",
        "link": "/dashboard"
    }

}


# ==========================================================
# Core Notification Function
# ==========================================================

def add_notification(

    category,

    action,

    title,

    message,

    priority="normal",

    created_by=None

):
    
    print("=" * 50)
    print("add_notification() called")
    print(category, action, title)

    config = NOTIFICATION_TYPES.get(

        category,

        NOTIFICATION_TYPES["system"]

    )

    create_notification(

        category=category,

        action=action,

        title=title,

        message=message,

        icon=config["icon"],

        color=config["color"],

        priority=priority,

        link=config["link"],

        created_by=created_by

    )
    
    notification = {

        "category": category,

        "action": action,

        "title": title,

        "message": message,

        "icon": config["icon"],

        "color": config["color"],

        "priority": priority,

        "link": config["link"]

    }

    socketio.emit(

        "new_notification",

        notification,

        namespace="/notifications"

    )


# ==========================================================
# JOBS
# ==========================================================

def notify_job_created(job, user=None):
    
    print("notify_job_created() called")

    add_notification(

        "jobs",

        "created",

        "New Job Added",

        f"{job} has been added.",

        created_by=user

    )

def notify_job_activated(job, user=None):

    add_notification(

        "jobs",

        "activated",

        "Job Activated",

        f"{job} has been activated.",

        created_by=user

    )

def notify_job_updated(job, user=None):

    add_notification(

        "jobs",

        "updated",

        "Job Updated",

        f"{job} has been updated.",

        created_by=user

    )


def notify_job_closed(job, user=None):

    add_notification(

        "jobs",

        "closed",

        "Job Closed",

        f"{job} has been closed.",

        created_by=user

    )


def notify_job_deleted(job, user=None):

    add_notification(

        "jobs",

        "deleted",

        "Job Deleted",

        f"{job} has been removed.",

        priority="high",

        created_by=user

    )

# ==========================================================
# APPLICATIONS
# ==========================================================

def notify_application_received(candidate, job=None):

    message = f"{candidate} applied."

    if job:
        message = f"{candidate} applied for {job}."

    add_notification(

        "application",

        "received",

        "New Job Application",

        message

    )


def notify_biodata_received(candidate):

    add_notification(

        "candidate",

        "biodata",

        "New Biodata Submitted",

        f"{candidate} submitted biodata."

    )

# ==========================================================
# CANDIDATES
# ==========================================================

def notify_candidate_added(name, user=None):

    add_notification(

        "candidate",

        "created",

        "Candidate Added",

        f"{name} has been registered.",

        created_by=user

    )


def notify_candidate_deleted(name, user=None):

    add_notification(

        "candidate",

        "deleted",

        "Candidate Deleted",

        f"{name} has been removed.",

        priority="high",

        created_by=user

    )

def notify_candidate_updated(name, user=None):

    add_notification(
        "candidate",
        "updated",
        "Candidate Updated",
        f"{name} profile updated.",
        created_by=user
    )


def notify_candidate_selected(name, user=None):

    add_notification(
        "candidate",
        "selected",
        "Candidate Selected",
        f"{name} selected for interview.",
        created_by=user
    )


def notify_candidate_rejected(name, user=None):

    add_notification(
        "candidate",
        "rejected",
        "Candidate Rejected",
        f"{name} application rejected.",
        created_by=user
    )

# ==========================================================
# USERS
# ==========================================================

def notify_user_created(username, user=None):

    add_notification(

        "users",

        "created",

        "New User",

        f"{username} account created.",

        created_by=user

    )


def notify_user_deleted(username, user=None):

    add_notification(

        "users",

        "deleted",

        "User Removed",

        f"{username} account deleted.",

        priority="high",

        created_by=user

    )
    
def notify_user_updated(username, user=None):

    add_notification(
        "users",
        "updated",
        "User Updated",
        f"{username} profile updated.",
        created_by=user
    )


# ==========================================================
# GALLERY
# ==========================================================

def notify_gallery_uploaded(filename, user=None):

    add_notification(

        "gallery",

        "uploaded",

        "New Gallery Item",

        f'"{filename}" has been uploaded.',

        created_by=user

    )


def notify_gallery_updated(filename, user=None):

    add_notification(

        "gallery",

        "updated",

        "Gallery Item Updated",

        f'"{filename}" has been updated.',

        created_by=user

    )


def notify_gallery_deleted(filename, user=None):

    add_notification(

        "gallery",

        "deleted",

        "Gallery Item Deleted",

        f'"{filename}" has been deleted.',

        priority="high",

        created_by=user

    )


# ==========================================================
# ANNOUNCEMENTS
# ==========================================================

def notify_announcement_updated(title, user=None):

    add_notification(

        "system",

        "announcement_updated",

        "Announcement Updated",

        f'Announcement has been updated.',

        created_by=user

    )


# ==========================================================
# CLIENTS
# ==========================================================

def notify_client_added(name, user=None):

    add_notification(

        "users",

        "client_created",

        "New Client Added",

        f'"{name}" has been added.',

        created_by=user

    )


def notify_client_updated(name, user=None):

    add_notification(

        "users",

        "client_updated",

        "Client Updated",

        f'"{name}" has been updated.',

        created_by=user

    )


def notify_client_deleted(name, user=None):

    add_notification(

        "users",

        "client_deleted",

        "Client Deleted",

        f'"{name}" has been deleted.',

        priority="high",

        created_by=user

    )
    

# ==========================================================
# TESTIMONIALS
# ==========================================================

def notify_testimonial_added(name, user=None):

    add_notification(

        "testimonial",

        "created",

        "New Testimonial",

        f'A new testimonial from {name}.',

        created_by=user

    )


def notify_testimonial_updated(name, user=None):

    add_notification(

        "testimonial",

        "updated",

        "Testimonial Updated",

        f'{name}\'s testimonial has been updated.',

        created_by=user

    )


def notify_testimonial_deleted(name, user=None):

    add_notification(

        "testimonial",

        "deleted",

        "Testimonial Deleted",

        f'{name}\'s testimonial has been deleted.',

        priority="high",

        created_by=user

    )


# ==========================================================
# CONTACT MESSAGES
# ==========================================================

def notify_message_received(name, subject, user=None):

    add_notification(

        "system",

        "message_received",

        "New Contact Message",

        f'{name} sent a message: "{subject}".',

        created_by=user

    )


def notify_message_replied(name, subject, user=None):

    add_notification(

        "system",

        "message_replied",

        "Message Replied",

        f'Replied to {name}: "{subject}".',

        created_by=user

    )


def notify_message_deleted(name, subject, user=None):

    add_notification(

        "system",

        "message_deleted",

        "Message Deleted",

        f'Message from {name}: "{subject}" has been deleted.',

        priority="high",

        created_by=user

    )
    

# ==========================================================
# MAINTENANCE
# ==========================================================

def notify_candidate_backup(user=None):

    add_notification(

        "maintenance",

        "candidate_backup",

        "Candidate Backup Downloaded",

        "Candidate CV backup downloaded successfully.",

        created_by=user

    )

def notify_database_backup(user=None):

    add_notification(

        "maintenance",

        "backup",

        "Database Backup",

        "SQL backup completed successfully.",

        created_by=user

    )


def notify_database_restore(user=None):

    add_notification(

        "maintenance",

        "restore",

        "Database Restored",

        "Database restored successfully.",

        priority="high",

        created_by=user

    )


def notify_database_reset(user=None):

    add_notification(

        "maintenance",

        "reset",

        "Database Reset",

        "System database has been reset.",

        priority="critical",

        created_by=user

    )


# ==========================================================
# SECURITY
# ==========================================================

def notify_login(username):

    add_notification(

        "security",

        "login",

        "User Login",

        f"{username} logged in."

    )


def notify_logout(username):

    add_notification(

        "security",

        "logout",

        "User Logout",

        f"{username} logged out."

    )


def notify_password_changed(username):

    add_notification(

        "security",

        "password",

        "Password Changed",

        f"{username} changed password."

    )


def notify_security_alert(message):

    add_notification(

        "security",

        "alert",

        "Security Alert",

        message,

        priority="critical"

    )


# ==========================================================
# SYSTEM
# ==========================================================

def notify_system(message):

    add_notification(

        "system",

        "system",

        "System",

        message

    )
    

# ==========================================================
# MAINTENANCE IN FUTURE
# ==========================================================

def notify_cache_cleared(user=None):

    add_notification(

        "maintenance",

        "cache",

        "System Cache Cleared",

        "Application cache has been cleared.",

        created_by=user

    )


def notify_logs_cleared(user=None):

    add_notification(

        "maintenance",

        "logs",

        "System Logs Cleared",

        "Application logs have been cleared.",

        created_by=user

    )


def notify_system_restart(user=None):

    add_notification(

        "maintenance",

        "restart",

        "System Restarted",

        "System services restarted successfully.",

        priority="high",

        created_by=user

    )


def notify_settings_updated(user=None):

    add_notification(

        "maintenance",

        "settings",

        "System Settings Updated",

        "Application settings have been updated.",

        created_by=user

    )