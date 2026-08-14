import os
import uuid
# ------------------------
# SAVE TESTIMONIAL IMAGES
# ------------------------    
UPLOAD_TESTIMONIAL = "static/testimonials"

def save_testimonial_image(file):

    ext=file.filename.rsplit(".",1)[1].lower()

    filename=f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(UPLOAD_TESTIMONIAL,exist_ok=True)

    file.save(os.path.join(

        UPLOAD_TESTIMONIAL,

        filename

    ))

    return filename