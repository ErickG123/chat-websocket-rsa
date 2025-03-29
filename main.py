from rsa import generate_keys, encrypt, decrypt
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO(cors_allowed_origins="*")

user_keys = {}

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @socketio.on("connect")
    def handle_connect():
        public_key, private_key = generate_keys()
        user_keys[request.sid] = public_key

        socketio.emit("update_users", user_keys)

        socketio.emit("public_key", {
            "socket_id": request.sid,
            "public_key": public_key,
            "private_key": str(private_key)
        }, room=request.sid)

    @socketio.on("disconnect")
    def handle_disconnect():
        if request.sid in user_keys:
            del user_keys[request.sid]

        socketio.emit("update_users", user_keys)

    @socketio.on("encrypt_message")
    def encrypt_message(data):
        message_to_encrypt = data.get("message")
        recipient_id = data.get("recipient_id")

        if recipient_id not in user_keys:
            return
        
        public_key = user_keys[recipient_id]

        encrypted_message = encrypt(message_to_encrypt, public_key)

        socketio.emit("encrypted_message", {
            "sender": request.sid,
            "ciphertext": ",".join(map(str, encrypted_message))
        }, room=recipient_id)

    @socketio.on("decrypt_message")
    def decrypt_message(data):
        message_to_decrypt = data.get("message")
        private_key_str = data.get("privateKey")

        private_key_str = private_key_str.strip("()")
        d, n = map(int, private_key_str.split(","))
        private_key = (d, n)

        decrypted_message = decrypt(message_to_decrypt, private_key)

        socketio.emit("decrypted_message", decrypted_message, room=request.sid)

    return app

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, "0.0.0.0", 5000, debug=True)
