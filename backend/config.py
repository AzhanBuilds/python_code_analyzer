import os

class Config:
    """Application configuration for Python Code Analyzer."""
    # Server settings
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")

    # Security & limits
    MAX_SOURCE_LENGTH = int(os.getenv("MAX_SOURCE_LENGTH", 100_000))  # 100k chars max
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")

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
