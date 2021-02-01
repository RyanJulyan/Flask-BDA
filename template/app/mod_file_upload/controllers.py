
# Import os for file path
import os

# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required
from sqlalchemy import event

# Import mobile template
from flask_mobility.decorators import mobile_template

# Import mail message to compile a message
from werkzeug.utils import secure_filename

# Import the database object from the main app module
from app import app

# Import module models (e.g. User)
from app.mod_xyz.models import Xyz

# Define the blueprint: 'xyz', set its url prefix: app.url/xyz
mod_file_upload = Blueprint('fild_upload', __name__, template_folder='templates', url_prefix='/file_upload')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@mod_file_upload.route('/')
def upload_form():
    return render_template('file_upload.upload.html')


@mod_file_upload.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/')
