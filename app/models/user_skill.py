from .base_model import BaseModel, db
from app.utils.enums import SkillLevel


class UserSkill(BaseModel):

    __tablename__ = "user_skills"

    skill_level = db.Column(db.Enum(SkillLevel))
    years = db.Column(db.Integer(), nullable=False)
    skill_id = db.Column(db.Integer(), db.ForeignKey("skills.id"))
    skill = db.relationship("Skill", lazy=False)
    user = db.relationship("User", lazy=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
