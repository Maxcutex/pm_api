from app.models import UserSkill
from app.repositories.user_skill_repo import UserSkillRepo
from factories.user_skill_factory import UserSkillFactoryFake
from tests.base_test_case import BaseTestCase


class TestUserSkillRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserSkillRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_skill_method_returns_new_user_skill_object(self):
        user_skill = UserSkillFactoryFake.build()

        new_user_skill = self.repo.new_user_skill(
            user_skill.skill_level,
            user_skill.years,
            user_skill.skill_id,
            user_skill.user_id,
        )
        self.assertIsInstance(new_user_skill, UserSkill)
        self.assertEqual(new_user_skill.skill_level, user_skill.skill_level)
