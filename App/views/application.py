from flask import Blueprint, request, jsonify
from App.models import Application, Student, Position
from App.database import db

application_views = Blueprint('application_views', __name__)


# 1. CREATE APPLICATION
@application_views.route('/api/application/create', methods=['POST'])
def api_create_application():
    data = request.get_json()

    student_id = data.get("student_id")
    position_id = data.get("position_id")

    # Validate student
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Validate position
    position = Position.query.get(position_id)
    if not position:
        return jsonify({"error": "Position not found"}), 404

    # Check for duplicate
    existing = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if existing:
        return jsonify({"error": "Duplicate application"}), 409

    # Create new Application (starts in Applied state)
    new_app = Application(student_id=student_id, position_id=position_id)
    db.session.add(new_app)
    db.session.commit()

    return jsonify({
        "message": "Application created successfully.",
        "application_id": new_app.id,
        "student_id": new_app.student_id,
        "position_id": new_app.position_id,
        "status": new_app.getStatus(),
    }), 201


# 2. PREVENT DUPLICATE CHECK
@application_views.route('/api/application/check-duplicate', methods=['POST'])
def api_check_duplicate_application():
    data = request.get_json()

    student_id = data.get("student_id")
    position_id = data.get("position_id")

    existing = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if existing:
        return jsonify({"duplicate": True}), 200

    return jsonify({"duplicate": False}), 200


# 3. GET APPLICATION STATUS
@application_views.route('/api/application/status/<int:student_id>/<int:position_id>')
def api_application_status(student_id, position_id):

    app = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if not app:
        return jsonify({"error": "Application not found"}), 404

    return jsonify({
        "application_id": app.id,
        "status": app.getStatus()
    }), 200


# 4. GET ALL APPLICATIONS
@application_views.route('/api/applications/<int:student_id>')
def api_get_all_applications(student_id):

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    apps = Application.query.filter_by(student_id=student_id).all()

    return jsonify([
        {
            "application_id": a.id,
            "position_id": a.position_id,
            "status": a.status
        } for a in apps
    ]), 200
