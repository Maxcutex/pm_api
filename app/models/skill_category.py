from .base_model import BaseModel, db


class SkillCategory(BaseModel):

    __tablename__ = "skill_categories"

    name = db.Column(db.String(100), nullable=False)
    help = db.Column(db.Text(), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=True)
    skills = db.relationship("Skill", backref="skill_categories", lazy=True)
