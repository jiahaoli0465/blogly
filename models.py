"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_PROFILE_PIC = "https://www.freeiconspng.com/uploads/name-people-person-user-icon--icon-search-engine-1.png"

class User(db.Model):
    """all users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_PROFILE_PIC)


    def get_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    def get_pic(self):
        """Return full name of user."""

        return self.image_url


def connect_db(app):
    db.app = app
    db.init_app(app)