from tests.base_test_case import BaseTestCase
import factory
from factories.role_factory import RoleFactory
from factories.user_role_factory import UserRoleFactory
from factories.permission_factory import PermissionFactory


def create_user_role(keyword, role_name):
    role = RoleFactory.create(name=role_name)
    user_id = BaseTestCase.user_id()
    PermissionFactory.create(keyword=keyword, role=role)
    return UserRoleFactory.create(user_id=user_id, role=role), user_id
