from .base_model import BaseModel, db


class Client(BaseModel):
    __tablename__ = "clients"

    institution_name = db.Column(db.String, nullable=False)
    institution_url = db.Column(db.String, nullable=True)
    institution_city = db.Column(db.String, nullable=False)
    institution_country = db.Column(db.String, nullable=False)
    institution_size = db.Column(db.String, nullable=True)
    job_title_needed = db.Column(db.String, nullable=True)
    job_description = db.Column(db.Text, nullable=True)
