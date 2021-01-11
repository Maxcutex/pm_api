from tests.base_test_case import BaseTestCase
from factories import (
    SkillsCategoryFactory,
    SkillsCategoryFactoryFake,
    PermissionFactory,
    UserRoleFactory,
    RoleFactory,
)


class TestSkillsCategoryEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_skill_category_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="create_skills_categories", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        data = {"name": "Jack Jones", "help": "A Help Message"}

        response = self.client().post(
            self.make_url("/skills_categories/"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, "payload")
        self.assertEqual(payload["skills_category"]["name"], "Jack Jones")
        self.assertEqual(payload["skills_category"]["help"], "A Help Message")

    def test_list_skill_categories_endpoint(self):

        SkillsCategoryFactory.create_batch(3)
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_skills_categories", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().get(
            self.make_url("/skills_categories/"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(len(payload["skills_categories"]), 3)
        self.assertJSONKeysPresent(payload["skills_categories"][0], "name", "help")

    def test_get_specific_skill_category_endpoint(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()
        skills_category = SkillsCategoryFactory.create()
        PermissionFactory.create(keyword="view_skills_categories", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().get(
            self.make_url("/skills_categories/{}".format(skills_category.id)),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertJSONKeyPresent(payload, "skills_category")
        self.assertJSONKeysPresent(payload["skills_category"], "name", "help")
        self.assertEqual(payload["skills_category"]["id"], skills_category.id)
        self.assertEqual(payload["skills_category"]["name"], skills_category.name)
        self.assertEqual(payload["skills_category"]["help"], skills_category.help)

    def test_update_skill_categories_endpoint(self):

        RoleFactory.create()
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        skills_category = SkillsCategoryFactory.create()

        PermissionFactory.create(keyword="update_skills_categories", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        data = {"name": "Super Admin"}
        response = self.client().put(
            self.make_url("/skills_categories/{}".format(skills_category.id)),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["skills_category"]["name"], data["name"])

    def test_invalid_update(self):

        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_skills_categories", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        data = {"name": "Super Admin"}
        response = self.client().put(
            self.make_url("/skills_categories/1000"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        self.assert400(response)

    def test_delete_skill_category_endpoint_with_right_permission(self):
        role = RoleFactory.create()
        skills_category = SkillsCategoryFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="delete_skills_categories", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        response = self.client().delete(
            self.make_url(f"/skills_categories/{skills_category.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(response_json["msg"], "skills category deleted")

    def test_delete_skill_category_endpoint_without_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(
            self.make_url(f"/skills_categories/{role.id}"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert401(response)
        self.assertEqual(response_json["msg"], "Access Error - No Permission Granted")

    def test_delete_skill_category_endpoint_with_wrong_skill_category_id(self):
        role1 = RoleFactory.create(name="admin")
        SkillsCategoryFactory.create()
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(
            keyword="delete_skills_categories",
            name="delete_skills_categories",
            role=role1,
        )
        UserRoleFactory.create(user_id=user_id, role=role1)

        response = self.client().delete(
            self.make_url("/skills_categories/1576"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert404(response)
        self.assertEqual(
            response_json["msg"], "Invalid or incorrect skills_category_id provided"
        )
