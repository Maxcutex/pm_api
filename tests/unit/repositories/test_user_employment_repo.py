from app.models import UserEmployment
from tests.base_test_case import BaseTestCase
from factories.user_employment_factory import UserEmploymentFactoryFake
from factories.user_factory import UserFactory
from app.repositories.user_employment_repo import UserEmploymentRepo


class TestUserEmploymentRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserEmploymentRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_employment_method_returns_new_user_employment_object(self):
        user = UserFactory.create()
        user.save()
        user_employment = UserEmploymentFactoryFake.build(user=user, user_id=user.id)
        new_user_employment = self.repo.new_user_employment(
            user_id=user.id,
            institution_name=user_employment.institution_name,
            job_title=user_employment.job_title,
            employment_type=user_employment.employment_type,
            institution_url=user_employment.institution_url,
            institution_city=user_employment.institution_city,
            institution_country=user_employment.institution_country,
            institution_size=user_employment.institution_size,
            work_summary=user_employment.work_summary,
            accomplishments=user_employment.accomplishments,
            start_date=user_employment.start_date,
            end_date=user_employment.end_date,
            is_current=False,
        )
        self.assertIsInstance(new_user_employment, UserEmployment)
        self.assertEqual(str(new_user_employment.user_id), str(user.id))
