from tests.base_test_case import BaseTestCase
from factories import PermissionFactory, RoleFactory, UserRoleFactory


class TestRoleEndpoints(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_role_endpoint(self):
        # role1 = RoleFactory.create(name="admin")
        # user_id = BaseTestCase.user_id()
        # permission = PermissionFactory.create(keyword="create_roles", role=role1)
        # user_role = UserRoleFactory.create(user_id=user_id, role=role1)

        data = {"name": "Jack Jones", "help": "A Help Message"}
        import pdb

        pdb.set_trace()
        response = self.client().post(
            self.make_url("/roles/"),
            data=self.encode_to_json_string(data),
            headers=self.headers(),
        )
        response_json = self.decode_from_json_string(response.data.decode("utf-8"))
        payload = response_json["payload"]

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, "payload")
        self.assertEqual(payload["role"]["name"], "Jack Jones")
        self.assertEqual(payload["role"]["help"], "A Help Message")

    # def test_list_roles_endpoint(self):
    #
    #     RoleFactory.create_batch(3)
    #     role1 = RoleFactory.create(name='admin')
    #     user_id = BaseTestCase.user_id()
    #
    #     response = self.client().get(self.make_url('/roles/'), headers=self.headers())
    #     response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    #     payload = response_json['payload']
    #
    #     self.assert200(response)
    #     self.assertEqual(len(payload['roles']), 4)
    #     self.assertJSONKeysPresent(payload['roles'][0], 'name', 'help')
    #
    # def test_get_specific_role_endpoint(self):
    #     role = RoleFactory.create()
    #     response = self.client().get(self.make_url('/roles/{}'.format(role.id)), headers=self.headers())
    #     response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    #     payload = response_json['payload']
    #
    #     self.assert200(response)
    #     self.assertJSONKeyPresent(payload, 'role')
    #     self.assertJSONKeysPresent(payload['role'], 'name', 'help')
    #     self.assertEqual(payload['role']['id'], role.id)
    #     self.assertEqual(payload['role']['name'], role.name)
    #     self.assertEqual(payload['role']['help'], role.help)
    #
    # def test_update_roles_endpoint(self):
    #
    #     role = RoleFactory.create()
    #     role1 = RoleFactory.create(name='admin')
    #     user_id = BaseTestCase.user_id()
    #     data = {'name': 'Super Admin'}
    #     response = self.client().put(self.make_url('/roles/{}'
    #     .format(role.id)), data=self.encode_to_json_string(data), headers=self.headers())
    #     response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    #     payload = response_json['payload']
    #
    #     self.assert200(response)
    #     self.assertEqual(payload['role']['name'], data['name'])
    #
    # def test_invalid_update(self):
    #
    #     role1 = RoleFactory.create(name='admin')
    #     user_id = BaseTestCase.user_id()
    #     data = {'name': 'Super Admin'}
    #     response = self.client().put(self.make_url('/roles/1000'), data=self.encode_to_json_string(data), headers=self.headers())
    #     self.assert400(response)
    #
    # def test_delete_role_endpoint_with_right_permission(self):
    #     role = RoleFactory.create()
    #
    #     response = self.client().delete(self.make_url(f'/roles/{role.id}'), headers=self.headers())
    #     response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    #     payload = response_json['payload']
    #
    #     self.assert200(response)
    #     self.assertEqual(payload['status'], 'success')
    #     self.assertEqual(response_json['msg'], 'role deleted')
    #
    # def test_delete_role_endpoint_without_right_permission(self):
    #     role = RoleFactory.create()
    #
    #     response = self.client().delete(self.make_url(f'/roles/{role.id}'), headers=self.headers())
    #     response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    #
    #     self.assert401(response)
    #     self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')
    #
    # def test_delete_role_endpoint_with_wrong_role_id(self):
    #
    #     response = self.client().delete(self.make_url(f'/roles/1576'), headers=self.headers())
    #     response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    #
    #     self.assert404(response)
    #     self.assertEqual(response_json['msg'], 'Invalid or incorrect role_id provided')
    #
