from app.models import SkillsCategory
from app.repositories.skills_category_repo import SkillsCategoryRepo
from factories.skill_category_factory import SkillsCategoryFactoryFake
from tests.base_test_case import BaseTestCase


class TestSkillsCategoryRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = SkillsCategoryRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_category_method_returns_new_category_object(self):
        skill_category = SkillsCategoryFactoryFake.build()

        new_skill_category = self.repo.new_skills_category(
            skill_category.name,
            skill_category.help,
        )
        self.assertIsInstance(new_skill_category, SkillsCategory)
        self.assertEqual(new_skill_category.name, skill_category.name)
