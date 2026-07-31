from flask import Flask
from flask_cors import CORS
from routes.email_routes import email_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(email_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
