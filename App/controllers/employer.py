from App.models.employer import Employer
from App.database import db
from App.models import Student, Shortlist, Position
from App.controllers.user import *
from App.models.application import Application

def create_employer(username, password, email, company, phone_number):
  newEmployer = Employer(username, password, email, company, phone_number)
  db.session.add(newEmployer)
  db.session.commit()
  print(f"Employer '{newEmployer.id}' created successfully!")
  return newEmployer

def decide_shortlist(student_id, position_id, decision):

    student = Student.query.get(student_id)
    position = Position.query.get(position_id)

    if not student or not position:
        return False

    application = Application.query.filter_by(
        student_id=student.id,
        position_id=position.id
    ).first()

    if not application:
        return False

    shortlist = Shortlist.query.filter_by(
        application_id=application.id,
        isWithdrawn=False
    ).first()

    if not shortlist:
        return False

    # Position Fixexit()
    if decision == "accept":
        if position.number_of_positions <= 0:
            print("No available positions.")
            return False
        
        # Consume one slot for accept
        position.number_of_positions -= 1

    # Reject does NOT consume slot

    # Move to next stage in state machine
    shortlist.application.next(decision)

    db.session.commit()
    return shortlist
