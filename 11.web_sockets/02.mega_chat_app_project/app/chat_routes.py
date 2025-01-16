from flask import Blueprint, jsonify, request
from .middleware import jwt_required, role_required
from .models import User, Chat
from datetime import datetime, timedelta

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/message', methods=['POST'])
@jwt_required
def create_message():
    try:
        data = request.json
        if not data:
            return jsonify({'message': 'data is required'}), 400
        if 'to_id' not in data:
            return jsonify({'message': 'to_id is required'}), 400
        if 'message' not in data:
            return jsonify({'message': 'text message is required'}), 400
        
        from_id = request.current_user["id"]
        to_id = data["to_id"]
        message = data["message"]

        new_message = Chat(
            from_id=from_id,
            to_id=to_id,
            message=message,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        new_message.save()
        return jsonify({'message': 'message sent successfully'}), 200
    
    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)}), 500
    
