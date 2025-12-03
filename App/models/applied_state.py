from App.models.application_state import ApplicationState
#APPLIED
class AppliedState(ApplicationState):
    def __init__(self):
        super().__init__("Applied")

    def next(self, app):
        # Applied -> Shortlisted
        from App.models.shortlisted_state import ShortListedState
        app.set_state(ShortListedState())

    def previous(self, app):
        return None  # no previous
    
    def reject(self, app):
            from App.models.rejected_state import RejectedState
            app.set_state(RejectedState())

    def withdraw(self, app):
        from App.models.rejected_state import RejectedState
        app.set_state(RejectedState())

    def getMatchedCompanies(self, app):
        return []
