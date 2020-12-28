from .base_model import BaseModel, db
from app.utils.enums import Gender


class Skill(BaseModel):

    __tablename__ = "skills"

    name = db.Column(db.String(100), nullable=False)
    skills_category_id = db.Column(db.Integer(), db.ForeignKey("skill_categories.id"))
    skills_category = db.relationship("SkillsCategory", lazy=False)
