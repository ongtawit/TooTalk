import socketio
import json
from MainTranslate import translate_text, SUPPORTED_LANGUAGES
import threading
import pyaudio
import time

# Audio configuration for VOIP
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class ChatClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.user_id = None
        self.language = None
        self.recipient = None
        self.audio_stream = None
        self.audio_running = False
        
        # Setup event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('receive_message', self.on_message)
        self.sio.on('offer', self.handle_offer)
        self.sio.on('answer', self.handle_answer)
        self.sio.on('ice_candidate', self.handle_ice_candidate)
        
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        
    def on_connect(self):
        print("Connected to server")
        
    def on_disconnect(self):
        print("Disconnected from server")
        
    def on_message(self, data):
        print(f"\n[Message from {data['from']}]")
        print(f"Original ({data['original_language']}): {data['original_message']}")
        print(f"Translated ({data['translated_language']}): {data['translated_message']}")
        
    def handle_offer(self, data):
        print("\nIncoming call from", data['from'])
        answer = input("Accept call? (y/n): ").lower()
        if answer == 'y':
            # In a real app, we'd set up WebRTC here
            print("Call connected (simulated)")
            self.start_audio_stream()
        else:
            print("Call declined")
            
    def handle_answer(self, data):
        print("Call answered by recipient")
        self.start_audio_stream()
        
    def handle_ice_candidate(self, data):
        pass  # Would handle ICE candidates in a real WebRTC implementation
        
    def start_audio_stream(self):
        if self.audio_running:
            return
            
        self.audio_running = True
        self.audio_stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK
        )
        
        print("Audio streaming started (simulated)")
        
    def stop_audio_stream(self):
        if not self.audio_running:
            return
            
        self.audio_running = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        print("Audio streaming stopped")
        
    def connect(self, server_url):
        self.sio.connect(server_url)
        
    def register(self, user_id, language):
        self.user_id = user_id
        self.language = language
        self.sio.emit('register_socket', {'user_id': user_id})
        
    def send_message(self, recipient_id, message):
        self.sio.emit('send_message', {
            'sender_id': self.user_id,
            'recipient_id': recipient_id,
            'message': message
        })
        
    def start_call(self, recipient_id):
        print(f"Calling {recipient_id}...")
        self.sio.emit('offer', {
            'from': self.user_id,
            'to': recipient_id,
            'sdp': 'simulated_sdp_offer'  # In real app, would be WebRTC offer
        })
        
    def end_call(self):
        self.stop_audio_stream()
        print("Call ended")

def main():
    print("Welcome to TransChat!")
    print("Supported languages:")
    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"{code}: {name}")
        
    server_url = input("Enter server URL (e.g., http://localhost:5001): ")
    user_id = input("Enter your user ID: ")
    language = input("Enter your language code: ")
    
    client = ChatClient()
    client.connect(server_url)
    client.register(user_id, language)
    
    try:
        while True:
            print("\nMenu:")
            print("1. Send message")
            print("2. Start voice call")
            print("3. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == '1':
                recipient = input("Enter recipient ID: ")
                message = input("Enter your message: ")
                client.send_message(recipient, message)
            elif choice == '2':
                recipient = input("Enter recipient ID: ")
                client.start_call(recipient)
            elif choice == '3':
                break
            else:
                print("Invalid choice")
                
    except KeyboardInterrupt:
        pass
    finally:
        client.sio.disconnect()

if __name__ == "__main__":
    main()