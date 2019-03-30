from models.Centre import *
from models.methods.Search import match

class CentreManager:
    def __init__(self):
        self._centres=[]
    def add_centre(self,centre):
        self._centres.append(centre)
    def search_centre(self,suburb,name,string):
        search_results=[]
        if suburb:
            for i in self._centres:
                if match(i.suburb,string):
                    search_results.append(i)
        elif name:
            for i in self._centres:
                if match(i.centre_name,string):
                    search_results.append(i)
        return search_results
    @property
    def centres(self):
        return self._centres
