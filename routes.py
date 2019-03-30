from flask import redirect, request, render_template, url_for
from flask_login import login_user, current_user, login_required, logout_user
from server import *
import datetime
import glob as g



@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        userObject=system.find_user(email)
        if userObject!= None and userObject.validate_password(password):
            login_user(get_user(userObject.get_id()))
            return redirect(url_for('welcome'))
        else:
            return render_template("login.html",failed=True)
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if current_user.is_provider==True:
        return redirect(url_for('welcome'))

    if request.method=='POST':
        string = request.form["search_string"]
        option = request.form["options"]
        if option =='all':
            search_resultsC=system.centreManager.centres
            search_resultsP=system.userManager.providers()
            return render_template('search.html',found=True,centre=True,provider=True,search_resultsC=search_resultsC,search_resultsP=search_resultsP)
        elif option =='cName':
            search_resultsC=system.centreManager.search_centre(False,True,string)
            if len(search_resultsC)>0:
                return render_template('search.html',found=True,centre=True,provider=False,search_resultsC=search_resultsC)
        elif option == 'cSuburb':
            search_resultsC=system.centreManager.search_centre(True,False,string)
            if len(search_resultsC)>0:
                return render_template('search.html',found=True,centre=True,provider=False,search_resultsC=search_resultsC)
        elif option == 'pName':
            search_resultsP=system.userManager.search_provider(False,True,string)
            if len(search_resultsP)>0:
                return render_template('search.html',found=True,centre=False,provider=True,search_resultsP=search_resultsP)
        elif option == 'pService':
            search_resultsP=system.userManager.search_provider(True,False,string)
            if len(search_resultsP)>0:
                return render_template('search.html',found=True,centre=False,provider=True,search_resultsP=search_resultsP)
        return render_template('search.html',notfound=True)
    return render_template('search.html')


@app.route('/pPageCentre/<centre_name>',methods=['POST','GET'])
@login_required
def profile_centre(centre_name):
    centreObject = system.find_centre(centre_name)
    if request.method=='POST':
        newRating=int(request.form['rating'])
        system.add_rating(centreObject,current_user.full_name,newRating)
    rating = system.get_rating(centreObject)
    return render_template('profileCentre.html',centre=centreObject,rating=rating)


@app.route('/pPageProvider/<full_name>',methods=['POST','GET'])
@login_required
def profile_provider(full_name):
    if current_user.is_provider==True:
        return redirect(url_for('welcome'))
    providerObject=system.find_provider(full_name)
    if request.method=='POST':
        newRating=int(request.form['rating'])
        system.add_rating(providerObject,current_user.full_name,newRating)
    rating = system.get_rating(providerObject)
    centres=system.find_centres(providerObject)
    return render_template('profileProvider.html',provider=providerObject,centres=centres,rating=rating)


@app.route('/book/<centre_name>/<full_name>', methods=['POST','GET'])
@login_required
def book(centre_name,full_name):
    if current_user.is_provider==True:
        return redirect(url_for('welcome'))
    providerObject= system.find_provider(full_name)
    centreObject = system.find_centre(centre_name)
    if request.method=='POST':
        date=request.form['date']
        date=system.date_refactor(date)
        hours = system.find_hours(date, providerObject, centreObject,current_user)
        if len(hours)==0:
            found=False
        else:
            found=True
        return render_template('datePicker.html',doctor=providerObject.full_name,centre=centreObject.centre_name,time=found,hours=hours,date=date,searched=True)
    return render_template('datePicker.html',doctor=providerObject.full_name,centre=centreObject.centre_name,time=False)


@app.route('/book/<centre_name>/<full_name>/<date>/<time>',methods=['POST','GET'])
@login_required
def bookConfirmation(centre_name,full_name,date,time):
    if current_user.is_provider==True:
        return redirect(url_for('welcome'))
    providerObject=system.find_provider(full_name)
    centreObject = system.find_centre(centre_name)
    patientObject = next((i for i in system.userManager._users if (i.full_name == current_user.full_name and i.is_provider==False)),None)
    if request.method=='POST':
        reason = request.form['reason']
        g.apptIndex=g.apptIndex+1
        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,g.apptIndex)
        print(g.apptIndex)
        return render_template('bookConfirm.html',centre=centreObject.centre_name,doctor=providerObject.full_name,date=date,time=time,confirmed=True)
    return render_template('bookConfirm.html',centre=centreObject.centre_name,doctor=providerObject.full_name,date=date,time=time,confirmed=False)


@app.route('/currentA')
@login_required
def viewAppoint():
    searchResults=current_user.appointments.search_appointment(False)
    searchResults.sort(key=lambda x: (x.date, str(x.time)))
    return render_template('upcoming.html',a=searchResults)

@app.route('/startAppt/<id>',methods=['POST','GET'])
@login_required
def startAppt(id):
    appointmentDetailsDoc= system.find_appt(current_user,int(id))
    appointmentDetailsPatient= system.find_appt(appointmentDetailsDoc.patient,int(id))
    if current_user.is_provider==False or appointmentDetailsDoc==None:
        return redirect(url_for('welcome'))
    if request.method=='POST':
        notes = request.form['notes']
        meds = request.form['meds']
        system.update_appt(appointmentDetailsDoc,appointmentDetailsPatient,notes,meds)
        return render_template('apptEnd.html',appointment= appointmentDetailsDoc,meds=meds,notes=notes)
    return render_template('apptcentre.html',appointment= appointmentDetailsDoc)

@app.route('/history/<full_name>',methods=['POST','GET'])
@login_required
def history(full_name):
    patient = system.find_patient(full_name)
    if current_user.is_provider==False or system.has_access(patient,current_user)==False:
        return redirect(url_for('welcome'))
    searchResults=patient.appointments.search_appointment(True)
    return render_template('patientHistory.html',appointments=searchResults,patient =patient)


@app.route('/myHistory',methods=['POST','GET'])
@login_required
def myHis():
    if current_user.is_provider==True:
        return redirect(url_for('welcome'))
    searchResults=current_user.appointments.search_appointment(True)
    return render_template('patientHistory.html',appointments=searchResults,patient =current_user)


@app.route('/myProfile',methods=['POST','GET'])
@login_required
def profile_user():
    if current_user.is_provider==True:
        providerObject=system.find_provider(current_user.full_name)
        rating = system.get_rating(providerObject)
        centres=system.find_centres(providerObject)
        if request.method=='POST':
            email = request.form['email']
            number = request.form['number']
            pNumber=request.form['Pnumber']
            system.update_provider(providerObject,email,number,pNumber)
        return render_template('profile.html',provider=providerObject, rating=rating, centres=centres)
    else:
        patientObject=system.find_patient(current_user.full_name)
        if request.method=='POST':
            email = request.form['email']
            number = request.form['number']
            medicare= request.form['medicare']
            system.update_patient(patientObject,email,number,medicare)
        return render_template('profile.html',patient=patientObject)
