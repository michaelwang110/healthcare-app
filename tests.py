import pytest
from server import *
from models.EHealthSystem import *


class TestMakeBooking(object):
    def test_make_booking(self):
        print("testing making a booking")

        id = 1
        time = '09:00:00'
        date = '2018-10-20'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,id)

        assert patientObject.appointments.appointments[0].time == datetime.datetime.strptime(time, '%H:%M:%S').time()
        assert providerObject.appointments.appointments[0].time == datetime.datetime.strptime(time, '%H:%M:%S').time()
        assert patientObject.appointments.appointments[0].date == date
        assert providerObject.appointments.appointments[0].date == date
        assert patientObject.appointments.appointments[0].visit_reason == 'cold'
        assert providerObject.appointments.appointments[0].visit_reason == 'cold'
        assert patientObject.appointments.appointments[0].patient == patientObject
        assert providerObject.appointments.appointments[0].patient == patientObject
        assert patientObject.appointments.appointments[0].provider == providerObject
        assert providerObject.appointments.appointments[0].provider == providerObject
        assert patientObject.appointments.appointments[0].centre == centreObject
        assert providerObject.appointments.appointments[0].centre == centreObject

    # bookings made in past will automatically be handled by the front end and an error returned

    def test_booking_in_past(self):
        print("Testing making booking in past")

        id = 123
        time = '09:00:00'
        date = '2018-10-12'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        check_date = datetime.date(2018, 10, 12)
        hours = system.find_hours(check_date, providerObject,centreObject,current_user)
        assert len(hours) == 0

    def test_multiple_appointments(self):
        print("testing booking multiple appointments in the same day and time slot")

        id = 2
        booking_time = '09:00:00'
        date = '2018-10-17'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        temp_time = time(hour=9,minute=0,second=0,microsecond=0)
        check_date = datetime.date(2018, 10, 17)
        check_time = datetime.datetime.combine(check_date, temp_time)
        hours = system.find_hours(check_date, providerObject, centreObject, current_user)
        assert check_time.time() in hours
        assert len(hours) == 4

        system.add_appointment(providerObject,current_user,date,booking_time,reason,patientObject,centreObject,id)

        hours = system.find_hours(check_date, providerObject, centreObject, current_user)
        assert len(hours) == 3
        assert check_time.time() not in hours
        
        id = 3
        booking_time = '09:30:00'
        reason = 'arm hurt'

        temp_time = time(hour=9,minute=30,second=0,microsecond=0)
        check_time = datetime.datetime.combine(check_date, temp_time)
        assert check_time.time() in hours

        system.add_appointment(providerObject,current_user,date,booking_time,reason,patientObject,centreObject,id)

        hours = system.find_hours(check_date, providerObject, centreObject, current_user)
        assert check_time.time() not in hours
        assert len(hours) == 2

        id = 4
        booking_time = '10:00:00'
        reason = 'leg hurt'
        current_user = system.find_patient('Hao Diamond')
        newPatientObject = system.find_patient('Hao Diamond')

        assert current_user != None
        assert newPatientObject != None

        temp_time = time(hour=10,minute=0,second=0,microsecond=0)
        check_time = datetime.datetime.combine(check_date, temp_time)
        assert check_time.time() in hours

        system.add_appointment(providerObject,current_user,date,booking_time,reason,newPatientObject,centreObject,id)

        hours = system.find_hours(check_date, providerObject, centreObject, current_user)
        assert len(hours) == 1
        assert check_time.time() not in hours

    def test_appointment_with_self(self):
        #handled by frontend
        pass


class TestViewHistory(object):
    def test_view_new_patient_history(self):
        print("testing viewing a new patient's history")

        time = '13:30:00'
        date = '2018-10-20'
        reason = 'cold'
        current_user = system.find_patient('Tom Smith')
        patientObject = system.find_patient('Tom Smith')
        providerObject = system.find_provider('Anna Quin')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user != None
        assert patientObject != None
        assert providerObject != None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,5)

        current_user = system.find_provider('Anna Quin')
        assert current_user.is_provider == True
        assert system.has_access(patientObject, current_user) == True

        appointmentPatient = system.find_appt(patientObject, 5)
        appointmentProvider = system.find_appt(current_user, 5)
        searchResults = patientObject.appointments.search_appointment(True)

        assert appointmentPatient != None
        assert appointmentPatient.date == date
        assert appointmentPatient.time == datetime.datetime.strptime(time, '%H:%M:%S').time()
        assert appointmentPatient.visit_reason == reason
        assert appointmentPatient.notes == ""
        assert appointmentPatient.medication == ""
        assert appointmentPatient.completed == False
        assert appointmentPatient.patient == patientObject
        assert appointmentPatient.provider == providerObject
        assert appointmentPatient.centre == centreObject
        assert appointmentProvider != None
        assert appointmentProvider.date == date
        assert appointmentProvider.time == datetime.datetime.strptime(time, '%H:%M:%S').time()
        assert appointmentProvider.visit_reason == reason
        assert appointmentProvider.notes == ""
        assert appointmentProvider.medication == ""
        assert appointmentProvider.completed == False
        assert appointmentProvider.patient == patientObject
        assert appointmentProvider.provider == providerObject
        assert appointmentProvider.centre == centreObject
        assert len(searchResults) == 0

    def test_wrong_doc_view_history(self):
        print("testing wrong doctor access to patient history")

        time = '13:30:00'
        date = '2018-10-20'
        reason = 'cold'
        current_user = system.find_patient('Tom Smith')
        patientObject = system.find_patient('Tom Smith')
        providerObject = system.find_provider('Anna Quin')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user != None
        assert patientObject != None
        assert providerObject != None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,5)

        current_user = system.find_provider('Toby Richards')
        assert current_user != None
        assert current_user.is_provider == True
        assert system.has_access(patientObject, current_user) == False

        appointmentProvider = system.find_appt(current_user, 5)
        assert appointmentProvider == None

    def test_view_existing_patient_history(self):
        print("test viewing an existing patient's history")

        time = '09:30:00'
        date = '2018-10-20'
        reason = 'arm problems'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Michael Young')
        centreObject =  system.find_centre('UNSW Health Service')

        assert current_user != None
        assert patientObject != None
        assert providerObject != None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,6)

        notes = "Need x-ray for arm"
        meds = "Some panadol to relieve symptoms"

        appointmentPatient = system.find_appt(patientObject, 6)
        appointmentProvider = system.find_appt(providerObject, 6)
        system.update_appt(appointmentProvider, appointmentPatient, notes, meds)

        assert appointmentPatient.completed == True
        assert appointmentProvider.completed == True

        new_time = '10:00:00'
        new_date = '2018-10-25'
        new_reason = 'arm x-ray'
        newProviderObject = system.find_provider('Ian Ho')
        newCentreObject = system.find_centre('Sydney Children Hospital')

        assert newProviderObject != None
        assert newCentreObject != None

        system.add_appointment(newProviderObject, current_user, new_date, new_time, new_reason, patientObject, newCentreObject, 7)

        current_user = system.find_provider('Ian Ho')
        assert current_user != None
        assert current_user.is_provider == True
        assert system.has_access(patientObject, current_user) == True

        searchResults = patientObject.appointments.search_appointment(True)
        assert len(searchResults) == 1

        pastAppointment = searchResults[0]

        assert pastAppointment.date == date
        assert pastAppointment.time == datetime.datetime.strptime(time, '%H:%M:%S').time()
        assert pastAppointment.visit_reason == reason
        assert pastAppointment.notes == notes
        assert pastAppointment.medication == meds
        assert pastAppointment.completed == True
        assert pastAppointment.patient == patientObject
        assert pastAppointment.provider == providerObject
        assert pastAppointment.centre == centreObject
        assert pastAppointment.id == 6

    def test_view_patient_history_another_centre(self):
        print("testing viewing a patient's history when patient books same provider at a different centre")

        old_time = '09:30:00'
        old_date = '2018-10-20'
        old_reason = 'leg problems'
        current_user = system.find_patient('Tom Smith')
        patientObject = system.find_patient('Tom Smith')
        oldProviderObject = system.find_provider('Anna Quin')
        oldCentreObject =  system.find_centre('UTS Health Service')

        assert current_user != None
        assert patientObject != None
        assert oldProviderObject != None
        assert oldCentreObject != None

        system.add_appointment(oldProviderObject,current_user,old_date,old_time,old_reason,patientObject,oldCentreObject,8)

        old_notes = "Need x-ray for leg"
        old_meds = "Some panadol to relieve symptoms"

        appointmentPatient = system.find_appt(patientObject, 8)
        appointmentProvider = system.find_appt(oldProviderObject, 8)
        system.update_appt(appointmentProvider, appointmentPatient, old_notes, old_meds)

        assert appointmentPatient.completed == True
        assert appointmentProvider.completed == True

        new_time = '10:00:00'
        new_date = '2018-10-25'
        new_reason = 'leg x-ray'
        newProviderObject = system.find_provider('Ian Ho')
        newCentreObject = system.find_centre('Sydney Children Hospital')

        assert newProviderObject != None
        assert newCentreObject != None

        system.add_appointment(newProviderObject, current_user, new_date, new_time, new_reason, patientObject, newCentreObject, 9)

        new_notes = "x-rayed leg"
        new_meds = "more panadol"

        appointmentPatient = system.find_appt(patientObject, 9)
        appointmentProvider = system.find_appt(newProviderObject, 9)
        system.update_appt(appointmentProvider, appointmentPatient, new_notes, new_meds)
        
        assert appointmentPatient.completed == True
        assert appointmentProvider.completed == True

        time = '16:30:00'
        date = '2018-10-30'
        reason = 'check x-ray scans'
        providerObject = system.find_provider('Anna Quin')
        centreObject = system.find_centre('Prince of Wales Hospital')

        assert providerObject != None
        assert centreObject != None

        system.add_appointment(providerObject, current_user, date, time, reason, patientObject, centreObject, 10)

        current_user = system.find_provider('Anna Quin')
        assert current_user != None
        assert current_user.is_provider == True
        assert system.has_access(patientObject, current_user) == True

        searchResults = patientObject.appointments.search_appointment(True)
        assert len(searchResults) == 2

        oldAppointment = searchResults[0]
        newAppointment = searchResults[1]

        assert oldAppointment.date == old_date
        assert oldAppointment.time == datetime.datetime.strptime(old_time, '%H:%M:%S').time()
        assert oldAppointment.visit_reason == old_reason
        assert oldAppointment.notes == old_notes
        assert oldAppointment.medication == old_meds
        assert oldAppointment.completed == True
        assert oldAppointment.patient == patientObject
        assert oldAppointment.provider == oldProviderObject
        assert oldAppointment.centre == oldCentreObject
        assert oldAppointment.id == 8
        assert newAppointment.date == new_date
        assert newAppointment.time == datetime.datetime.strptime(new_time, '%H:%M:%S').time()
        assert newAppointment.visit_reason == new_reason
        assert newAppointment.notes == new_notes
        assert newAppointment.medication == new_meds
        assert newAppointment.completed == True
        assert newAppointment.patient == patientObject
        assert newAppointment.provider == newProviderObject
        assert newAppointment.centre == newCentreObject
        assert newAppointment.id == 9
    
    def test_completed_appointment_view_patient_history(self):
        print("testing viewing patient history after appointment completed")

        time = '09:30:00'
        date = '2018-10-20'
        reason = 'arm problems'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Sid Mallya')
        centreObject =  system.find_centre('Royal Prince Alfred Hospital')

        assert current_user != None
        assert patientObject != None
        assert providerObject != None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,12)
        
        current_user = system.find_provider('Sid Mallya')
        assert current_user != None
        assert current_user.is_provider == True
        assert system.has_access(patientObject, current_user) == True

        notes = "Need x-ray for arm"
        meds = "Some panadol to relieve symptoms"

        appointmentPatient = system.find_appt(patientObject, 12)
        appointmentProvider = system.find_appt(providerObject, 12)
        system.update_appt(appointmentProvider, appointmentPatient, notes, meds)

        assert appointmentPatient.completed == True
        assert appointmentProvider.completed == True
        assert system.has_access(patientObject, current_user) == False 


class TestManageHistory(object):
    #the front end takes care if a patient tries to access the start/edit appt page
    def test_add_notes_and_meds(self):
        print("testing adding notes and meds to an appointment")

        time = '09:00:00'
        date = '2018-10-20'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,2)

        notes="the patient had a flu due to the weather changes"
        meds="Some panadol to relive symptoms"

        appointmentPatient = system.find_appt(patientObject,2)
        appointmentProvider = system.find_appt(providerObject,2)
        system.update_appt(appointmentProvider,appointmentPatient,notes,meds)

        assert appointmentPatient.notes==notes
        assert appointmentPatient.medication==meds
        assert appointmentPatient.completed==True
        assert appointmentProvider.notes==notes
        assert appointmentProvider.medication==meds
        assert appointmentProvider.completed==True

    def test_add_notes_only(self):
        print("testing adding notes only to an appointment")

        time = '09:00:00'
        date = '2018-10-23'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,3)

        notes="the patient had a flu due to the weather changes"
        meds=""

        appointmentPatient = system.find_appt(patientObject,3)
        appointmentProvider = system.find_appt(providerObject,3)

        system.update_appt(appointmentProvider,appointmentPatient,notes,meds)

        assert appointmentPatient.notes==notes
        assert appointmentPatient.medication==meds
        assert appointmentPatient.completed==True
        assert appointmentProvider.notes==notes
        assert appointmentProvider.medication==meds
        assert appointmentProvider.completed==True

    def test_add_nothing(self):
        print("testing adding nothing to an appointment")

        time = '09:00:00'
        date = '2018-11-11'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,4)

        notes=""
        meds=""

        appointmentPatient = system.find_appt(patientObject,4)
        appointmentProvider = system.find_appt(providerObject,4)

        system.update_appt(appointmentProvider,appointmentPatient,notes,meds)

        assert appointmentPatient.notes==notes
        assert appointmentPatient.medication==meds
        assert appointmentPatient.completed==True
        assert appointmentProvider.notes==notes
        assert appointmentProvider.medication==meds
        assert appointmentProvider.completed==True

    def test_wrong_doc_starting_appt(self):
        print("testing wrong doctor access and adding to appointment")

        time = '09:00:00'
        date = '2018-11-20'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        wrongDoc = system.find_provider('Gary Chen')

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,5)

        appointmentPatient = system.find_appt(patientObject,5)
        appointmentProvider = system.find_appt(wrongDoc,5)

        assert appointmentPatient != None
        assert appointmentProvider == None

    def test_add_meds_only(self):
        print("testing adding meds only to an appointment")

        time = '09:00:00'
        date = '2018-12-25'
        reason = 'cold'
        current_user = system.find_patient('Jack Ryan')
        patientObject = system.find_patient('Jack Ryan')
        providerObject = system.find_provider('Toby Richards')
        centreObject =  system.find_centre('Sydney Children Hospital')

        assert current_user!=None
        assert patientObject!=None
        assert providerObject!=None
        assert centreObject != None

        system.add_appointment(providerObject,current_user,date,time,reason,patientObject,centreObject,6)

        notes=""
        meds="panadol"

        appointmentPatient = system.find_appt(patientObject,6)
        appointmentProvider = system.find_appt(providerObject,6)

        system.update_appt(appointmentProvider,appointmentPatient,notes,meds)

        assert appointmentPatient.notes==notes
        assert appointmentPatient.medication==meds
        assert appointmentPatient.completed==True
        assert appointmentProvider.notes==notes
        assert appointmentProvider.medication==meds
        assert appointmentProvider.completed==True