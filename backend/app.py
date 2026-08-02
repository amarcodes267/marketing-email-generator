import os

from flask import Flask, jsonify, render_template
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

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"success": False, "message": "Endpoint not found."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"success": False, "message": "Method not allowed."}), 405

    @app.errorhandler(413)
    def handle_request_entity_too_large(error):
        return jsonify({"success": False, "message": "Request body is too large."}), 413

    @app.errorhandler(415)
    def handle_unsupported_media_type(error):
        return jsonify({"success": False, "message": "Content-Type must be application/json."}), 415

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        app.logger.exception(error)
        return jsonify({"success": False, "message": "Unexpected server error. Please try again."}), 500

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])

