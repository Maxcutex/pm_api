from datetime import datetime, date

from factories.skill_category_factory import CategoryWithSkillsFactory
from tests.base_test_case import BaseTestCase
from factories import (
    UserSkillFactory,
    UserSkillFactoryFake,
    PermissionFactory,
    UserRoleFactory,
    RoleFactory,
    UserFactory,
)


class TestUserSkillEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.skill_category = CategoryWithSkillsFactory.create(skills=4)
        self.skill_category.save()
        self.skill_one = self.skill_category.skills[0]
        self.skill_two = self.skill_category.skills[1]
        self.skill_three = self.skill_category.skills[2]
        self.skill_four = self.skill_category.skills[3]

    def tearDown(self):
        self.BaseTearDown()

    def test_create_user_skill_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="create_user_skill", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_proj_data = UserSkillFactoryFake.build(skill_id=self.skill_two.id)
        data = {
            "user_id": user_id,
            "skill_id": user_proj_data.skill_id,
            "skill_level": user_proj_data.skill_level,
            "years": user_proj_data.years,
        }
        response = self.client().post(
            self.make_url("/user_skill/"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )

        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, "payload")
        self.assertEqual(
            payload["user_skill"]["skill_id"],
            user_proj_data.skill_id,
        )
        self.assertEqual(payload["user_skill"]["years"], user_proj_data.years)

    def test_list_user_skill_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_skill", role=role1)
        user = UserFactory.create()
        user.save()
        UserRoleFactory.create(user=user, role=role1)
        UserSkillFactory.create_batch(3, user=user)

        response = self.client().get(
            self.make_url(f"/user_skill/user/{user.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]
        self.assert200(response)
        self.assertEqual(len(payload["user_skills"]), 3)
        self.assertJSONKeysPresent(payload["user_skills"][0], "skill_level", "years")

    def test_get_specific_user_skill_endpoint(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_skill", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        user_skill = UserSkillFactory.create()
        user_skill.save()
        response = self.client().get(
            self.make_url("/user_skill/user-single/{}".format(user_skill.id)),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        payload = response_json["payload"]

        self.assert200(response)
        self.assertJSONKeyPresent(payload, "user_skill")
        self.assertJSONKeysPresent(payload["user_skill"], "skill_level", "years")
        self.assertEqual(payload["user_skill"]["id"], user_skill.id)
        self.assertEqual(
            payload["user_skill"]["skill_level"],
            user_skill.skill_level,
        )
        self.assertEqual(payload["user_skill"]["years"], user_skill.years)

    def test_update_user_skill_endpoint(self):
        RoleFactory.create()
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_skill", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_proj_data = UserSkillFactory.create()
        user_proj_data.save()
        data = {
            "user_id": user_id,
            "user_skill_id": user_proj_data.id,
            "skill_id": user_proj_data.skill_id,
            "skill_level": user_proj_data.skill_level,
            "years": user_proj_data.years,
        }
        response = self.client().put(
            self.make_url("/user_skill/{}".format(user_proj_data.id)),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["user_skill"]["skill_id"], data["skill_id"])

    def test_invalid_update(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_skill", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        user_proj_data = UserSkillFactory.create(skill_id=self.skill_one.id)
        user_proj_data.save()

        data = {
            "user_id": user_id,
            "skill_id": user_proj_data.skill_id,
            "expert_level": user_proj_data.skill_level,
            "years": user_proj_data.years,
        }
        response = self.client().put(
            self.make_url("/user_skill/1000"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        self.assert400(response)

    def test_delete_user_skill_endpoint_with_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="delete_user_skill", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        user_proj_data = UserSkillFactory.create()
        user_proj_data.save()

        response = self.client().delete(
            self.make_url(f"/user_skill/{user_proj_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(response_json["msg"], "user skill deleted")

    def test_delete_user_skill_endpoint_without_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        UserRoleFactory.create(user_id=user_id, role=role)
        user_proj_data = UserSkillFactory.create()
        user_proj_data.save()

        response = self.client().delete(
            self.make_url(f"/user_skill/{user_proj_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert401(response)
        self.assertEqual(response_json["msg"], "Access Error - No Permission Granted")

    def test_delete_user_skill_endpoint_with_wrong_user_skill_id(self):
        role1 = RoleFactory.create(name="admin")

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(
            keyword="delete_user_skill",
            name="delete_user_skill",
            role=role1,
        )

        UserRoleFactory.create(user_id=user_id, role=role1)
        user_proj_data = UserSkillFactory.create()
        user_proj_data.save()

        response = self.client().delete(
            self.make_url("/user_skill/1576"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert404(response)
        self.assertEqual(
            response_json["msg"], "Invalid or incorrect user_skill_id provided"
        )
