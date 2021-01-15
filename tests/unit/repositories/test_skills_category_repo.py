from app.models import SkillCategory
from app.repositories.skill_category_repo import SkillCategoryRepo
from factories.skill_category_factory import SkillCategoryFactoryFake
from tests.base_test_case import BaseTestCase


class TestSkillCategoryRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = SkillCategoryRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_category_method_returns_new_category_object(self):
        skill_category = SkillCategoryFactoryFake.build()

        new_skill_category = self.repo.new_skill_category(
            skill_category.name,
            skill_category.help,
        )
        self.assertIsInstance(new_skill_category, SkillCategory)
        self.assertEqual(new_skill_category.name, skill_category.name)
