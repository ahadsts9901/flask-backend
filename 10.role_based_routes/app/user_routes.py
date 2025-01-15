from flask import Blueprint, request, jsonify
from middleware import jwt_required
from models import User

user_bp = Blueprint('user', __name__)

# Get current user profile
@user_bp.route('/profile', methods=['GET'])
@jwt_required
def get_current_user_profile():
    user_id = request.current_user['id']
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'message': 'user not found'}), 404

    return jsonify({
        'message': 'profile fetched',
        'data': {
            'id': str(user.id),
            'username': user.username,
            'profile_picture': user.profile_picture,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
    }), 200
