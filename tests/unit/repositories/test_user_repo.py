import datetime

from app.models.user import User
from factories.user_factory import UserFactory, UserFactoryFake
from factories.user_role_factory import UserRoleFactory
from factories.role_factory import RoleFactory
from app.repositories.user_repo import UserRepo
from tests.base_test_case import BaseTestCase


class TestUserRoleRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_method_returns_new_user_object(self):
        user = UserFactoryFake.build()
        user1 = UserFactory.create()
        role = RoleFactory()
        UserRoleFactory(user_id=user1.id, role_id=role.id)

        new_user = self.repo.new_user(
            user.first_name,
            user.last_name,
            user.email,
            "male",
            datetime.datetime.now().strftime("%Y-%m-%d"),
            1,
            "password",
        )
        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.first_name, user.first_name)
