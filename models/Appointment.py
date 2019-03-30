class Appointment:
    def __init__(self,date,time, visit_reason, patient, provider, centre,id,completed):
        self._date = date
        self._time = time
        self._visit_reason = visit_reason
        self._notes = ""
        self._medication = ""
        self._completed = completed
        self._patient = patient
        self._provider = provider
        self._centre = centre
        self._id=id

    @property
    def time(self):
        return self._time

    @property
    def date(self):
        return self._date

    @property
    def visit_reason(self):
        return self._visit_reason

    @visit_reason.setter
    def visit_reason(self, reason):
        self._visit_reason=reason

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes=notes

    @property
    def medication(self):
        return self._medication

    @medication.setter
    def medication(self, medication):
        self._medication=medication

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        self._completed=completed

    @property
    def patient(self):
        return self._patient

    @property
    def provider(self):
        return self._provider

    @property
    def centre(self):
        return self._centre

    @property
    def id(self):
        return self._id
