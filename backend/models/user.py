from datetime import datetime, timezone
import re
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import db

class User(db.Model):
    """User account model for authentication."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    @classmethod
    def validate_email(cls, email: str) -> tuple[bool, str]:
        if not email or not isinstance(email, str):
            return False, "Email address is required."
        clean_email = email.strip()
        if len(clean_email) > 255:
            return False, "Email address cannot exceed 255 characters."
        if not cls.EMAIL_REGEX.match(clean_email):
            return False, "Please enter a valid email address."
        return True, ""

    @classmethod
    def validate_password(cls, password: str) -> tuple[bool, str]:
        if not password or not isinstance(password, str):
            return False, "Password is required."
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if len(password) > 128:
            return False, "Password cannot exceed 128 characters."
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter."
        if not any(c.isdigit() or not c.isalnum() for c in password):
            return False, "Password must contain at least one number or special character."
        return True, ""

    @classmethod
    def validate_display_name(cls, display_name: str) -> tuple[bool, str]:
        if not display_name or not isinstance(display_name, str):
            return False, "Display name is required."
        clean_name = display_name.strip()
        if len(clean_name) < 2:
            return False, "Display name must be at least 2 characters long."
        if len(clean_name) > 100:
            return False, "Display name cannot exceed 100 characters."
        return True, ""

    def set_password(self, password: str) -> None:
        """Securely hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the given password against the stored password hash."""
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Serialize user object without sensitive data like password_hash."""
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
