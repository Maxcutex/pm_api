from .base_model import BaseModel, db
from app.utils.enums import Gender


class UserProject(BaseModel):

    __tablename__ = "user_projects"

    gender = db.Column(db.Enum(Gender))
    date_of_birth = db.Column(db.Date(), nullable=False)
