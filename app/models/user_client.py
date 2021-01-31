from .base_model import BaseModel, db
from ..utils.enums import EmploymentType


class UserClient(BaseModel):
    __tablename__ = "user_clients"

    job_title = db.Column(db.String, nullable=False)
    employment_type = db.Column(
        db.Enum(EmploymentType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=True,
    )
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", lazy=False)
    client_id = db.Column(db.Integer(), db.ForeignKey("clients.id"))
    client = db.relationship("Client", lazy=False)
