from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import User, Reservation
from . import db
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import json
from sqlalchemy import desc

views = Blueprint('views', __name__)


#data - vyfiltrovane rezervacie pre konkretneho uzivatela, tie sa tu aj vypocitavaju
@views.route('/home', methods=['GET','POST'])
@login_required
def home():
    reservation = Reservation.query.order_by(Reservation.date).all()
   
    date_now = datetime.today() - timedelta(hours=1)

    final = []    
    i = 1
    for res in reservation:  
        if(res.user_id == current_user.id): 
            if(date_now < res.date):           
                fulldate = res.date
                date = str(fulldate.day) + "." + str(fulldate.month) + "." + str(fulldate.year)   
                time = str(fulldate.hour) + ":00 - " + str(fulldate.hour+1) + ":00"      
                small = (i, date, time, res.id)            
                final.append(small)
                i += 1    
                  
    return render_template("home.html", User=current_user, Reservation = reservation, data=final)
    


#api na vytvorenie rezervacie a pridanie do databazy
@views.route('/reservation', methods=['GET','POST'])
@login_required
def reservation():

    if request.method == 'POST':      

        date = request.form.get('date')
        cas = request.form.get('time')

        date_split = date.split("-")
        cas_split = cas.split(":")
     
        date = datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]),int(cas_split[0]))
               
        new_reservation = Reservation(date=date,user_id=current_user.id)
        db.session.add(new_reservation)
        db.session.commit() 

        return redirect(url_for('views.home'))  
    

#api na ziskanie vsetkych rezervacii
@views.route('/getReservation', methods=['GET','POST'])
@login_required
def getReservation():
    
    reservation = Reservation.query.all()  
    dates = {}

    for res in reservation:  
        fulldate = res.date

        dates[res.id]={
                "day": str(fulldate.day),
                "month":  str(fulldate.month),
                "year": str(fulldate.year),
                "hour": str(fulldate.hour)
                }          
                
    return json.dumps(dates)


#api na zmazanie rezervacia
@views.route('/deleteReservation', methods=['POST'])
@login_required
def deleteReservation():    
                    
    resID = json.loads(request.data)    
    resID = resID['resID']    
    
    res = Reservation.query.get(resID)
    if res:
        if res.user_id == current_user.id:
            db.session.delete(res)
            db.session.commit()

    return jsonify({})
   


