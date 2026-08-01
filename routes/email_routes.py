from flask import Blueprint, jsonify, request

from services.email_service import generate_email
from utils.validator import validate_email_request

email_bp = Blueprint("email", __name__)


@email_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "Marketing Copy AI Backend Running"}), 200


@email_bp.route("/generate-email", methods=["POST"])
def generate_email_route():
    data = request.get_json(silent=True)

    validation = validate_email_request(data)

    if not validation["valid"]:
        first_error = validation["errors"][0]
        return jsonify({"success": False, "message": first_error["message"]}), 400

    try:
        result = generate_email(data)
    except ValueError as error:
        return jsonify({"success": False, "message": str(error)}), 400
    except Exception as error:
        return jsonify({"success": False, "message": f"Unexpected server error: {error}"}), 500

    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code
