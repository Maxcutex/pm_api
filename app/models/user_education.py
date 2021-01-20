from .base_model import BaseModel, db
from app.utils.enums import Gender


class UserEducation(BaseModel):

    __tablename__ = "user_education"

    institution_name = db.Column(db.String, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    degree_earned = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", lazy=False)
    accomplishments = db.Column(db.Text, nullable=True)
