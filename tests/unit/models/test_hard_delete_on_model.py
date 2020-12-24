from tests.base_test_case import BaseTestCase

from app.models import User, Activity


class TestHardDelete(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_hard_delete_on_user_model(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
        )

        user.save()
        user_id = user.id

        user.delete()

        self.assertEquals(User.query.get(user_id), None)

    def test_creating_vendor_gets_logged(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
        )

        user.save()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("created" in activity[0])

    def test_updating_vendor_gets_logged(self):
        user = User(
            first_name="Fist name",
            last_name="Last name",
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
        )

        user.save()

        user = User.query.get(1)
        user.delete()

        activity = [activity.action_details for activity in Activity.query.all()]

        self.assertTrue("hard deleted" in activity[-1])
