from models.User import *
from models.methods.Search import match

class UserManager:
    def __init__(self):
        self._users = []

    # add a new user to UserManager
    def add_user(self, user):
        self._users.append(user)

    # verify user login
    def verify_user(self, email, password):
        for user in self._users:
            if user.email == email and user.password == password:
                return True
        return False

    # search for a Provider
    def search_provider(self, service, name, search):
        search_results = []
        for i in self._users:
            # skip patient users
            if not i.is_provider:
                continue
            # add user to search result if matches search
            if service:
                if match(i.service, search):
                    search_results.append(i)
            elif name:
                if match(i.full_name, search):
                    search_results.append(i)
        return search_results
    @property
    def users(self):
        return self._users

    def providers(self):
        results=[]
        for i in self._users:
            if i.is_provider:
                results.append(i)
        return results
