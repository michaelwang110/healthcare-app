from abc import ABC, abstractmethod
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.AppointmentManager import *
from models.RatingManager import *
from datetime import datetime, date, time
from collections import defaultdict

class User(UserMixin, ABC):
    __id = -1

    def __init__(self, full_name, email, phone_number, password, is_provider):
        self._id = self._generate_id()
        self._full_name = full_name
        self._email = email
        self._phone_number = phone_number
        self._password=password
        self._password_hash = generate_password_hash(password)
        self._is_provider = is_provider
        self._appointments = AppointmentManager()

    def _generate_id(self):
        User.__id += 1
        return User.__id

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def validate_password(self, password):
        return check_password_hash(self._password_hash, password)

    @property
    def full_name(self):
        return self._full_name

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self,email):
        self._email=email

    @property
    def phone_number(self):
        return self._phone_number
    @phone_number.setter
    def phone_number(self,phone):
        self._phone_number=phone

    @property
    def password(self):
        return self._password

    @property
    def appointments(self):
        return self._appointments

    @property
    def is_provider(self):
        return self._is_provider


class Patient(User):
    def __init__(self, full_name, email, phone_number, password, medicare):
        super().__init__(full_name, email, phone_number, password, False)
        self._medicare = medicare

    @property
    def medicare(self):
        return self._medicare
    @medicare.setter
    def medicare(self,number):
        self._medicare=number

    def has_access(self,doctor):
        for i in self._appointments.appointments:
            if i.provider.full_name == doctor.full_name and i.completed==False:
                return True
        return False


class Provider(User):
    def __init__(self, full_name, email, phone_number, password, provider_number, service):
        super().__init__(full_name, email, phone_number, password, True)
        self._provider_number = provider_number
        self._service = service
        self._centre_working_hours = defaultdict(dict)
        self._ratings = RatingManager()

    # add new centre and the associated working hours.
    def add_centre_working_hours(self, centre, start_hour,finish_hour):
        start = time(hour=start_hour,minute=0, second=0, microsecond=0)
        finish =time(hour=finish_hour,minute=0, second=0, microsecond=0)
        self._centre_working_hours[centre]['start'] = start
        self._centre_working_hours[centre]['finish'] = finish

    # return start time at a particular centre
    def centre_start_time(self, centre):
        if centre in self._centre_working_hours:
            return self._centre_working_hours[centre]['start']
        return None

    # return finish time at a particular centre
    def centre_finish_time(self, centre):
        if centre in self._centre_working_hours:
            return self._centre_working_hours[centre]['finish']
        return None

    @property
    def provider_number(self):
        return self._provider_number
    @provider_number.setter
    def provider_number(self,number):
        self._provider_number=number

    @property
    def service(self):
        return self._service

    @property
    def centre_working_hours(self):
        return self._centre_working_hours
