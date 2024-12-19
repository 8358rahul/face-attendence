from flask import Blueprint, jsonify, request
from models.user import User

users_bp = Blueprint('user_routes', __name__) 



@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'], photo=data.get('photo')) 
    new_user.save()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email})
