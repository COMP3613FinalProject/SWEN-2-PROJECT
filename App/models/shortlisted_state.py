from App.models.application_state import ApplicationState
from App.models.applied_state import AppliedState
from App.models.accepted_state import AcceptedState
from App.models.rejected_state import RejectedState
from App.models.application import Application

class ShortListedState(ApplicationState):
    def __init__(self):
        super().__init__("Shortlisted")

    def next(self):
        return None
    
    def next_decision(self, decision: str): #Accepts decision from make_decision() in employer controller
        if decision == "accept":
            self.context.setState(AcceptedState())
        elif decision == "rejected":
            self.context.setState(RejectedState())

    def previous(self):
        if self.context:
            self.context.setState(AppliedState())

    def withdraw(self):
        self.context.setState(RejectedState())
        #application.setStatus("Withdrawn")

    def getMatchedCompanies(self):
        super().getMatchedCompanies()