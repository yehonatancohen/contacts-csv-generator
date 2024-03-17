from flask import Blueprint, render_template, redirect, url_for, request, abort, make_response
from werkzeug.utils import secure_filename
from flask import current_app as app
import os
from util import create_csv, translate_numbers 

home = Blueprint('home', __name__,
    template_folder='templates',
    static_folder='static/home')

@home.route('/')
def index():
    return render_template('home.html')

@home.route('/upload', methods=['POST'])
def upload_files():
    prefix = request.form['prefix']
    group_size = request.form['groupSize']
    phone_numbers = request.form['phoneNumbers']
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENTIONS']:
            abort(400)
        file = translate_numbers(uploaded_file)
        create_csv.create_csv(uploaded_file, prefix, group_size)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    elif phone_numbers != '':
        file = create_csv.create_csv(phone_numbers, prefix, group_size)
        output = make_response(file.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    return redirect(url_for('home.index'))