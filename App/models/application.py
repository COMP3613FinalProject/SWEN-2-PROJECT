from App.database import db


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
        

    def next(self, decision=None):
        """Move to next state."""
        return self.state.next(self, decision)

    def previous(self):
        return self.state.previous(self)

    def withdraw(self):
        return self.state.withdraw(self)

    
    def set_state(self, new_state):
        self.state = new_state
        self.status = new_state.name  # THIS UPDATES THE STATUS
        db.session.add(self)
        db.session.commit()

    def getStatus(self):
        return self.status

    def __repr__(self):
        return f"<Application {self.id} - Status: {self.status}>"
