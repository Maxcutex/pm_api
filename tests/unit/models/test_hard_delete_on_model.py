from datetime import datetime

from app.utils.enums import Gender
from tests.base_test_case import BaseTestCase

from app.models import User, Activity, Role


class TestHardDelete(BaseTestCase):
    dev_role = None
    admin_role = None

    def setUp(self):
        self.BaseSetUp()
        self.create_base_roles()

    def tearDown(self):
        self.BaseTearDown()

    def create_base_roles(self):
        dev_role = Role(name="Engineer", help="A webspoons engineer")
        dev_role.save()
        self.dev_role = dev_role

        admin_role = Role(name="Administrator", help="A webspoons Admin")
        admin_role.save()
        self.admin_role = admin_role

    def test_hard_delete_on_user_model(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
            user_type_id=self.dev_role.id,
            date_of_birth=datetime.now(),
            gender=Gender.male,
        )

        user.save()
        user_id = user.id

        user.delete()

        self.assertEquals(User.query.get(user_id), None)

    def test_creating_vendor_gets_logged(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
            user_type_id=self.dev_role.id,
            date_of_birth=datetime.now(),
            gender=Gender.male,
        )

        user.save()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("created" in activity[0])

    def test_updating_vendor_gets_logged(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
            user_type_id=self.dev_role.id,
            date_of_birth=datetime.now(),
            gender=Gender.male,
        )

        user.save()

        user = User.query.get(1)
        user.first_name = "New Name"
        user.save()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("updated" in activity[1])

    def test_hard_deleting_vendor_gets_logged(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
            user_type_id=self.dev_role.id,
            date_of_birth=datetime.now(),
            gender=Gender.male,
        )

        user.save()

        user = User.query.get(1)
        user.delete()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("hard deleted" in activity[-1])
