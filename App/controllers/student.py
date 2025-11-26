# App/controllers/student.py
from App.models import Student, Position, Application, Shortlist
from App.database import db


# 1. APPLY FOR A POSITION
def apply_for_position(student_id, position_id):

    student = Student.query.filter_by(id=student_id).first()
    position = Position.query.filter_by(id=position_id).first()

    if not student or not position:
        return {"error": "Student or position not found"}, 404

    # Prevent duplicate applications
    existing = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if existing:
        return {"error": "Already applied"}, 400

    # Create Application (state = applied)
    app = Application(student_id=student_id, position_id=position_id)
    db.session.add(app)
    db.session.commit()

    return app.__repr__(), 201


# 2. VIEW ALL APPLICATIONS (Track Stage)
def get_student_applications(student_id):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return {"error": "Student not found"}, 404

    apps = Application.query.filter_by(student_id=student_id).all()
    return [{
        "application_id": a.id,
        "position_id": a.position_id,
        "status": a.status
    } for a in apps], 200


# 3. VIEW SHORTLISTED POSITIONS
def get_student_shortlisted_positions(student_id):

    entries = Shortlist.query.filter_by(student_id=student_id).all()

    return [{
        "shortlist_id": s.id,
        "position_id": s.position_id,
        "staff_id": s.staff_id,
        "status": s.status
    } for s in entries], 200


# 4. VIEW STATUS OF A SPECIFIC APPLICATION
def get_application_status(student_id, position_id):

    app = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if not app:
        return {"error": "Application not found"}, 404

    return {"status": app.status}, 200


# 5. UPDATE STUDENT PROFILE (Optional)
def update_student_profile(student_id, gpa=None, resume=None):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return {"error": "Student not found"}, 404

    if gpa is not None:
        student.gpa = gpa
    if resume is not None:
        student.resume = resume

    db.session.commit()
    return {"message": "Profile updated"}, 200


# 6. FILTER POSITIONS STUDENT IS ELIGIBLE FOR 
def get_eligible_positions_for_student(student_id):

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return {"error": "Student not found"}, 404

    positions = Position.query.all()
    eligible = []

    for p in positions:
        if p.gpa_requirement is None or student.gpa >= p.gpa_requirement:
            eligible.append(p.toJSON())

    return eligible, 200
