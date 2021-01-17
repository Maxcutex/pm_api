from app.models import UserProject
from tests.base_test_case import BaseTestCase
from factories.user_project_factory import UserProjectFactoryFake
from factories.user_factory import UserFactory
from app.repositories.user_project_repo import UserProjectRepo


class TestUserProjectRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserProjectRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_project_method_returns_new_user_project_object(self):
        user = UserFactory.create()
        user.save()
        user_project = UserProjectFactoryFake.build(user=user, user_id=user.id)
        new_user_project = self.repo.new_user_project(
            user_id=user.id,
            project_name=user_project.project_name,
            project_url=user_project.project_url,
            project_description=user_project.project_description,
            start_date=user_project.start_date,
            end_date=user_project.end_date,
            is_current=False,
        )
        self.assertIsInstance(new_user_project, UserProject)
        self.assertEqual(str(new_user_project.user_id), str(user.id))
