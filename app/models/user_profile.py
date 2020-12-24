from .base_model import BaseModel, db
from app.utils.enums import MealSessionNames


class UserProfile(BaseModel):

    __tablename__ = "user_profiles"

    name = db.Column(db.Enum(MealSessionNames))
    start_time = db.Column(db.Time(), nullable=False)
    stop_time = db.Column(db.Time(), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    location = db.relationship("Location", lazy=False)
    location_id = db.Column(db.Integer(), db.ForeignKey("locations.id"))
