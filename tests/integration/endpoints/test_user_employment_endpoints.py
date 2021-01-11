from datetime import datetime, date

from tests.base_test_case import BaseTestCase
from factories import (
    UserEmploymentFactory,
    UserEmploymentFactoryFake,
    PermissionFactory,
    UserRoleFactory,
    RoleFactory,
    UserFactory,
)


class TestUserEmploymentEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_user_employment_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword="create_user_employment_history", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_emp_data = UserEmploymentFactoryFake.build(
            start_date=date(year=2018, month=1, day=31),
            end_date=date(year=2028, month=1, day=31),
        )
        data = {
            "user_id": user_id,
            "institution_name": user_emp_data.institution_name,
            "job_title": user_emp_data.job_title,
            "start_date": str(user_emp_data.start_date),
            "end_date": str(user_emp_data.end_date),
            "is_current": user_emp_data.is_current,
        }

        response = self.client().post(
            self.make_url("/user_employment_history/"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, "payload")
        self.assertEqual(
            payload["user_employment"]["institution_name"],
            user_emp_data.institution_name,
        )
        self.assertEqual(
            payload["user_employment"]["job_title"], user_emp_data.job_title
        )

    def test_list_user_employment_endpoint(self):
        role1 = RoleFactory.create(name="admin")
        BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_employment_history", role=role1)
        user = UserFactory.create()
        user.save()
        UserRoleFactory.create(user=user, role=role1)
        UserEmploymentFactory.create_batch(3, user=user)

        response = self.client().get(
            self.make_url(f"/user_employment_history/user/{user.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]
        self.assert200(response)
        self.assertEqual(len(payload["user_employments"]), 3)
        self.assertJSONKeysPresent(
            payload["user_employments"][0], "institution_name", "job_title"
        )

    def test_get_specific_user_employment_endpoint(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="view_user_employment_history", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        user_employment_history = UserEmploymentFactory.create()
        user_employment_history.save()
        response = self.client().get(
            self.make_url(
                "/user_employment_history/user-single/{}".format(
                    user_employment_history.id
                )
            ),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        payload = response_json["payload"]

        self.assert200(response)
        self.assertJSONKeyPresent(payload, "user_employment")
        self.assertJSONKeysPresent(
            payload["user_employment"], "institution_name", "job_title"
        )
        self.assertEqual(payload["user_employment"]["id"], user_employment_history.id)
        self.assertEqual(
            payload["user_employment"]["institution_name"],
            user_employment_history.institution_name,
        )
        self.assertEqual(
            payload["user_employment"]["job_title"], user_employment_history.job_title
        )

    def test_update_user_employment_endpoint(self):
        RoleFactory.create()
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_employment_history", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)
        user_emp_data = UserEmploymentFactory.create()
        user_emp_data.save()
        data = {
            "user_id": user_id,
            "user_employment_id": user_emp_data.id,
            "institution_name": user_emp_data.institution_name,
            "job_title": user_emp_data.job_title,
            "start_date": str(user_emp_data.start_date),
            "end_date": str(user_emp_data.end_date),
            "is_current": user_emp_data.is_current,
        }
        response = self.client().put(
            self.make_url("/user_employment_history/{}".format(user_emp_data.id)),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(
            payload["user_employment"]["institution_name"], data["institution_name"]
        )

    def test_invalid_update(self):
        role1 = RoleFactory.create(name="admin")
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="update_user_employment_history", role=role1)
        UserRoleFactory.create(user_id=user_id, role=role1)

        user_emp_data = UserEmploymentFactory.create()
        user_emp_data.save()

        data = {
            "user_id": user_id,
            "user_employment_id": user_emp_data.id,
            "institution_name": user_emp_data.institution_name,
            "job_title": user_emp_data.job_title,
            "start_date": str(user_emp_data.start_date),
            "end_date": str(user_emp_data.end_date),
            "is_current": user_emp_data.is_current,
        }
        response = self.client().put(
            self.make_url("/user_employment_history/1000"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        self.assert400(response)

    def test_delete_user_employment_endpoint_with_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        PermissionFactory.create(keyword="delete_user_employment_history", role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        user_emp_data = UserEmploymentFactory.create()
        user_emp_data.save()

        response = self.client().delete(
            self.make_url(f"/user_employment_history/{user_emp_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assert200(response)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(response_json["msg"], "user employment deleted")

    def test_delete_user_employment_endpoint_without_right_permission(self):
        role = RoleFactory.create()
        user_id = BaseTestCase.user_id()

        UserRoleFactory.create(user_id=user_id, role=role)
        user_emp_data = UserEmploymentFactory.create()
        user_emp_data.save()

        response = self.client().delete(
            self.make_url(f"/user_employment_history/{user_emp_data.id}"),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert401(response)
        self.assertEqual(response_json["msg"], "Access Error - No Permission Granted")

    def test_delete_user_employment_endpoint_with_wrong_user_employment_id(self):
        role1 = RoleFactory.create(name="admin")

        user_id = BaseTestCase.user_id()
        PermissionFactory.create(
            keyword="delete_user_employment_history",
            name="delete_user_employment_history",
            role=role1,
        )

        UserRoleFactory.create(user_id=user_id, role=role1)
        user_emp_data = UserEmploymentFactory.create()
        user_emp_data.save()

        response = self.client().delete(
            self.make_url("/user_employment_history/1576"), headers=self.headers()
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))

        self.assert404(response)
        self.assertEqual(
            response_json["msg"], "Invalid or incorrect user_employment_id provided"
        )
