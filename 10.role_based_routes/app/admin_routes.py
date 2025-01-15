from flask import Blueprint, jsonify
from middleware import jwt_required, role_required
from models import User

admin_bp = Blueprint('admin', __name__)

# Admin route to fetch all users
@admin_bp.route('/users', methods=['GET'])
@jwt_required
@role_required('admin')  # Only accessible by admin users
def get_all_users():
    users = User.objects.all()
    return jsonify({
        'message': 'all users fetched',
        'data': [user.to_dict() for user in users]
    }), 200
