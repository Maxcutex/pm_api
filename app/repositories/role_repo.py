from app.repositories.base_repo import BaseRepo
from app.models.role import Role


class RoleRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, Role)

    def new_role(self, name, help_=None, is_active=True, is_deleted=False):

        role = Role(name=name, help=help_, is_active=is_active, is_deleted=is_deleted)

        role.save()
        return role
