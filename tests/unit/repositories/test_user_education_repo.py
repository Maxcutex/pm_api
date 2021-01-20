from app.models import UserEducation
from tests.base_test_case import BaseTestCase
from factories.user_education_factory import UserEducationFactoryFake
from factories.user_factory import UserFactory
from app.repositories.user_education_repo import UserEducationRepo


class TestUserEducationRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserEducationRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_education_method_returns_new_user_education_object(self):
        user = UserFactory.create()
        user.save()
        user_education = UserEducationFactoryFake.build(user=user, user_id=user.id)
        new_user_education = self.repo.new_user_education(
            user_id=user.id,
            institution_name=user_education.institution_name,
            course_name=user_education.course_name,
            degree_earned=user_education.degree_earned,
            start_date=user_education.start_date,
            end_date=user_education.end_date,
            accomplishments=user_education.accomplishments,
        )
        self.assertIsInstance(new_user_education, UserEducation)
        self.assertEqual(str(new_user_education.user_id), str(user.id))
