from app.models import Client
from tests.base_test_case import BaseTestCase
from factories.client_factory import ClientFactoryFake
from factories.user_factory import UserFactory
from app.repositories.client_repo import ClientRepo


class TestClientRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = ClientRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_client_method_returns_new_client_object(self):
        user = UserFactory.create()
        user.save()
        client = ClientFactoryFake.build()
        new_client = self.repo.new_client(
            institution_name=client.institution_name,
            institution_url=client.institution_url,
            institution_city=client.institution_city,
            institution_country=client.institution_country,
            institution_size=client.institution_size,
            start_date=client.start_date,
            status=client.status,
        )
        self.assertIsInstance(new_client, Client)
        self.assertEqual(
            str(new_client.institution_name), str(new_client.institution_name)
        )
