from .base_model import BaseModel, db
from app.utils.enums import Gender


class SkillsCategory(BaseModel):

    __tablename__ = "skill_categories"

    gender = db.Column(db.Enum(Gender))
    date_of_birth = db.Column(db.Date(), nullable=False)
