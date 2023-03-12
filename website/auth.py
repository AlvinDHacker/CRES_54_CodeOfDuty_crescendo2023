from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, login_user, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        key = str(password)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, key):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!, Try Again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login_form.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2= request.form.get('password2')
        age= request.form.get('age')
        gender= request.form.get('gender')
        bloodgrp= request.form.get('bloodgrp')
        weight= request.form.get('weight')
        height= request.form.get('height')
        heart_attack= request.form.get('heart_attack')
        mail = str(email)
        fname = str(firstname)
        lname = str(lastname)
        pass1 = str(password1)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(mail) < 4: 
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fname) < 2: 
            flash('First name must be greater than 1 character.', category='error')
        elif len(lname) < 2: 
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(pass1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(pass1, method='sha256'), age=age, gender=gender, bloodgrp=bloodgrp, weight=weight, height=height, heart_attack=heart_attack)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) # views.py --> home() function
            # OR return redirect('/')
    return render_template("signup_form.html", user=current_user)