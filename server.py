from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from models.EHealthSystem import *
import csv
import os.path
import atexit
import glob as g


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Another_highly_secret_key'

# login set up
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def get_user(id):
    userObject=next((i for i in system.userManager._users if i.get_id() == id), None)
    print(userObject)
    return userObject

@login_manager.user_loader
def load_user(id):
    userObject=next((i for i in system.userManager._users if i.get_id() == id), None)
    return userObject

# system set up
Bootstrap(app)
datepicker(app)
system = EHealthSystem()


columnsPatient=['full_name','patient_email','password','medicare','phone_number']
if os.path.isfile('data/patients/patients.csv')==True:
    with open('data/patients/patients.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['full_name']
            email = row['patient_email']
            password = row['password']
            medicare = row['medicare']
            phone = row['phone_number']
            system.userManager.add_user(Patient(name,email,phone,password,medicare))
else:
    with open('inputs/patient.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['full_name']
            email = row['patient_email']
            password = row['password']
            medicare = row['medicare']
            phone = row['phone_number']
            system.userManager.add_user(Patient(name,email,phone,password,medicare))

columnsProvider=['full_name','provider_email','provider_type','password','phone_number','provider_number']


if os.path.isfile('data/providers/providers.csv')==True:
    with open('data/providers/providers.csv')as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['full_name']
            email = row['provider_email']
            type = row['provider_type']
            password = row['password']
            phone = row['phone_number']
            number=row['provider_number']
            system.userManager.add_user(Provider(name,email,phone,password,number,type))
else:
    with open('inputs/provider.csv')as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['full_name']
            email = row['provider_email']
            type = row['provider_type']
            password = row['password']
            phone = row['phone_number']
            number=row['provider_number']
            system.userManager.add_user(Provider(name,email,phone,password,number,type))

columnsCentres=['centre_type','abn','name','phone','suburb','description']

with open('inputs/health_centres.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        type = row['centre_type']
        abn = row['abn']
        name = row['name']
        phone = row['phone']
        suburb = row['suburb']
        description = row['description']
        system.centreManager.add_centre(Centre(name,suburb,abn,phone,type,description))



columnsServies=['provider_email','health_centre_name','start','end']

with open('inputs/provider_health_centre.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row['provider_email']
        centre = row['health_centre_name']
        start = row['start']
        end = row['end']
        providerObject=next((i for i in system.userManager._users if (i.email == email and i.is_provider==True)), None)
        centreObject = next((i for i in system.centreManager._centres if i.centre_name==centre),None)
        providerObject.add_centre_working_hours(centre,int(start),int(end))
        centreObject.add_provider_service(providerObject.service,providerObject)


columnsAppts=['date,time','reason','notes','meds','completed','patient','provider','centre','id']
columnsRatings=['patient','rating']

for i in system.userManager.users:
    if i.is_provider==False:
        name= i.full_name.split()
        newName=name[0]+'_'+name[1]
        if os.path.isfile('data/patients/%s_appts.csv' % newName)==True:
            with open('data/patients/%s_appts.csv' % newName) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date = row['date']
                    time= row['time']
                    reason= row['reason']
                    notes = row['notes']
                    meds = row ['meds']
                    completed = row['completed']
                    patient = row['patient']
                    provider=row['provider']
                    centre=row['centre']
                    id=int(row['id'])
                    if g.apptIndex<int(id):
                        g.apptIndex=int(id)
                    print(patient)
                    patient=system.find_patient(patient)
                    provider=system.find_provider(provider)
                    centre=system.find_centre(centre)
                    if completed=='False':
                        patient.appointments.add_appointment(Appointment(date,datetime.datetime.strptime(time, '%H:%M:%S').time(),reason,patient, provider, centre,id,False))
                        provider.appointments.add_appointment(Appointment(date,datetime.datetime.strptime(time, '%H:%M:%S').time(),reason,patient, provider, centre,id,False))
                    else:
                        patient.appointments.add_appointment(Appointment(date,datetime.datetime.strptime(time, '%H:%M:%S').time(),reason,patient, provider, centre,id,True))
                        provider.appointments.add_appointment(Appointment(date,datetime.datetime.strptime(time, '%H:%M:%S').time(),reason,patient, provider, centre,id,True))

for i in system.userManager.users:
    if i.is_provider==True:
        name= i.full_name.split()
        newName=name[0]+'_'+name[1]
        if os.path.isfile('data/providers/%s_ratings.csv' % newName)==True:
            with open('data/providers/%s_ratings.csv' % newName) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    patient = row['patient']
                    rating = int(row['rating'])
                    patient=system.find_patient(patient)
                    provider=system.find_provider(i.full_name)
                    system.add_rating(provider,patient,rating)


for i in system.centreManager.centres:
    name= i.centre_name.split()
    newName=name[0]+'_'+name[1]
    if os.path.isfile('data/centres/%s_ratings.csv' % newName)==True:
        with open('data/centres/%s_ratings.csv' % newName) as f:
            reader = csv.DictReader(f)
            for row in reader:
                patient = row['patient']
                rating = int(row['rating'])
                patient=system.find_patient(patient)
                centre=system.find_centre(i.centre_name)
                system.add_rating(centre,patient,rating)
