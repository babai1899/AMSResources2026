from services.maintenance_service import *

def get_dashboard_data():

    return {

        "system": {

            "database": "Connected",

            "storage": get_candidate_folder_size(),

            "mail": "SMTP Connected",

            "last_backup": get_latest_backup()

        }

    }