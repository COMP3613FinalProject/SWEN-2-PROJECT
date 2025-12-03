''' Employer related REST endpoints

Routes (blueprint url_prefix='/employer'):
- POST   /employer/reject     -> employer rejects a shortlisted student (auth)
'''

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import(
    create_employer,
    decide_shortlist
)

employer_views = Blueprint('employer', __name__, url_prefix='/employer')

#Employer - reject student
@employer_views.route('/reject', methods=['POST'])
@jwt_required()
def employer_reject_route():
  """Employer rejects a shortlisted student
  Body JSON: {"student_id": <int>, "position_id": <int>, "response": "Rejected"}
  The employer_id is taken from the JWT identity (current user)"""

  data = request.get_json() or {}
  student_id = data.get("student_id")
  position_id = data.get("position_id")
  if not student_id or not position_id:
    return jsonify({"error": "student_id and position_id required"}), 400

  decision = "reject" #decision is always reject for this route
  result = decide_shortlist(student_id, position_id, decision)
  if not result:
    return jsonify({"error": "Unable to reject student."}), 400

  return jsonify({
        "message": "Student rejected - successful",
        "listing": {
            "id": result.id,
            "internship_id": position_id,
            "student_id": student_id,
            "status": "rejected"
        }
    }), 200
