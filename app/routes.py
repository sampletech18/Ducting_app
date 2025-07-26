# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app.database import db
from datetime import datetime
import os
import math
from app.models import User, Vendor, Project, MeasurementSheet

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

def generate_enquiry_id():
    year = datetime.now().year
    state_code = "TN"
    vendor_code = "2526"
    count = Project.query.count() + 1
    return f"VE/{state_code}/{vendor_code}/E{count:03d}"

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            session['user'] = user.username
            return redirect(url_for('main.dashboard'))

        flash('Invalid Credentials')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('User registered')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('dashboard.html')

@main.route('/vendors', methods=['GET', 'POST'])
def vendors():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        vendor = Vendor(
            name=request.form['name'],
            gst_number=request.form['gst'],
            address=request.form['address'],
            contact_person=request.form['person'],
            contact_email=request.form['email'],
            contact_phone=request.form['phone'],
            bank_name=request.form['bank'],
            bank_account=request.form['account'],
            ifsc=request.form['ifsc']
        )
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor added')
        return redirect(url_for('main.vendors'))

    vendors = Vendor.query.all()
    return render_template('vendor_registration.html', vendors=vendors)

@main.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    vendors = Vendor.query.all()

    if request.method == 'POST':
        enquiry_id = generate_enquiry_id()

        file = request.files.get('source_drawing')
        filename = secure_filename(file.filename) if file else None
        if filename:
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        project = Project(
            enquiry_id=enquiry_id,
            name=request.form['name'],
            location=request.form['location'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            vendor_id=request.form['vendor_id'],
            gst_number=request.form['gst'],
            address=request.form['address'],
            quotation=request.form['quotation'],
            project_incharge=request.form['incharge'],
            email=request.form['email'],
            phone=request.form['phone'],
            source_drawing=filename
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('main.projects'))

    enquiry_id = generate_enquiry_id()
    return render_template('new_project.html', enquiry_id=enquiry_id, vendors=vendors)

@main.route('/projects')
def projects():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@main.route('/measurement_sheet/<int:project_id>', methods=['GET', 'POST'])
def measurement_sheet(project_id):
    if 'user' not in session:
        return redirect(url_for('main.login'))

    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        w1 = float(request.form['w1'])
        h1 = float(request.form['h1'])
        w2 = float(request.form['w2'])
        h2 = float(request.form['h2'])
        length_or_radius = float(request.form['length_or_radius'])
        quantity = int(request.form['quantity'])
        factor = float(request.form['factor'])

        area = (w1 * h1 * quantity * factor) / 1000000
        gasket = 2 * (w1 + h1) * quantity * factor
        cleat = 2 * (w1 + h1) * quantity * factor
        bolts = math.ceil((2 * (w1 + h1) / 150) * quantity * factor)
        corner = 4 * quantity

        if w1 <= 751 and h1 <= 751:
            gauge = '24g'
        elif w1 <= 1201 and h1 <= 1201:
            gauge = '22g'
        elif w1 <= 1800 and h1 <= 1800:
            gauge = '20g'
        else:
            gauge = '18g'

        sheet = MeasurementSheet(
            project_id=project_id,
            duct_no=request.form['duct_no'],
            duct_type=request.form['duct_type'],
            w1=w1,
            h1=h1,
            w2=w2,
            h2=h2,
            degree_or_offset=request.form['degree_or_offset'],
            length_or_radius=length_or_radius,
            quantity=quantity,
            factor=factor,
            area=area,
            gauge=gauge,
            bolts=bolts,
            gasket=gasket,
            cleat=cleat,
            corner=corner,
            nuts=0
        )
        db.session.add(sheet)
        db.session.commit()
        flash('Measurement entry added')

    sheets = MeasurementSheet.query.filter_by(project_id=project_id).all()
    return render_template('measurement_sheet.html', project=project, sheets=sheets)
        
