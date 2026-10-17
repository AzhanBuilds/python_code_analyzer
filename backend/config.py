import os
from datetime import timedelta
from dotenv import load_dotenv

# Load backend/.env if present
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

class Config:
    """Application configuration for Python Code Analyzer."""
    # Server settings
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")

    # Security & secrets
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-python-analyzer-change-in-production")
    MAX_SOURCE_LENGTH = int(os.getenv("MAX_SOURCE_LENGTH", 100_000))  # 100k chars max
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
        ).split(",")
        if origin.strip()
    ]

    # Database configuration (PostgreSQL)
    # Configure through DATABASE_URL or component variables
    PG_USER = os.getenv("POSTGRES_USER", "postgres")
    PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
    PG_PORT = os.getenv("POSTGRES_PORT", "5432")
    PG_DB = os.getenv("POSTGRES_DB", "python_code_analyzer_db")

    @staticmethod
    def _format_db_url():
        from urllib.parse import quote_plus, unquote
        raw_url = os.getenv("DATABASE_URL")
        if raw_url:
            # Handle special characters like '@' in database password
            if "://" in raw_url and "@" in raw_url:
                prefix, _, rest = raw_url.partition("://")
                auth_part, _, host_part = rest.rpartition("@")
                if ":" in auth_part:
                    user, _, pwd = auth_part.partition(":")
                    return f"{prefix}://{user}:{quote_plus(unquote(pwd))}@{host_part}"
            return raw_url

        user = quote_plus(os.getenv("POSTGRES_USER", "postgres"))
        pwd = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        dbname = os.getenv("POSTGRES_DB", "python_code_analyzer_db")
        return f"postgresql://{user}:{pwd}@{host}:{port}/{dbname}"

    SQLALCHEMY_DATABASE_URI = _format_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session cookie security settings
    SESSION_COOKIE_NAME = "py_analyzer_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() in ("true", "1", "yes")
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.getenv("SESSION_LIFETIME_DAYS", 7)))

    # Static analysis thresholds
    MAX_LINE_LENGTH = int(os.getenv("MAX_LINE_LENGTH", 100))
    MAX_FUNCTION_LINES = int(os.getenv("MAX_FUNCTION_LINES", 50))
    MAX_COMPLEXITY_THRESHOLD = int(os.getenv("MAX_COMPLEXITY_THRESHOLD", 10))

    # Quality scoring deductions by severity
    PENALTIES = {
        "critical": 20,
        "high": 10,
        "medium": 5,
        "low": 2,
        "info": 0
    }

class TestingConfig(Config):
    """Configuration for automated test execution."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    SECRET_KEY = "test-secret-key"
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False
