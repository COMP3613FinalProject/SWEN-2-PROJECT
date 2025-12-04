""" Shortlist endpoints
Routes (blueprint url_prefix='/shortlist'):
- POST      /api/shortlist/add               -> add to shortlist
- GET       /api/shortlist/student/<id>      -> shortlist entries for a student
- GET       /api/shortlist/position/<id>     -> shortlist entries for a position"""


from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import ( add_student_to_shortlist, get_shortlist_by_student, get_shortlist_by_position)


shortlist_views = Blueprint('shortlist_views', __name__, url_prefix='/api/shortlist')

#Add student to shortlist
@shortlist_views.route('/', methods = ['POST'])
@jwt_required()
def add_student_shortlist():
     identity = get_jwt_identity()
     data = request.get_json() or {}
     student_id = data.get("student_id")
     position_id = data.get("position_id")
     if not student_id or not position_id:
          return jsonify({"error": "student_id and position_id are required"}), 400
     
     result = add_student_to_shortlist(student_id = student_id,
                                       position_id = position_id,
                                       staff_id = identity["id"])

     if not result:
          return jsonify({"error": "Failed to add to shortlist"}), 400

     return jsonify(result.toJSON()), 200
     
     

@shortlist_views.route('/student/<int:student_id>', methods = ['GET'])
@jwt_required()
def get_student_shortlist(student_id):
    
    shortlists = get_shortlist_by_student(student_id)
    if not shortlists:
         return jsonify({"message": "No listings available"}), 404
         return jsonify([s.toJSON() for s in shortlists]), 200
    

@shortlist_views.route('/api/shortlist/position/<int:position_id>', methods=['GET'])
@jwt_required()
def get_position_shortlist(position_id):
     
     shortlists = get_shortlist_by_position(position_id)
     if not shortlists:
          return jsonify({"message": "No listings available"}), 404
     return jsonify([s.toJSON() for s in shortlists]), 200 
     
