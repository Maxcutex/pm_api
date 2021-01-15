from .base_model import BaseModel, db

from . import constants
from ..utils.enums import Gender


class User(BaseModel):
    __tablename__ = "users"

    # slack_id = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(constants.MAXLEN), nullable=True)
    password = db.Column(db.String, nullable=False)
    last_password = db.Column(db.String, nullable=True)
    location_id = db.Column(db.Integer(), db.ForeignKey("locations.id"), default=1)
    location = db.relationship("Location", lazy=False)
    image_url = db.Column(db.String, nullable=True)
    gender = db.Column(db.Enum(Gender), nullable=True)
    date_of_birth = db.Column(db.Date(), nullable=False)
    user_role = db.relationship("UserRole", backref="user_roles", lazy=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_deleted = db.Column(db.Boolean, default=True, nullable=True)
