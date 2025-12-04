from App.database import db
from sqlalchemy.orm import reconstructor

class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    state = None  

    def __init__(self, student_id, position_id):
        self.student_id = student_id
        self.position_id = position_id
        # initial state
        from App.models.applied_state import AppliedState
        self.set_state(AppliedState())

    
     # Rebuild state when loaded from DB
    @reconstructor
    def init_on_load(self):
        self.state = self._state_from_status(self.status)

    @staticmethod   # because states are not stored this helps to load the state based on its last status
    def _state_from_status(status):
        from App.models.applied_state import AppliedState
        from App.models.shortlisted_state import ShortListedState
        from App.models.accepted_state import AcceptedState
        from App.models.rejected_state import RejectedState

        mapping = {
            "Applied": AppliedState(),
            "Shortlisted": ShortListedState(),
            "Accepted": AcceptedState(),
            "Rejected": RejectedState(),
        }
        if status not in mapping:
            raise ValueError(f"Invalid application status: {status}")
        return mapping[status]
        

    # ---------- Delegate to State ----------
    def next(self, decision=None):
        """Move to next state."""
        return self.state.next(self, decision)

    def previous(self):
        return self.state.previous(self)

    def withdraw(self):
        return self.state.withdraw(self)

    # ---------- State setter ----------
    def set_state(self, new_state):
        self.state = new_state
        self.status = new_state.name  # THIS UPDATES THE STATUS
        db.session.add(self)
        db.session.commit()

    def getStatus(self):
        return self.status

    def __repr__(self):
        return f"<Application {self.id} - Status: {self.status}>"
