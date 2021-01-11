from .base_model import BaseModel, db


class UserEmployment(BaseModel):

    __tablename__ = "user_employments"

    institution_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", lazy=False)
    is_current = db.Column(db.Boolean, default=False, nullable=True)
