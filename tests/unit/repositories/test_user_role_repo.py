from factories import UserFactory
from tests.base_test_case import BaseTestCase
from app.models.user_role import UserRole
from factories.user_role_factory import UserRoleFactory, UserRoleFactoryFake
from factories.location_factory import LocationFactory
from app.repositories.user_role_repo import UserRoleRepo
from factories.role_factory import RoleFactory
from app.utils.redisset import RedisSet


class TestUserRoleRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserRoleRepo()
        self.redis_set = RedisSet()

    def tearDown(self):
        self.BaseTearDown()

    # def test_new_user_role_method_returns_new_user_role_object(self):
    #     role = RoleFactory.create()
    #     user = UserFactory.create()
    #     # user_role = UserRoleFactoryFake.build(user_id=user.id, role_id=role.id,)
    #     user_role = UserRoleFactory.build(role_id=role.id, user_id=user.id, )
    #
    #     # new_user_role = self.repo.new_user_role(
    #     #     user_id=user.id, role_id=user_role.role_id,
    #     # )
    #     new_user_role = self.repo.new_user_role(
    #         user_id=user_role.user_id, role_id=user_role.role_id,
    #     )
    #     print(new_user_role.__dict__)
    #     self.assertIsInstance(new_user_role, UserRole)
    #     self.assertEqual(str(new_user_role.user_id), str(user.id))

    def test_exclude_works_user_role_instance(self):
        role = RoleFactory.create()
        user = UserFactory.create()

        user_role = UserRoleFactory.build(
            role_id=role.id,
            user_id=user.id,
        )

        new_user_role = self.repo.new_user_role(
            user_id=user_role.user_id,
            role_id=user_role.role_id,
        )

        excluded_response = new_user_role.to_dict(exclude=["user_id"])

        self.assertFalse(excluded_response.get("user_id", False))
