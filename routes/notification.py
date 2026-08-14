from flask import (
    Blueprint,
    jsonify
)

from datetime import (
    datetime,
    timedelta
)

from utils.decorators import login_required

from models.notification_model import *
from services.notification_service import *

notification_bp = Blueprint(
    "notification",
    __name__
)


# ==========================================================
# Relative Time
# ==========================================================

def relative_time(value):

    if value is None:

        return ""

    now = datetime.now()

    diff = now - value

    if diff < timedelta(seconds=30):

        return "Just now"

    if diff < timedelta(minutes=1):

        return f"{diff.seconds} seconds ago"

    if diff < timedelta(hours=1):

        minutes = diff.seconds // 60

        return f"{minutes} minute{'s' if minutes>1 else ''} ago"

    if diff < timedelta(days=1):

        hours = diff.seconds // 3600

        return f"{hours} hour{'s' if hours>1 else ''} ago"

    if diff < timedelta(days=2):

        return "Yesterday"

    if diff < timedelta(days=7):

        return f"{diff.days} days ago"

    return value.strftime("%d %b %Y %I:%M %p")


# ==========================================================
# Get Notifications
# ==========================================================

@notification_bp.route(
    "/dashboard/notifications"
)
@login_required
def notifications():

    notifications = get_notifications()

    for item in notifications:

        item["time"] = relative_time(
            item["created_at"]
        )

    return jsonify(

        success=True,

        unread=get_unread_notification_count(),

        data=notifications

    )


# ==========================================================
# Unread Count Only
# ==========================================================

@notification_bp.route(
    "/dashboard/notifications/count"
)
@login_required
def notification_count():

    return jsonify(

        success=True,

        unread=get_unread_notification_count()

    )


# ==========================================================
# Mark One Read
# ==========================================================

@notification_bp.route(
    "/dashboard/notifications/read/<int:id>",
    methods=["POST"]
)
@login_required
def read_notification(id):

    mark_notification_read(id)

    return jsonify(

        success=True,

        unread=get_unread_notification_count()

    )


# ==========================================================
# Mark All Read
# ==========================================================

@notification_bp.route(
    "/dashboard/notifications/read-all",
    methods=["POST"]
)
@login_required
def read_all_notifications():

    mark_all_notifications_read()

    return jsonify(

        success=True,

        unread=0

    )


# ==========================================================
# Delete One
# ==========================================================

@notification_bp.route(
    "/dashboard/notifications/delete/<int:id>",
    methods=["POST"]
)
@login_required
def delete_single_notification(id):

    delete_notification(id)

    return jsonify(

        success=True,

        unread=get_unread_notification_count()

    )


# ==========================================================
# Clear All
# ==========================================================

@notification_bp.route(
    "/dashboard/notifications/clear",
    methods=["POST"]
)
@login_required
def clear_all_notifications():

    clear_notifications()

    return jsonify(

        success=True,

        unread=0

    )
    