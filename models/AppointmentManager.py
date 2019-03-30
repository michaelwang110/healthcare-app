from models.Appointment import *

class AppointmentManager:

    def __init__(self):
        self._appointments=[]

    def add_appointment(self, appointment):
        self._appointments.append(appointment)

    def search_appointment(self, past):
        results=[]
        for i in self._appointments:
            if past:
                if i.completed:
                    results.append(i)
            else:
                if i.completed==False:
                    results.append(i)
        return results

    @property
    def appointments(self):
        return self._appointments
