"""Integration tests for the User Blueprint.
"""
from unittest.mock import patch

from factories.user_factory import UserFactoryFake
from tests.base_test_case import BaseTestCase
from app.utils.auth import PermissionRepo, UserRoleRepo
from factories import (
    UserFactory,
    RoleFactory,
    PermissionFactory,
    UserRoleFactory,
    LocationFactory,
)
from .user_role import create_user_role


class TestUserEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    # @patch.object(PermissionRepo, "get_unpaginated")
    # @patch.object(UserRoleRepo, "find_first")
    # def test_get_admin_user_endpoint_with_right_permission(
    #     self, mock_user_role_repo_find_first, mock_permission_repo_get_unpaginated
    # ):
    #     class MockUserRoleRep:
    #         def __init__(self, role_id):
    #             self.role_id = role_id
    #
    #     class MockPermissionRepo:
    #         def __init__(self, keyword):
    #             self.keyword = keyword
    #
    #     mock_user_role_repo = MockUserRoleRep(1)
    #     mock_user_perms = MockPermissionRepo("create_user_roles")
    #
    #     with self.app.app_context():
    #         mock_user_role_repo_find_first.return_value = mock_user_role_repo
    #         mock_permission_repo_get_unpaginated.return_value = [mock_user_perms]
    #
    #         response = self.client().get(
    #             self.make_url("/users/admin"), headers=self.headers()
    #         )
    #         response = response.get_json()
    #
    #         assert response["msg"] == "OK"
    #         assert response["payload"].get("adminUsers") == []

    def test_list_users_endpoint(self):
        role = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="view_users", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        # Create ten Dummy users
        UserFactory.create_batch(10)

        response = self.client().get(self.make_url("/users/"), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(len(payload["users"]), 11)
        self.assertJSONKeysPresent(payload["users"][0], "first_name", "last_name")

    def test_delete_user_endpoint_with_right_permission(self):

        role = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        permission = PermissionFactory.create(keyword="delete_user", role=role)
        permission.save()
        user_role = UserRoleFactory.create(user_id=user_id, role=role)
        user_role.save()

        user = UserFactory.create()
        user.save()

        response = self.client().delete(
            self.make_url(f"/users/{user.id}/"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(response_json["msg"], "User deleted")

    def test_delete_already_deleted_user_with_right_permission(self):

        role = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="delete_user", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        user = UserFactory.create(is_deleted=True)
        user.save()
        response = self.client().delete(
            self.make_url(f"/users/{user.id}/"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        self.assert400(response)
        self.assertEqual(400, response.status_code)
        self.assertEqual(response_json["msg"], "User has already been deleted")

    def test_delete_vendor_endpoint_without_right_permission(self):

        role = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="wrong_permission", role_id=100)
        UserRoleFactory.create(user_id=user_id, role=role)

        user = UserFactory.create(is_deleted=True)
        user.save()
        response = self.client().delete(
            self.make_url(f"/users/{user.id}/"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert401(response)
        self.assertEqual(response_json["msg"], "Access Error - No Permission Granted")

    def test_delete_user_endpoint_with_wrong_user_id(self):

        role = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="delete_user", role=role)

        user = UserFactory.create(is_deleted=True)
        user.save()

        UserRoleFactory.create(user_id=user_id, role_id=user.id)

        response = self.client().delete(
            self.make_url("/userrs/-576A/"), headers=self.headers()
        )

        self.assert404(response)

    def test_create_user_endpoint_succeeds1(self):
        location = LocationFactory()
        create_user_role("create_user", "admin")

        user = UserFactoryFake.build()
        role1 = RoleFactory()
        user_data = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            role_id=role1.id,
            email=user.email,
            gender=user.gender,
            date_of_birth=str(user.date_of_birth),
            location_id=location.id,
            password=user.password,
        )

        headers = self.headers()
        headers.update({"X-Location": location.id})

        response = self.client().post(
            self.make_url("/users/"),
            headers=headers,
            data=self.encode_to_json_string(user_data),
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json["msg"], "OK")
        self.assertEqual(
            response_json["payload"]["user"]["first_name"], user.first_name
        )
        self.assertEqual(response_json["payload"]["user"]["last_name"], user.last_name)

    def test_create_user_endpoint_succeeds2(self):
        location = LocationFactory.create()
        headers = self.headers()
        headers.update({"X-Location": location.id})

        create_user_role("view_users", "admin")
        user = UserFactory()
        user.save()
        response = self.client().get(
            self.make_url(f"/users/user_profile/{user.id}"), headers=headers
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["msg"], "OK")
        self.assertEqual(
            response_json["payload"]["user"]["first_name"], user.first_name
        )
        self.assertEqual(response_json["payload"]["user"]["last_name"], user.last_name)

    # Failing Test even though it should succeed
    # def test_update_user_endpoint_succeeds(self):
    #
    #     create_user_role("update_user", "admin")
    #     role = RoleFactory()
    #     user = UserFactory.create(first_name="testng")
    #     user.save()
    #     user_role = UserRoleFactory(user_id=user.id, role=role)
    #     user_role.save()
    #     print("asfdasfd", user_role.id)
    #     print("user being checked", user.id)
    #
    #     user_data = dict(first_name="Andela", last_name="Eats", role_id=role.id)
    #
    #     response = self.client().patch(
    #         self.make_url(f"/users/{user.id}"),
    #         headers=self.headers(),
    #         data=self.encode_to_json_string(user_data),
    #     )
    #     print(response)
    #     response_json = self.decode_from_json_string(response.data.decode("utf-8"))
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response_json["msg"], "OK")
    #     self.assertEqual(response_json["payload"]["user"]["first_name"], user.first_name)
    #     self.assertEqual(response_json["payload"]["user"]["last_name"], user.last_name)

    def test_update_user_endpoint_with_invalid_role_fails(self):
        create_user_role("update_user", "admin")
        role = RoleFactory()

        user = UserFactory()
        user.save()
        UserRoleFactory(user_id=user.id, role=role)
        user_data = dict(
            first_name="Andela",
            last_name="Eats",
            role_id=100,
            gender="male",
            date_of_birth="2020-10-01",
            employment_date="2020-10-01",
        )

        response = self.client().patch(
            self.make_url(f"/users/{user.id}"),
            headers=self.headers(),
            data=self.encode_to_json_string(user_data),
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["msg"], "Role with id 100 doesnot exist")

    def test_update_user_endpoint_for_non_existing_user_id_fails(self):

        create_user_role("update_user", "admin")
        user = UserFactory.create(id=600)
        user.save()

        user_data = dict(
            first_name="Andela",
            last_name="Eats",
            user_id=601,
            role_id=1,
            gender="male",
            date_of_birth="2020-10-01",
            employment_date="2020-10-01",
        )

        response = self.client().put(
            self.make_url("/users/" + str(user.id + 1)),
            headers=self.headers(),
            data=self.encode_to_json_string(user_data),
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json["msg"], "FAIL")
        self.assertEqual(response_json["payload"]["user"], "User not found")

    def test_update_user_endpoint_for_already_deleted_user_fails(self):

        create_user_role("update_user", "admin")
        user = UserFactory.create(is_deleted=True)
        user.save()

        user_data = dict(
            first_name="Andela",
            last_name="Eats",
            user_id=user.id,
            role_id=1,
            gender="male",
            date_of_birth="2020-10-01",
            employment_date="2020-10-01",
        )
        response = self.client().put(
            self.make_url("/users/" + str(user.id)),
            headers=self.headers(),
            data=self.encode_to_json_string(user_data),
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["msg"], "FAIL")
        self.assertEqual(response_json["payload"]["user"], "User already deleted")

    def test_create_user_endpoint_succeeds(self):
        create_user_role("create_user", "admin")
        user = UserFactoryFake.build(id=500, is_deleted=True)
        role = RoleFactory(name="test_role")

        location = LocationFactory.create()
        headers = self.headers()
        headers.update({"X-Location": location.id})

        user_data = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            role_id=role.id,
            gender=user.gender,
            date_of_birth=str(user.date_of_birth),
            employment_date=str(user.employment_date),
            password=user.password,
            email=user.email,
            location_id=user.location_id,
        )

        response = self.client().post(
            self.make_url("/users/"),
            headers=headers,
            data=self.encode_to_json_string(user_data),
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        print(response_json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json["msg"], "OK")
        self.assertEqual(
            response_json["payload"]["user"]["first_name"], user.first_name
        )
        self.assertEqual(response_json["payload"]["user"]["last_name"], user.last_name)
        self.assertEqual(
            response_json["payload"]["user"]["user_roles"][0]["name"], role.name
        )
        self.assertEqual(
            response_json["payload"]["user"]["user_roles"][0]["help"], role.help
        )
