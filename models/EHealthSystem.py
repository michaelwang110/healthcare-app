from models.UserManager import *
from models.CentreManager import *
import datetime

class EHealthSystem:
    def __init__(self):
        self.centreManager=CentreManager()
        self.userManager = UserManager()

    def find_user(self,email):
        return next((i for i in self.userManager._users if i.email == email), None)

    def find_centre(self,centre_name):
        return next((i for i in self.centreManager._centres if i.centre_name==centre_name),None)

    def find_provider(self,full_name):
        return next((i for i in self.userManager._users if (i.full_name == full_name and i.is_provider==True)), None)

    def find_patient(self,full_name):
        return next((i for i in self.userManager._users if (i.full_name == full_name and i.is_provider==False)), None)

    def find_centres(self,providerObject):
        centres=[]
        for key,value in providerObject.centre_working_hours.items():
            centres.append(next((i for i in self.centreManager._centres if i.centre_name==key),None))
        return centres


    def find_hours(self,date, providerObject, centreObject,current_user):

        hours = []
        start_time = providerObject.centre_working_hours[centreObject.centre_name]['start']
        end_time = providerObject.centre_working_hours[centreObject.centre_name]['finish']
        start_time= datetime.datetime.combine(datetime.date.min, start_time)
        end_time= datetime.datetime.combine(datetime.date.min, end_time)
        cur_date = datetime.datetime.now().date()
        cur_time = datetime.datetime.now()
        if date >= cur_date:
            if date > cur_date:
                while start_time < end_time:
                    hours.append(start_time.time())
                    start_time += datetime.timedelta(minutes=30)
            else:
                if cur_time.time() < end_time.time():
                    if cur_time.time().minute < 30:
                        cur_time = cur_time.replace(minute=30)
                    else:
                        hr = cur_time.hour
                        hr += 1
                        if hr == 24:
                            hr = 00
                        cur_time = cur_time.replace(hour=hr, minute=00)
                while cur_time.time() < end_time.time():
                    hours.append(cur_time.time())
                    cur_time += datetime.timedelta(minutes=30)
            
            for i in providerObject.appointments.appointments:
                if i.date==str(date) and i.centre == centreObject:
                    hours.remove(i.time)
            for i in current_user.appointments.appointments:
                if i.date==str(date):
                    if i.time in hours:
                        hours.remove(i.time)
        return hours

    def add_appointment(self,providerObject,current_user,date,time,reason,patientObject,centreObject,id):
        providerObject.appointments.add_appointment(Appointment(date,datetime.datetime.strptime(time, '%H:%M:%S').time(),reason,patientObject, providerObject, centreObject,id,False))
        current_user.appointments.add_appointment(Appointment(date,datetime.datetime.strptime(time, '%H:%M:%S').time(),reason,patientObject, providerObject, centreObject,id,False))



    def date_refactor(self,date):
        date=date.split("/")
        day=date[0]
        month=date[1]
        year=date[2]
        return datetime.date(int(year), int(month), int(day))

    def find_appt(self,user,id):
        for j in user.appointments.appointments:
            if int(j.id)==id:
                return j

    def update_appt(self, appointmentDetailsDoc,appointmentDetailsPatient,notes,meds):
        appointmentDetailsDoc.notes=notes
        appointmentDetailsDoc.medication=meds
        appointmentDetailsDoc.completed= True
        appointmentDetailsPatient.notes=notes
        appointmentDetailsPatient.medication=meds
        appointmentDetailsPatient.completed= True

    def get_rating(self,centre):
        return centre._ratings.calculate_average()

    def add_rating(self,centre,user,rating):
        centre._ratings.add_rating(user,rating)

    def has_access(self,patient,doctor):
        return patient.has_access(doctor)

    def update_provider(self,providerObject,email,number,pnumber):
        providerObject.email=email
        providerObject.phone_number=number
        providerObject.provider_number=pnumber

    def update_patient(self,patientObject,email,number,medicare):
        patientObject.email=email
        patientObject.phone_number=number
        patientObject.medicare=medicare
