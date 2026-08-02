from flask import Blueprint, jsonify, request

from services.email_service import generate_email
from utils.validator import validate_email_request

email_bp = Blueprint("email", __name__)


@email_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"message": "Marketing Copy AI Backend Running"}), 200


@email_bp.route("/generate-email", methods=["POST"])
def generate_email_route():
    if not request.is_json:
        return jsonify({"success": False, "message": "Content-Type must be application/json."}), 415

    if request.content_length and request.content_length > request.max_content_length:
        return jsonify({"success": False, "message": "Request body is too large."}), 413

    data = request.get_json(silent=True)

    validation = validate_email_request(data)

    if not validation["valid"]:
        first_error = validation["errors"][0]
        return jsonify({"success": False, "message": first_error["message"]}), 400

    try:
        result = generate_email(data)
    except ValueError as error:
        return jsonify({"success": False, "message": str(error)}), 400
    except Exception:
        return jsonify({"success": False, "message": "Unexpected server error. Please try again."}), 500

    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code
