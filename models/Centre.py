from models.RatingManager import *
class Centre:
    def __init__(self,name,suburb,abn,phone,type,description):
        self._type=type
        self._centre_name=name
        self._suburb=suburb
        self._phone = phone
        self._description=description
        self._services_providers={}
        self._abn=abn
        self._ratings = RatingManager()

    def __str__(self):
        return "Centre {0} is in {1} and is a {2} with phone number {3}".format(self._centre_name, self._suburb,self._description, self._phone)
    def add_provider_service(self,service,provider):
        if service in self._services_providers:
            self._services_providers[service].append(provider)
        else:
            self._services_providers[service]=[provider]
    @property
    def centre_name(self):
        return self._centre_name

    @property
    def suburb(self):
        return self._suburb

    @property
    def abn(self):
        return self._abn

    @property
    def phone(self):
        return self._phone

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def services_providers(self):
        return self._services_providers
