from .base_model import BaseModel, db
from app.utils.enums import Gender


class UserEmploymentSkill(BaseModel):

    __tablename__ = "user_employment_skills"

    user_employment_id = db.Column(db.Integer(), db.ForeignKey("user_employments.id"))
    user_employment = db.relationship("UserEmployment", lazy=False)
    skill_id = db.Column(db.Integer(), db.ForeignKey("skills.id"))
    skill = db.relationship("Skill", lazy=False)
