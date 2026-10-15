import os
import sys

# Ensure project root is in sys.path so backend is always importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, jsonify
from flask_cors import CORS

if __package__ is None or __package__ == "":
    from backend.config import Config
    from backend.routes.health import health_bp
    from backend.routes.analysis import analysis_bp
    from backend.analyzer.analyzer_service import AnalyzerService
else:
    from .config import Config
    from .routes.health import health_bp
    from .routes.analysis import analysis_bp
    from .analyzer.analyzer_service import AnalyzerService

def create_app(config_class=Config):
    """Application factory for Python Code Analyzer Flask service."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS
    cors_origins = app.config.get("CORS_ORIGINS", ["http://localhost:5173", "http://127.0.0.1:5173"])
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # Attach analyzer service to app
    app.analyzer_service = AnalyzerService(config=config_class())

    # Register blueprints under /api and /api/v1
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(analysis_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api/v1", name="health_v1")
    app.register_blueprint(analysis_bp, url_prefix="/api/v1", name="analysis_v1")

    # Global error handlers
    @app.errorhandler(404)
    def handle_not_found(err):
        return jsonify({
            "status": "error",
            "error": "The requested resource was not found."
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(err):
        return jsonify({
            "status": "error",
            "error": "HTTP method not allowed for this endpoint."
        }), 405

    @app.errorhandler(500)
    def handle_server_error(err):
        return jsonify({
            "status": "error",
            "error": "Internal server error."
        }), 500

    return app

if __name__ == "__main__":
    app = create_app()
    host = app.config.get("HOST", "127.0.0.1")
    port = app.config.get("PORT", 5000)
    debug = app.config.get("DEBUG", False)
    print(f"Starting Python Code Analyzer Backend at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
