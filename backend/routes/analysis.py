from flask import Blueprint, request, jsonify, current_app
from ..analyzer.analyzer_service import AnalyzerService

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/analyze", methods=["POST"], strict_slashes=False)
def analyze_endpoint():
    """
    POST /api/analyze
    Analyzes Python source code statically without execution.
    """
    # 1. Validate JSON payload
    if not request.is_json:
        return jsonify({
            "status": "error",
            "error": "Request body must be valid JSON with Content-Type application/json."
        }), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({
            "status": "error",
            "error": "Invalid or malformed JSON in request body."
        }), 400

    # 2. Validate 'code' field
    if "code" not in data:
        return jsonify({
            "status": "error",
            "error": "Missing required field 'code' in request body."
        }), 400

    code = data.get("code")
    if not isinstance(code, str):
        return jsonify({
            "status": "error",
            "error": "The 'code' field must be a string."
        }), 400

    # 3. Validate size limits
    max_length = current_app.config.get("MAX_SOURCE_LENGTH", 100_000)
    if len(code) > max_length:
        return jsonify({
            "status": "error",
            "error": f"Submitted code exceeds maximum size limit of {max_length} characters ({len(code)} characters received)."
        }), 413

    # 4. Perform static analysis
    try:
        service = current_app.analyzer_service
        result = service.analyze_code(code)
        return jsonify(result), 200
    except Exception as exc:
        current_app.logger.error("Unexpected error during analysis: %s", str(exc))
        return jsonify({
            "status": "error",
            "error": "An internal server error occurred during static analysis."
        }), 500
