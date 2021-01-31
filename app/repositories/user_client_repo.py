from app.repositories.base_repo import BaseRepo
from app.models.user_client import UserClient


class UserClientRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserClient)
