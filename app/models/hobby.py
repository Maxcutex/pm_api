from .base_model import BaseModel, db
from app.utils.enums import Gender


class Hobby(BaseModel):

    __tablename__ = "hobbies"

    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))

