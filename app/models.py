from database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gst_number = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    contact_person = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    bank_name = db.Column(db.String(100))
    bank_account = db.Column(db.String(100))
    ifsc = db.Column(db.String(20))
    additional_contacts = db.relationship('VendorContact', backref='vendor', cascade='all, delete-orphan')

class VendorContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    person_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enquiry_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    source_drawing = db.Column(db.String(300))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    quotation = db.Column(db.String(100))
    project_incharge = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    gst_number = db.Column(db.String(100))
    address = db.Column(db.String(250))
    vendor = db.relationship('Vendor', backref='projects')
    measurement_sheets = db.relationship('MeasurementSheet', backref='project', cascade='all, delete-orphan')

class MeasurementSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    duct_no = db.Column(db.String(50))
    duct_type = db.Column(db.String(50))
    w1 = db.Column(db.Float)
    h1 = db.Column(db.Float)
    w2 = db.Column(db.Float)
    h2 = db.Column(db.Float)
    degree_or_offset = db.Column(db.String(50))
    length_or_radius = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    factor = db.Column(db.Float)
    area = db.Column(db.Float)
    gauge = db.Column(db.String(10))
    bolts = db.Column(db.Integer)
    gasket = db.Column(db.Float)
    cleat = db.Column(db.Float)
    corner = db.Column(db.Integer)
    nuts = db.Column(db.Integer)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    contact = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
