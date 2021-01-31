from datetime import datetime, date

from tests.base_test_case import BaseTestCase
from factories import (
    UserEducationFactory,
    UserEducationFactoryFake,
    PermissionFactory,
    UserRoleFactory,
    RoleFactory,
    UserFactory,
)


class TestUserEducationEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_user_education_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="create_user_education", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_emp_data = UserEducationFactoryFake.build(
            start_date=date(year=2018, month=1, day=31),
            end_date=date(year=2028, month=1, day=31),
        )
        data = {
            "user_id": user_id,
            "institution_name": user_emp_data.institution_name,
            "course_name": user_emp_data.course_name,
            "degree_earned": user_emp_data.degree_earned,
            "accomplishments": user_emp_data.accomplishments,
            "institution_city": user_emp_data.institution_city,
            "institution_country": user_emp_data.institution_country,
            "start_date": str(user_emp_data.start_date),
            "end_date": str(user_emp_data.end_date),
        }

        response = self.client().post(
            self.make_url("/user_education/"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        print(response_json)
        payload = response_json["payload"]

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, "payload")
        self.assertEqual(
            payload["user_education"]["institution_name"],
            user_emp_data.institution_name,
        )
        self.assertEqual(
            payload["user_education"]["course_name"], user_emp_data.course_name
        )

    def test_list_user_education_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_education", role=role1)
        user = UserFactory.create()
        user.save()
        UserRoleFactory.create(user=user, role=role1)
        UserEducationFactory.create_batch(3, user=user)

        response = self.client().get(
            self.make_url(f"/user_education/user/{user.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]
        self.assert200(response)
        self.assertEqual(len(payload["user_education"]), 3)
        self.assertJSONKeysPresent(
            payload["user_education"][0], "institution_name", "course_name"
        )

    def test_get_specific_user_education_endpoint(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_education", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        user_education = UserEducationFactory.create()
        user_education.save()
        response = self.client().get(
            self.make_url("/user_education/user-single/{}".format(user_education.id)),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        payload = response_json["payload"]

        self.assert200(response)
        self.assertJSONKeyPresent(payload, "user_education")
        self.assertJSONKeysPresent(
            payload["user_education"], "institution_name", "course_name"
        )
        self.assertEqual(payload["user_education"]["id"], user_education.id)
        self.assertEqual(
            payload["user_education"]["institution_name"],
            user_education.institution_name,
        )
        self.assertEqual(
            payload["user_education"]["course_name"], user_education.course_name
        )

    def test_update_user_education_endpoint(self):
        RoleFactory.create()
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_education", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_emp_data = UserEducationFactory.create()
        user_emp_data.save()
        data = {
            "user_id": user_id,
            "user_education_id": user_emp_data.id,
            "institution_name": user_emp_data.institution_name,
            "course_name": user_emp_data.course_name,
            "degree_earned": user_emp_data.degree_earned,
            "accomplishments": user_emp_data.accomplishments,
            "institution_city": user_emp_data.institution_city,
            "institution_country": user_emp_data.institution_country,
            "start_date": str(user_emp_data.start_date),
            "end_date": str(user_emp_data.end_date),
        }
        response = self.client().put(
            self.make_url("/user_education/{}".format(user_emp_data.id)),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(
            payload["user_education"]["institution_name"], data["institution_name"]
        )

    def test_invalid_update(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_education", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        user_emp_data = UserEducationFactory.create()
        user_emp_data.save()

        data = {
            "user_id": user_id,
            "user_education_id": user_emp_data.id,
            "institution_name": user_emp_data.institution_name,
            "course_name": user_emp_data.course_name,
            "degree_earned": user_emp_data.degree_earned,
            "accomplishments": user_emp_data.accomplishments,
            "institution_city": user_emp_data.institution_city,
            "institution_country": user_emp_data.institution_country,
            "start_date": str(user_emp_data.start_date),
            "end_date": str(user_emp_data.end_date),
        }
        response = self.client().put(
            self.make_url("/user_education/1000"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        self.assert400(response)

    def test_delete_user_education_endpoint_with_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="delete_user_education", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        user_emp_data = UserEducationFactory.create()
        user_emp_data.save()

        response = self.client().delete(
            self.make_url(f"/user_education/{user_emp_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(response_json["msg"], "user education deleted")

    def test_delete_user_education_endpoint_without_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        UserRoleFactory.create(user_id=user_id, role=role)
        user_emp_data = UserEducationFactory.create()
        user_emp_data.save()

        response = self.client().delete(
            self.make_url(f"/user_education/{user_emp_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert401(response)
        self.assertEqual(response_json["msg"], "Access Error - No Permission Granted")

    def test_delete_user_education_endpoint_with_wrong_user_education_id(self):
        role1 = RoleFactory.create(name="admin")

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(
            keyword="delete_user_education",
            name="delete_user_education",
            role=role1,
        )

        UserRoleFactory.create(user_id=user_id, role=role1)
        user_emp_data = UserEducationFactory.create()
        user_emp_data.save()

        response = self.client().delete(
            self.make_url("/user_education/1576"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert404(response)
        self.assertEqual(
            response_json["msg"], "Invalid or incorrect user_education_id provided"
        )
