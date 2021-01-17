from datetime import datetime, date

from factories.skill_category_factory import CategoryWithSkillsFactory
from tests.base_test_case import BaseTestCase
from factories import (
    UserProjectFactory,
    UserProjectFactoryFake,
    PermissionFactory,
    UserRoleFactory,
    RoleFactory,
    UserFactory,
)


class TestUserProjectEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        # self.skill_category = CategoryWithSkillsFactory.create(skills=4)
        # self.skill_category.save()
        # self.skill_one = self.skill_category.skills[0]
        # self.skill_two = self.skill_category.skills[1]
        # self.skill_three = self.skill_category.skills[2]
        # self.skill_four = self.skill_category.skills[3]

    def tearDown(self):
        self.BaseTearDown()

    def test_create_user_project_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="create_user_project", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_proj_data = UserProjectFactoryFake.build(
            start_date=date(year=2018, month=1, day=31),
            end_date=date(year=2028, month=1, day=31),
        )
        data = {
            "user_id": user_id,
            "project_name": user_proj_data.project_name,
            "project_url": user_proj_data.project_url,
            "project_description": user_proj_data.project_description,
            "start_date": str(user_proj_data.start_date),
            "end_date": str(user_proj_data.end_date),
            "is_current": user_proj_data.is_current,
        }

        response = self.client().post(
            self.make_url("/user_project/"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        print(response)
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        print(response_json)
        payload = response_json["payload"]

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, "payload")
        self.assertEqual(
            payload["user_project"]["project_name"],
            user_proj_data.project_name,
        )
        self.assertEqual(
            payload["user_project"]["project_url"], user_proj_data.project_url
        )

    def test_list_user_project_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_project", role=role1)
        user = UserFactory.create()
        user.save()
        UserRoleFactory.create(user=user, role=role1)
        UserProjectFactory.create_batch(3, user=user)

        response = self.client().get(
            self.make_url(f"/user_project/user/{user.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]
        self.assert200(response)
        self.assertEqual(len(payload["user_projects"]), 3)
        self.assertJSONKeysPresent(
            payload["user_projects"][0], "project_name", "project_url"
        )

    def test_get_specific_user_project_endpoint(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_project", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        user_project = UserProjectFactory.create()
        user_project.save()
        response = self.client().get(
            self.make_url("/user_project/user-single/{}".format(user_project.id)),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        payload = response_json["payload"]

        self.assert200(response)
        self.assertJSONKeyPresent(payload, "user_project")
        self.assertJSONKeysPresent(
            payload["user_project"], "project_name", "project_url"
        )
        self.assertEqual(payload["user_project"]["id"], user_project.id)
        self.assertEqual(
            payload["user_project"]["project_name"],
            user_project.project_name,
        )
        self.assertEqual(
            payload["user_project"]["project_url"], user_project.project_url
        )

    def test_update_user_project_endpoint(self):
        RoleFactory.create()
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_project", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_proj_data = UserProjectFactory.create()
        user_proj_data.save()
        data = {
            "user_id": user_id,
            "user_project_id": user_proj_data.id,
            "project_name": user_proj_data.project_name,
            "project_url": user_proj_data.project_url,
            "project_description": user_proj_data.project_description,
            "start_date": str(user_proj_data.start_date),
            "end_date": str(user_proj_data.end_date),
            "is_current": user_proj_data.is_current,
        }
        response = self.client().put(
            self.make_url("/user_project/{}".format(user_proj_data.id)),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["user_project"]["project_name"], data["project_name"])

    def test_invalid_update(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_project", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        user_proj_data = UserProjectFactory.create()
        user_proj_data.save()

        data = {
            "user_id": user_id,
            "user_project_id": user_proj_data.id,
            "project_name": user_proj_data.project_name,
            "project_url": user_proj_data.project_url,
            "start_date": str(user_proj_data.start_date),
            "end_date": str(user_proj_data.end_date),
            "is_current": user_proj_data.is_current,
        }
        response = self.client().put(
            self.make_url("/user_project/1000"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        self.assert400(response)

    def test_delete_user_project_endpoint_with_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="delete_user_project", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        user_proj_data = UserProjectFactory.create()
        user_proj_data.save()

        response = self.client().delete(
            self.make_url(f"/user_project/{user_proj_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(response_json["msg"], "user project deleted")

    def test_delete_user_project_endpoint_without_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        UserRoleFactory.create(user_id=user_id, role=role)
        user_proj_data = UserProjectFactory.create()
        user_proj_data.save()

        response = self.client().delete(
            self.make_url(f"/user_project/{user_proj_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert401(response)
        self.assertEqual(response_json["msg"], "Access Error - No Permission Granted")

    def test_delete_user_project_endpoint_with_wrong_user_project_id(self):
        role1 = RoleFactory.create(name="admin")

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(
            keyword="delete_user_project",
            name="delete_user_project",
            role=role1,
        )

        UserRoleFactory.create(user_id=user_id, role=role1)
        user_proj_data = UserProjectFactory.create()
        user_proj_data.save()

        response = self.client().delete(
            self.make_url("/user_project/1576"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert404(response)
        self.assertEqual(
            response_json["msg"], "Invalid or incorrect user_project_id provided"
        )
