
from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from random import randrange
from website.myfcn import sendEmail

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
               
        user = User.query.filter_by(email=email).first()  #sqlalchemy        
  
        if user:
            if user.password == password:     
                login_user(user, remember=True)
                return redirect(url_for('views.home'))               
                               
        return render_template("login.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')            

                
        if password == password_repeat: 
            log_password = ""
            for x in range(4):
                number = randrange(4)+1
                log_password = log_password + str(number)              

            new_user = User(email=email,password=password,first_name=first_name,last_name=last_name, log_password=int(log_password))
            db.session.add(new_user)
            db.session.commit()   

            sprava = "Vitajte, " + first_name + ". \n\nVáš účet bol vytvorený. Vitajte v systéme Inteligentny vránik.\n\nVaše vygenerované heslo pre prvý vstup:\n\n" + log_password 
            sendEmail(email, "Vitajte", sprava)

        return render_template("login.html")


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'GET':      
        logout_user()
        return redirect(url_for('auth.login'))   