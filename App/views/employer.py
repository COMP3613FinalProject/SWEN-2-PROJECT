''' Employer related REST endpoints

Routes (blueprint url_prefix='/employer'):
- POST   /employer/           -> create employer
- POST   /employer/accept     -> employer accepts a shortlisted student (auth)
'''

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import(
    create_employer,
    decide_shortlist
)

employer_views = Blueprint('employer', __name__, url_prefix='/employer')

#Create employer
@employer_views.route('/', methods=['POST'])
def create_employer_route():
  """Create a new employer
  Body JSON: { username, password, email, company, phone_number } """
  data = request.get_json() or {}
  required = ['username', 'password', 'email', 'company', 'phone_number']
  if not all(k in data for k in required):
    return jsonify({"error": "Missing fields"}), 400

  emp = create_employer(data['username'],
                        data['password'],
                        data['email'],
                        data['company'],
                        data['phone_number'])
  return jsonify({"message": "Employer created", "id":emp.id}), 201

#Employer - accept student
@employer_views.route('/accept', methods=['POST'])
@jwt_required()
def employer_accept_route():
  """Employer accepts a shortlisted student
  Body JSON: {"student_id": <int>, "position_id": <int>, "response": "Accepted"}
  The employer_id is taken from the JWT identity (current user)"""
    
  data = request.get_json() or {}
  student_id = data.get("student_id")
  position_id = data.get("position_id")
  if not student_id or not position_id: #Validation
    return jsonify({"error": "student_id and position_id required"}), 400

  decision = "accept" #decision is always accept for this route
  result = decide_shortlist(student_id, position_id, decision)
  if not result:
    return jsonify({"error": "Unable to accept student. Check eligibility, shortlist status or position availability"}), 400

  return jsonify({
        "message": "Student accepted successfully",
        "listing": {
            "id": result.id,
            "internship_id": position_id,
            "student_id": student_id,
            "status": "accepted"
        }
    }), 200
