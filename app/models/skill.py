from .base_model import BaseModel, db
from app.utils.enums import Gender


class Skill(BaseModel):

    __tablename__ = "skills"

    name = db.Column(db.String(100), nullable=False)
    skill_category_id = db.Column(db.Integer(), db.ForeignKey("skill_categories.id"))
    skill_category = db.relationship("SkillCategory", lazy=False)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=True)
