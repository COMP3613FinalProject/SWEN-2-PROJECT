from App import db
from App.models.context import Context
from App.models.applied_state import AppliedState

class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    status = db.Column(db.String(10), default="applied", nullable=False)

    def __init__(self, student_id, position_id, status="applied"):
        self.student_id = student_id
        self.position_id = position_id
        self.context = Context(AppliedState())
        self.status = AppliedState.getStateName()

    def getStatus(self):
        return self.status

    def setStatus(self, newStatus:str):
        self.status = newStatus
        db.session.commit()

    def __repr__(self):
        return f'<Application id: {self.id} - Student ID: {self.student_id} - Position ID: {self.position_id} - Status: {self.status}>'
