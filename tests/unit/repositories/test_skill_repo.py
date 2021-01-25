from app.models import Skill
from app.repositories.skill_repo import SkillRepo
from factories.skill_category_factory import SkillFactoryFake
from tests.base_test_case import BaseTestCase


class TestSkillRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = SkillRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_skill_method_returns_new__object(self):
        skill_ = SkillFactoryFake.build()

        new_skill_ = self.repo.new_skill(
            skill_.name,
            skill_.skill_category_id,
        )
        self.assertIsInstance(new_skill_, Skill)
        self.assertEqual(new_skill_.name, skill_.name)
