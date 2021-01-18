from app.models import UserEmploymentSkill
from tests.base_test_case import BaseTestCase
from factories.user_employment_factory import (
    UserEmploymentSkillFactoryFake,
    UserEmploymentFactory,
    SkillFactory,
)
from factories.user_factory import UserFactory
from app.repositories.user_employment_skill_repo import UserEmploymentSkillRepo


class TestUserEmploymentSkillRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserEmploymentSkillRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_employment_skill_method_returns_new_user_employment_skill_object(
        self,
    ):
        user = UserFactory.create()
        user.save()

        user_employment = UserEmploymentFactory.create()
        user_employment.save()

        skill = SkillFactory()
        skill.save()

        user_employment_skill = UserEmploymentSkillFactoryFake.build(
            user_employment_id=user_employment.id, skill_id=skill.id
        )
        new_user_employment_skill = self.repo.new_user_employment_skill(
            user_employment_id=user_employment_skill.user_employment_id,
            skill_id=user_employment_skill.skill_id,
        )
        self.assertIsInstance(new_user_employment_skill, UserEmploymentSkill)
        self.assertEqual(str(new_user_employment_skill.skill_id), str(skill.id))
