"""
Unit tests for the User Controller.
"""
from datetime import datetime
from unittest.mock import patch

from app.controllers.user_controller import UserController
from app.models import User, Role
from app.models.user_role import UserRole
from app.repositories import UserRepo, RoleRepo, UserRoleRepo
from tests.base_test_case import BaseTestCase
from factories.user_factory import UserFactory
from factories import RoleFactory, UserRoleFactory, PermissionFactory
from factories.location_factory import LocationFactory
from app.utils.auth import Auth


class TestUserController(BaseTestCase):
    """
    UserController test class.
    """

    def setUp(self):
        self.BaseSetUp()
        self.mock_role = Role(
            id=1,
            name="Pass",
            help="help",
        )
        self.mock_user_role = UserRole(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            role_id=1,
            role=self.mock_role,
            user_id=1,
            is_active=True,
            is_deleted=False,
        )

        self.mock_user = User(
            id=1,
            first_name="test",
            last_name="test",
            gender="male",
            password="test",
            email="user1@user.com",
            is_active=True,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_user2 = User(
            id=1,
            first_name="test",
            last_name="test",
            gender="male",
            password="test",
            email="user2@user.com",
            is_active=True,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(UserController, "pagination_meta")
    @patch("app.repositories.user_role_repo.UserRoleRepo.filter_by")
    @patch.object(UserRepo, "find_first")
    def test_list_admin_users_ok_response(
        self, mock_user_repo_find_first, mock_filter_by, mock_pagination_meta
    ):
        """
        Test list_admin_users OK response.
        """
        # Arrange
        with self.app.app_context():
            mock_filter_by.return_value.items = [
                self.mock_user_role,
            ]
            mock_user_repo_find_first.return_value = self.mock_user
            mock_pagination_meta.return_value = {
                "total_rows": 1,
                "total_pages": 1,
                "current_page": 1,
                "next_page": None,
                "prev_page": None,
            }
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.list_admin_users()

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            assert result.get_json()["payload"]["meta"]["current_page"] == 1
            assert result.get_json()["payload"]["meta"]["next_page"] is None

    @patch.object(Auth, "get_location")
    @patch.object(UserController, "request_params")
    @patch.object(RoleRepo, "find_first")
    @patch.object(UserRepo, "exists")
    @patch.object(UserRepo, "new_user")
    @patch.object(UserRoleRepo, "new_user_role")
    def test_create_user_succeeds(
        self,
        mock_user_role_repo_new_user_role,
        mock_user_repo_new_user,
        mock_user_repo_exists,
        mock_role_repo_find_first,
        mock_request_params,
        mock_get_location,
    ):
        location = LocationFactory()
        role = RoleFactory(name="test_role")

        with self.app.app_context():
            mock_get_location.return_value = location.id
            mock_role_repo_find_first.return_value = self.mock_role
            mock_user_repo_exists.return_value = None
            mock_user_repo_new_user.return_value = self.mock_user2
            mock_user_role_repo_new_user_role.return_value = self.mock_user_role
            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                "tst@tst.com",
                role.id,
                "male",
                str(datetime.now()),
                1,
                "password",
            ]
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.create_user()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserController, "request_params")
    def test_create_user_method_handles_user_creation_with_non_existent_role_id(
        self, mock_request_params
    ):
        with self.app.app_context():
            user = UserFactory()
            role = RoleFactory(name="test_role")
            UserRoleFactory(role_id=role.id, user_id=user.id)

            non_existent_role_id = 100

            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                "tst@tst.com",
                non_existent_role_id,
                "male",
                str(datetime.now()),
                1,
                "password",
            ]

            user_controller = UserController(self.request_context)

            response = user_controller.create_user()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()["msg"],
                "Role with userTypeId(roleId) {} does not exist".format(
                    non_existent_role_id
                ),
            )

    @patch.object(UserRepo, "find_first")
    def test_list_user_succeeds(
        self,
        mock_user_repo_find_first,
    ):
        with self.app.app_context():
            role = RoleFactory()

            UserRoleFactory(user_id=self.mock_user.id, role_id=role.id)
            PermissionFactory.create(keyword="view_users", role=role)
            mock_user_repo_find_first.return_value = self.mock_user
            user_controller = UserController(self.request_context)

            response = user_controller.list_user(id=self.mock_user.id)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["msg"], "OK")

            self.assertEqual(
                response.get_json()["payload"]["user"]["first_name"],
                self.mock_user.first_name,
            )
            self.assertEqual(
                response.get_json()["payload"]["user"]["last_name"],
                self.mock_user.last_name,
            )

    @patch.object(UserRepo, "find_first")
    def test_list_user_when_user_found_succeeds(
        self,
        mock_user_repo_find_first,
    ):
        with self.app.app_context():
            user_controller = UserController(self.request_context)
            mock_user_repo_find_first.return_value = self.mock_user
            response = user_controller.list_user(id=1)

            self.assertEqual(response.status_code, 200)

    @patch.object(Auth, "get_location")
    @patch.object(UserController, "request_params")
    @patch.object(RoleRepo, "find_first")
    @patch.object(UserRepo, "exists")
    # @patch.object(UserRepo, "new_user")
    @patch.object(UserRoleRepo, "new_user_role")
    def test_create_user_fails_for_existing_user(
        self,
        mock_user_role_repo_new_user_role,
        # mock_user_repo_new_user,
        mock_user_repo_exists,
        mock_role_repo_find_first,
        mock_request_params,
        mock_get_location,
    ):
        location = LocationFactory()
        role = RoleFactory(name="test_role")

        with self.app.app_context():
            mock_get_location.return_value = location.id
            mock_role_repo_find_first.return_value = self.mock_role
            mock_user_repo_exists.return_value = self.mock_user2
            # mock_user_repo_new_user.return_value = None
            mock_user_role_repo_new_user_role.return_value = self.mock_user_role
            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                self.mock_user2.email,
                role.id,
                "male",
                str(datetime.now()),
                1,
                "password",
            ]
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.create_user()
            print(result)
            print(result.get_json())
            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == f"User with email '{self.mock_user2.email}' already exists"
            )
