from .base_model import BaseModel, db

from . import constants
from ..utils.enums import Gender


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(constants.MAXLEN), nullable=False)
    password = db.Column(db.String, nullable=False)
    last_password = db.Column(db.String, nullable=True)
    location_id = db.Column(db.Integer(), db.ForeignKey("locations.id"), default=1)
    location = db.relationship("Location", lazy=False)
    image_url = db.Column(db.String, nullable=True)
    profile_summary = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Enum(Gender), nullable=True)
    date_of_birth = db.Column(db.Date(), nullable=False)
    user_role = db.relationship("UserRole", backref="user_roles", lazy=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_deleted = db.Column(db.Boolean, default=True, nullable=True)
    employment_date = db.Column(db.Date(), nullable=True)
    terminal_date = db.Column(db.Date(), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    personal_email = db.Column(db.String(constants.MAXLEN), nullable=True)
