from .base_model import BaseModel, db
from app.utils.enums import Gender


class UserProject(BaseModel):

    __tablename__ = "user_projects"

    project_name = db.Column(db.String, nullable=False)
    project_url = db.Column(db.String, nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", lazy=False)
    is_current = db.Column(db.Boolean, default=False, nullable=True)
    skills = db.relationship(
        "UserProjectSkill", backref="user_project_skills", lazy=True
    )
