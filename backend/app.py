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
    from backend.database import db, migrate
    from backend.models import User
    from backend.routes.health import health_bp
    from backend.routes.analysis import analysis_bp
    from backend.routes.auth import auth_bp
    from backend.analyzer.analyzer_service import AnalyzerService
else:
    from .config import Config
    from .database import db, migrate
    from .models import User
    from .routes.health import health_bp
    from .routes.analysis import analysis_bp
    from .routes.auth import auth_bp
    from .analyzer.analyzer_service import AnalyzerService

def create_app(config_class=Config):
    """Application factory for Python Code Analyzer Flask service."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Database and Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize CORS with credentials support for session cookies
    cors_origins = app.config.get("CORS_ORIGINS", ["http://localhost:5173", "http://127.0.0.1:5173"])
    CORS(app, resources={r"/api/*": {"origins": cors_origins}}, supports_credentials=True)

    # Attach analyzer service to app
    app.analyzer_service = AnalyzerService(config=config_class())

    # Register blueprints under /api and /api/v1
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(analysis_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    app.register_blueprint(health_bp, url_prefix="/api/v1", name="health_v1")
    app.register_blueprint(analysis_bp, url_prefix="/api/v1", name="analysis_v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1", name="auth_v1")

    # Friendly root and /api status endpoints
    @app.route("/", methods=["GET"])
    def root_index():
        return jsonify({
            "status": "ok",
            "service": "python-code-analyzer-api",
            "message": "Python Code Analyzer backend is running. Open http://localhost:5173 for the web application.",
            "frontend_url": "http://localhost:5173",
            "endpoints": {
                "health": "/api/health",
                "analyze": "/api/analyze",
                "auth": {
                    "register": "/api/auth/register",
                    "login": "/api/auth/login",
                    "logout": "/api/auth/logout",
                    "me": "/api/auth/me"
                }
            }
        }), 200

    @app.route("/api", methods=["GET"])
    @app.route("/api/", methods=["GET"])
    def api_index():
        return jsonify({
            "status": "ok",
            "service": "python-code-analyzer-api",
            "version": "1.0"
        }), 200

    # Automatically ensure schema tables exist when database is reachable
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning("Database schema auto-creation skipped or pending: %s", e)

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

    from sqlalchemy.exc import OperationalError

    @app.errorhandler(OperationalError)
    def handle_db_operational_error(err):
        return jsonify({
            "status": "error",
            "error": "Database connection failed. PostgreSQL is not running or unreachable on localhost:5432. Please start PostgreSQL or configure DATABASE_URL in backend/.env."
        }), 503

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
