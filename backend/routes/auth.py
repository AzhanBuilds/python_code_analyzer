from functools import wraps
from flask import Blueprint, request, jsonify, session, g
from sqlalchemy.exc import OperationalError
from backend.database import db
from backend.models.user import User

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    """Decorator to enforce session authentication on protected endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "status": "error",
                "error": "Authentication required. Please log in."
            }), 401

        user = db.session.get(User, user_id)
        if not user:
            session.clear()
            return jsonify({
                "status": "error",
                "error": "Session invalid or expired. Please log in again."
            }), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/auth/register", methods=["POST"], strict_slashes=False)
def register():
    """Register a new user account with validated credentials."""
    if not request.is_json:
        return jsonify({
            "status": "error",
            "error": "Invalid request. Content-Type must be application/json."
        }), 400

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "error": "Request body must be a valid JSON object."
        }), 400

    email = data.get("email")
    display_name = data.get("display_name")
    password = data.get("password")

    # Check for missing required fields
    missing_fields = []
    if not email:
        missing_fields.append("email")
    if not display_name:
        missing_fields.append("display_name")
    if not password:
        missing_fields.append("password")

    if missing_fields:
        return jsonify({
            "status": "error",
            "error": f"Missing required fields: {', '.join(missing_fields)}."
        }), 400

    # Validate fields format and constraints
    is_valid_email, email_err = User.validate_email(email)
    if not is_valid_email:
        return jsonify({"status": "error", "error": email_err}), 400

    is_valid_name, name_err = User.validate_display_name(display_name)
    if not is_valid_name:
        return jsonify({"status": "error", "error": name_err}), 400

    is_valid_pwd, pwd_err = User.validate_password(password)
    if not is_valid_pwd:
        return jsonify({"status": "error", "error": pwd_err}), 400

    clean_email = email.strip().lower()

    try:
        # Check for duplicate email
        existing_user = User.query.filter_by(email=clean_email).first()
        if existing_user:
            return jsonify({
                "status": "error",
                "error": "An account with this email address already exists."
            }), 409

        user = User(
            email=clean_email,
            display_name=display_name.strip()
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Automatically log in the user upon successful registration
        session.clear()
        session["user_id"] = user.id
        session.permanent = True

        return jsonify({
            "status": "success",
            "message": "User registered successfully.",
            "user": user.to_dict()
        }), 201
    except OperationalError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Database connection failed. PostgreSQL is not running or unreachable on port 5432. Please start PostgreSQL or configure DATABASE_URL."
        }), 503
    except Exception:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Failed to create user account due to a database error."
        }), 500

@auth_bp.route("/auth/login", methods=["POST"], strict_slashes=False)
def login():
    """Authenticate existing user credentials and establish session."""
    if not request.is_json:
        return jsonify({
            "status": "error",
            "error": "Invalid request. Content-Type must be application/json."
        }), 400

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "error": "Request body must be a valid JSON object."
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "error": "Email and password are both required."
        }), 400

    try:
        clean_email = str(email).strip().lower()
        user = User.query.filter_by(email=clean_email).first()

        if not user or not user.check_password(str(password)):
            # Safe generic error message to prevent account enumeration
            return jsonify({
                "status": "error",
                "error": "Invalid email or password."
            }), 401

        session.clear()
        session["user_id"] = user.id
        session.permanent = True

        return jsonify({
            "status": "success",
            "message": "Logged in successfully.",
            "user": user.to_dict()
        }), 200
    except OperationalError:
        return jsonify({
            "status": "error",
            "error": "Database connection failed. PostgreSQL is not running or unreachable on port 5432."
        }), 503

@auth_bp.route("/auth/logout", methods=["POST"], strict_slashes=False)
def logout():
    """Clear session and log out the user."""
    session.clear()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully."
    }), 200

@auth_bp.route("/auth/me", methods=["GET"], strict_slashes=False)
@login_required
def get_current_user():
    """Retrieve details of the currently authenticated user."""
    return jsonify({
        "status": "success",
        "user": g.current_user.to_dict()
    }), 200
