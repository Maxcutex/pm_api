from .base_model import BaseModel, db
from app.utils.enums import Gender, SkillLevels


class UserSkills(BaseModel):

    __tablename__ = "user_skills"

    skill_level = db.Column(db.Enum(SkillLevels))
    years = db.Column(db.Integer(), nullable=False)
    skill_id = db.Column(db.Integer(), db.ForeignKey("skills.id"))
    skill = db.relationship("Skill", lazy=False)
