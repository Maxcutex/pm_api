from .base_model import BaseModel, db


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    role = db.relationship("Role", lazy=False)
    user = db.relationship("User", lazy=False)
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_deleted = db.Column(db.Boolean, default=True, nullable=True)
