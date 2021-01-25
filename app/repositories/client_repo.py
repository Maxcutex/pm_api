from app.repositories.base_repo import BaseRepo
from app.models.client import Client


class ClientRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, Client)
