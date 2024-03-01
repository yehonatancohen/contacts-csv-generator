from flask import Blueprint, render_template, redirect, url_for, request, abort
from werkzeug.utils import secure_filename
from flask import current_app as app
import os

home = Blueprint('home', __name__,
    template_folder='templates',
    static_folder='static/home')

@home.route('/')
def index():
    return render_template('home.html')

@home.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENTIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('home.index'))