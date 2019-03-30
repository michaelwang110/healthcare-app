class RatingManager:
    def __init__(self):
        self._ratings={}

    def add_rating(self,patient,rating):
        self._ratings[patient]=int(rating)

    def calculate_average(self):
        total=0
        counter=0
        if len(self._ratings)==0:
            return None
        for i in list(self._ratings.values()):
            total+=i
            counter+=1
        return round(total/counter, 2)
        
