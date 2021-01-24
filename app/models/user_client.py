from .base_model import BaseModel, db
from ..utils.enums import EmploymentType


class UserClient(BaseModel):
    __tablename__ = "user_clients"

    institution_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    employment_type = db.Column(
        db.Enum(EmploymentType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=True,
    )
    institution_url = db.Column(db.String, nullable=True)
    institution_city = db.Column(db.String, nullable=False)
    institution_country = db.Column(db.String, nullable=False)
    institution_size = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", lazy=False)
    client_id = db.Column(db.Integer(), db.ForeignKey("clients.id"))
    client = db.relationship("Client", lazy=False)
