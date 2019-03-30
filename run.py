from routes import app
import atexit
import dill
from flask import Flask, current_app
from routes import *
from server import *
from models.EHealthSystem import *




if __name__ == '__main__':
    app.run(debug=False)

def exit_handler():
    patientsFile=open('data/patients/patients.csv' ,'w')
    patientsFile.write("full_name,patient_email,password,medicare,phone_number\n")
    providerFile=open('data/providers/providers.csv' ,'w')
    providerFile.write("full_name,provider_email,provider_type,password,phone_number,provider_number\n")
    for i in system.userManager.users:
        if i.is_provider==False:
            patientsFile.write("{},{},{},{},{}\n".format(i.full_name,i.email,i._password,i.medicare,i.phone_number))
            name= i.full_name.split()
            newName=name[0]+'_'+name[1]
            with open('data/patients/%s_appts.csv' % newName,'w') as f:
                f.write("date,time,reason,notes,meds,completed,patient,provider,centre,id\n")
                for j in i.appointments.appointments:
                    print(j.date)
                    f.write("{},{},{},{},{},{},{},{},{},{}\n".format(j.date,j.time,j.visit_reason,j.notes,j.medication,j.completed,j.patient.full_name,j.provider.full_name,j.centre.centre_name,j.id))
        else:
            providerFile.write("{},{},{},{},{},{}\n".format(i.full_name,i.email,i.service,i._password,i.phone_number,i.provider_number))
            name= i.full_name.split()
            newName=name[0]+'_'+name[1]
            with open('data/providers/%s_ratings.csv' % newName,'w') as f:
                f.write("patient,rating\n")
                for key,value in i._ratings._ratings.items():
                    f.write("{},{}\n".format(key,value))

    for i in system.centreManager.centres:
        name= i.centre_name.split()
        newName=name[0]+'_'+name[1]
        with open('data/centres/%s_ratings.csv' % newName,'w') as f:
            f.write("patient,rating\n")
            for key,value in i._ratings._ratings.items():
                f.write("{},{}\n".format(key,value))
atexit.register(exit_handler)
