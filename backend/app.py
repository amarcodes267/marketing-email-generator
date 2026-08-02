import os

from flask import Flask, render_template
from flask_cors import CORS

from config import get_config
from routes.email_routes import email_bp

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))


def create_app():
    app = Flask(
        __name__,
        template_folder=FRONTEND_DIR,
        static_folder=FRONTEND_DIR,
        static_url_path="",
    )
    app.config.from_object(get_config())
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(email_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])

