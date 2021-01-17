from .base_model import BaseModel, db
from ..utils.enums import EmploymentType


class UserEmployment(BaseModel):

    __tablename__ = "user_employments"

    institution_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    employment_type = db.Column(
        db.Enum(EmploymentType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=True,
    )
    institution_url = db.Column(db.String, nullable=False)
    institution_city = db.Column(db.String, nullable=False)
    institution_country = db.Column(db.String, nullable=False)
    institution_size = db.Column(db.String, nullable=False)
    work_summary = db.Column(db.Text, nullable=False)
    accomplishments = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", lazy=False)
    is_current = db.Column(db.Boolean, default=False, nullable=True)
    skills = db.relationship(
        "UserEmploymentSkill", backref="user_employment_skills", lazy=True
    )
