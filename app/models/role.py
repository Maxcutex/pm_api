from .base_model import BaseModel, db
from . import constants


class Role(BaseModel):
    __tablename__ = "roles"

    name = db.Column(db.String(constants.MAXLEN), nullable=False, unique=True)
    help = db.Column(db.Text(), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=True)
    user_roles = db.relationship("UserRole", backref="roles", lazy=True)
    # permissions = db.relationship("Permission", lazy=False)
