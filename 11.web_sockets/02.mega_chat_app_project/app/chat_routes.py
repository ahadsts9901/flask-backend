from flask import Blueprint, jsonify
from .middleware import jwt_required, role_required
from .models import User

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/users', methods=['GET'])
@jwt_required


