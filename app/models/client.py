from .base_model import BaseModel, db
from ..utils.enums import ClientStatus


class Client(BaseModel):
    __tablename__ = "clients"

    institution_name = db.Column(db.String, nullable=False)
    institution_url = db.Column(db.String, nullable=True)
    institution_city = db.Column(db.String, nullable=False)
    institution_country = db.Column(db.String, nullable=False)
    institution_size = db.Column(db.String, nullable=True)
    status = db.Column(db.Enum(ClientStatus), nullable=True)
    start_date = db.Column(db.Date(), nullable=False)
