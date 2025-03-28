from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from MainTranslate import translate_text
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    async_mode='threading'
)

# User storage
users = {}
connections = {}

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = next((k for k, v in connections.items() if v == request.sid), None)
    if user_id:
        del connections[user_id]
        print(f"User disconnected: {user_id}")

@socketio.on('register')
def handle_register(data):
    user_id = data.get('user_id')
    language = data.get('language')
    if user_id and language:
        users[user_id] = {'language': language, 'status': 'online'}
        connections[user_id] = request.sid
        print(f"User {user_id} registered (SID: {request.sid})")
        emit('registration_success', {'status': 'registered'})

@socketio.on('send_message')
def handle_message(data):
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    message = data.get('message')
    
    if not all([sender_id, recipient_id, message]):
        emit('error', {'message': 'Missing required fields'})
        return
    
    if recipient_id not in users:
        emit('error', {'message': 'Recipient not found'}, room=connections.get(sender_id))
        return
    
    target_language = users[recipient_id]['language']
    translated_text, detected_language = translate_text(message, target_language)
    
    if not translated_text:
        emit('error', {'message': 'Translation failed'}, room=connections.get(sender_id))
        return
    
    message_data = {
        'from': sender_id,
        'original_message': message,
        'translated_message': translated_text,
        'original_language': detected_language,
        'translated_language': target_language,
        'timestamp': datetime.now().isoformat()
    }
    
    if recipient_id in connections:
        emit('receive_message', message_data, room=connections[recipient_id])
    
    emit('message_sent', {'status': 'success'}, room=connections[sender_id])

# VOIP handlers
@socketio.on('offer')
def handle_offer(data):
    recipient_id = data.get('to')
    if recipient_id in connections:
        emit('offer', data, room=connections[recipient_id])

@socketio.on('answer')
def handle_answer(data):
    recipient_id = data.get('to')
    if recipient_id in connections:
        emit('answer', data, room=connections[recipient_id])

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    recipient_id = data.get('to')
    if recipient_id in connections:
        emit('ice_candidate', data, room=connections[recipient_id])

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=5001,
        debug=True,
        allow_unsafe_werkzeug=True
    )