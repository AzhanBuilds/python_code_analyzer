from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"], strict_slashes=False)
def health_check():
    """Health check endpoint confirming API availability."""
    return jsonify({
        "status": "ok",
        "service": "python-code-analyzer"
    }), 200
