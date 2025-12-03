#SHORTLISTED

from App.models.application_state import ApplicationState

class ShortListedState(ApplicationState):
    def __init__(self):
        super().__init__("Shortlisted")


    def next(self, app, decision=None):
        if decision is None:
            return None

        if decision == "accept":
            from App.models.accepted_state import AcceptedState
            app.set_state(AcceptedState())

        elif decision == "reject":
            from App.models.rejected_state import RejectedState
            app.set_state(RejectedState())
    
    def previous(self, app):
        from App.models.applied_state import AppliedState
        app.set_state(AppliedState())

    def withdraw(self, app):
        # Student withdraws: move to rejected
        from App.models.rejected_state import RejectedState
        app.set_state(RejectedState())

    def getMatchedCompanies(self, app):
        """Return all Shortlisted applications for the same student."""
        from App.models.application import Application

        student_id = app.student_id

        shortlisted = Application.query.filter_by(
            student_id=student_id,
            status="Shortlisted"
        ).all()

        return [repr(a) for a in shortlisted]
