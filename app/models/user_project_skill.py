from .base_model import BaseModel, db


class UserProjectSkill(BaseModel):

    __tablename__ = "user_project_skills"

    user_project_id = db.Column(db.Integer(), db.ForeignKey("user_projects.id"))
    user_project = db.relationship("UserProject", lazy=False)
    skill_id = db.Column(db.Integer(), db.ForeignKey("skills.id"))
    skill = db.relationship("Skill", lazy=False)
