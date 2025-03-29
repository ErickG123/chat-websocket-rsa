from rsa import generate_keys, encrypt, decrypt
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio.init_app(app)

    @app.route("/")
    def index():
        public_key, private_key = generate_keys()

        return render_template("index.html", public_key=public_key, private_key=private_key)
    
    @socketio.on("encrypt_message")
    def encrypt_message(data):
        message_to_encrypt = data.get("message")
        public_key_str = data.get("publicKey")

        public_key_str = public_key_str.strip("()")
        e, n = map(int, public_key_str.split(","))
        public_key = (e, n)

        encrypted_message = encrypt(message_to_encrypt, public_key)

        socketio.emit("encryptedMessage", encrypted_message)

    @socketio.on("decrypt_message")
    def decrypt_message(data):
        message_to_decrypt = data.get("message")
        private_key_str = data.get("privateKey")

        private_key_str = private_key_str.strip("()")
        e, n = map(int, private_key_str.split(","))
        private_key = (e, n)

        decrypted_message = decrypt(message_to_decrypt, private_key)

        socketio.emit("decryptedMessage", decrypted_message)

    return app

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, "0.0.0.0", 5000, debug=True)
