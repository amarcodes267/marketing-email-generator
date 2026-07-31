from flask import Blueprint, request, jsonify
from utils.validator import validate_email_request
from services.email_service import generate_email

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

    result = generate_email(data)

    return jsonify(result), 200
