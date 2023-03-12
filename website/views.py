from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, To_Dos, User, Diabetes, Heart, Park
from . import db
import json
from .diabetes import my_diabetes
from .heart import my_heart
from .parkinson import my_park
import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/landing')
def landing():
    return render_template("landingpg.html")

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/diab_reversal')
def diab_reversal():
    return render_template("diab_reversal.html", user=current_user)

@views.route('/diab_yes')
def diab_yes():
    return render_template("diab_popup_yes.html", user=current_user)

@views.route('/diab_no')
def diab_no():
    return render_template("diab_popup_no.html", user=current_user)

@views.route('/dashboard')
def dashboard():
    return render_template("yourdata.html", user=current_user)

@views.route('/details')
def details():
    return render_template("edit_profile.html", user=current_user)

@views.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        my_note = str(note)
        if len(my_note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')
    return render_template("notes.html", user=current_user)

@views.route('/todo', methods=['GET', 'POST'])
def todo_html():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) < 1 or len(desc) < 1:
            flash("ToDo is too short!", category='error')
        else:
            todo = To_Dos(title=title, desc=desc, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash("Todo added!", category='success')
    return render_template("todo.html", user=current_user)

@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = To_Dos.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')
    todo = To_Dos.query.filter_by(id=id).first()
    return render_template("update.html", todo=todo, user=current_user)

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_profile(id):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user = User.query.filter_by(id=id).first()
        user.firstname = firstname
        user.lastname = lastname
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    user = User.query.filter_by(id=id).first()
    return render_template("edit_profile.html", user=current_user)

@views.route('/delete/<int:id>')
def delete_todo(id):
    todo = To_Dos.query.filter_by(id=id).first()
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/todo')
    todo = To_Dos.query.filter_by(id=id).first()
    return render_template("todo.html", todo=todo, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            redirect('notes.html')
    return jsonify({})

@views.route('/diabetes', methods=['POST', 'GET'])
def diabetes():
    if request.method == 'POST':
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bloodpressure = float(request.form['bloodpressure'])
        skinthickness = float(request.form['skinthickness'])
        insulin = float(request.form['insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
        age = float(request.form['age'])
        pred_diabetes = my_diabetes(pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age)
        new_diabetes = Diabetes(pregnancies=pregnancies, glucose=glucose, bloodpressure=bloodpressure, skinthickness=skinthickness, insulin=insulin, BMI=BMI, DiabetesPedigreeFunction=DiabetesPedigreeFunction, age=age, pred_diabetes=pred_diabetes[0], user_id = current_user.id)
        db.session.add(new_diabetes)
        db.session.commit()
        if pred_diabetes[0] == 1:
            flash('You can have Diabetes', category="error")
            print("Probability for diabetes: ", pred_diabetes[1])
            return redirect('/diab_yes')
        else: 
            flash('You cannot have Diabetes', category="success")
            return redirect('/diab_yes')
    return render_template('diabetes_form.html', user=current_user)

@views.route('/heart', methods=['POST', 'GET'])
def heart():
    if request.method == 'POST':
        age = float(request.form['age'])
        s = request.form['sex']
        if s == 'male':
            sex = 1.0
        else:
            sex = 0.0
        cp = float(request.form['cp'])
        rbp = float(request.form['rbp'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        recg = float(request.form['recg'])
        mhra = float(request.form['mhra'])
        exia = float(request.form['exia'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        vcf = float(request.form['vcf'])
        thal = float(request.form['thal'])
        pred_heart = my_heart(age, sex, cp, rbp, chol, fbs, recg, mhra, exia, oldpeak, slope, vcf, thal)
        new_heart = Heart(age=age, sex=sex, cp=cp, rbp=rbp, chol=chol, fbs=fbs, recg=recg, mhra=mhra, exia=exia, oldpeak=oldpeak, slope=slope, vcf=vcf, thal=thal, pred_heart=pred_heart[0], user_id = current_user.id)
        db.session.add(new_heart)
        db.session.commit()
        if pred_heart[0] == 1:
            flash('You can have Heart Disease', category="error")

        else: 
            flash('You cannot have Heart Disease', category="success")
    return render_template('heart_form.html', user=current_user)

@views.route('/park', methods=['POST', 'GET'])
def park():
    if request.method == 'POST':
        mdvp_fo = float(request.form['mdvp_fo'])
        mdvp_fhi = float(request.form['mdvp_fhi'])
        mdvp_flo = float(request.form['mdvp_flo'])
        mdvp_jitter = float(request.form['mdvp_jitter'])
        mdvp_jitter_abs = float(request.form['mdvp_jitter_abs'])
        mdvp_rap = float(request.form['mdvp_rap'])
        mdvp_ppq = float(request.form['mdvp_ppq'])
        jitter_ddp = float(request.form['jitter_ddp'])
        mdvp_shimmer = float(request.form['mdvp_shimmer'])
        mdvp_shimmer_db = float(request.form['mdvp_shimmer_db'])
        mdvp_shimmer_apq3 = float(request.form['mdvp_shimmer_apq3'])
        mdvp_shimmer_apq5 = float(request.form['mdvp_shimmer_apq5'])
        mdvp_apq = float(request.form['mdvp_apq'])
        shimmer_dda = float(request.form['shimmer_dda'])
        nhr = float(request.form['nhr'])
        hnr = float(request.form['hnr'])
        rpde = float(request.form['rpde'])
        dfa = float(request.form['dfa'])
        spread1 = float(request.form['spread1'])
        spread2 = float(request.form['spread2'])
        d2 = float(request.form['d2'])
        ppe = float(request.form['ppe'])
        pred_park = my_park(mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter, mdvp_jitter_abs, mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db, mdvp_shimmer_apq3, mdvp_shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe)
        new_park = Park(mdvp_fo=mdvp_fo, mdvp_fhi=mdvp_fhi, mdvp_flo=mdvp_flo, mdvp_jitter=mdvp_jitter, mdvp_jitter_abs=mdvp_jitter_abs, mdvp_rap=mdvp_rap, mdvp_ppq=mdvp_ppq, jitter_ddp=jitter_ddp, mdvp_shimmer=mdvp_shimmer, mdvp_shimmer_db=mdvp_shimmer_db, mdvp_shimmer_apq3=mdvp_shimmer_apq3, mdvp_shimmer_apq5=mdvp_shimmer_apq5, mdvp_apq=mdvp_apq, shimmer_dda=shimmer_dda, nhr=nhr, hnr=hnr, rpde=rpde, spread2=spread2, d2=d2, dfa=dfa, ppe=ppe, pred_park=pred_park[0], user_id = current_user.id)
        db.session.add(new_park)
        db.session.commit()
        if pred_park[0] == 1:
            flash('You can have Parkinson Disease', category="error")
        else: 
            flash('You cannot have Parkinson Disease', category="success")
    return render_template('parkinson_form.html', user=current_user)