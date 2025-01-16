from app import create_app
from flask_socketio import SocketIO, join_room, emit

app = create_app()
socketio = SocketIO(app, cors_allowed_origins= "*")

@socketio.on('join')
def on_join(data):
    user_id = data.get('user_id')
    if user_id:
        room = f'message-{user_id}'
        join_room(room)
        emit('status', {'message': f'User {user_id} has joined {room}.'}, to=room)

if __name__ == "__main__":
    socketio.run(app, debug=True)
