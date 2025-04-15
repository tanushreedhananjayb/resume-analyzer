import os
import io
import csv
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, current_app
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF

from .models import db, User, ResumeData
from app.forms import RegisterForm, LoginForm, ResumeUploadForm
from app.utils.resume_processing import extract_text_from_resume, match_resume_to_jobs

routes = Blueprint('routes', __name__)
UPLOAD_FOLDER = 'uploads'

# ---------- Home ----------
@routes.route('/')
def index():
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template('index.html', register_form=register_form, login_form=login_form)

# ---------- Register ----------
@routes.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'warning')
            return redirect(url_for('routes.index'))

        # Hash the password
        hashed_pw = generate_password_hash(password)

        # Create a new user and persist it to the database
        new_user = User(name=name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()  # Save to the database

        # Debugging print statement to check if the user is added
        print(f"New user created: {new_user.name}, {new_user.email}")

        flash('Registration successful! Please login.', 'success')
    else:
        flash('Invalid registration details.', 'danger')

    return redirect(url_for('routes.index'))

# ---------- Login ----------
@routes.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Log the user in
            login_user(user)

            # Set session variables manually if needed
            session['user_id'] = user.id
            session['user_name'] = user.name

            # Debugging the session data
            print(f"Session user_id: {session['user_id']}")
            print(f"Session user_name: {session['user_name']}")

            flash('Welcome back!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return redirect(url_for('routes.index'))

# ---------- Dashboard ----------
@routes.route('/dashboard')
@login_required
def dashboard():
    form = ResumeUploadForm()
    return render_template('dashboard.html', name=current_user.name, form=form)

# ---------- Upload Resume ----------
@routes.route('/upload', methods=['POST'])
@login_required
def upload_resume():
    form = ResumeUploadForm()

    if form.validate_on_submit():
        file = form.resume.data

        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('routes.dashboard'))

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        resume_text = extract_text_from_resume(filepath)

        if not resume_text.strip():
            flash("Couldn't extract text from resume. Please upload a valid PDF.", "danger")
            return redirect(url_for('routes.dashboard'))

        matched_jobs = match_resume_to_jobs(resume_text)

        # Store jobs in session for download functionality
        session['jobs'] = matched_jobs

        return render_template('result.html', job_matches=matched_jobs, name=current_user.name)

    flash("Upload failed. Try again.", "danger")
    return redirect(url_for('routes.dashboard'))

# ---------- Admin ----------
@routes.route('/admin')
def admin():
    data = ResumeData.query.order_by(ResumeData.created_at.desc()).all()
    return render_template('admin.html', logs=data)

# ---------- Download CSV ----------
@routes.route('/download/csv')
def download_csv():
    jobs = session.get('jobs', [])
    
    if not jobs:
        flash("No jobs to download.", "warning")
        return redirect(url_for('routes.dashboard'))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Job Title', 'Company', 'Score (%)', 'Description'])
    
    for job in jobs:
        writer.writerow([job['title'], job['company'], job['score'], job['description']])
    
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                     download_name='matched_jobs.csv', as_attachment=True)

# ---------- Download PDF ----------
@routes.route('/download/pdf')
def download_pdf():
    jobs = session.get('jobs', [])
    
    if not jobs:
        flash("No jobs to download.", "warning")
        return redirect(url_for('routes.dashboard'))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Top Matched Jobs", ln=True, align='C')
    pdf.ln(10)

    for job in jobs:
        pdf.set_font("Arial", style='B', size=12)
        pdf.multi_cell(0, 10, f"{job['title']} - {job['company']} ({job['score']}%)")
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, job['description'][:500] + '...')  # Limit description length
        pdf.ln(5)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, mimetype='application/pdf',
                     download_name='matched_jobs.pdf', as_attachment=True)

# ---------- Logout ----------
@routes.route('/logout')
@login_required
def logout():
    logout_user()  # Flask-Login's logout_user to handle the session clearing
    flash('Logged out successfully.', 'info')
    return redirect(url_for('routes.index'))
