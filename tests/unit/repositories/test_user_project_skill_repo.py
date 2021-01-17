from app.models import UserProjectSkill
from tests.base_test_case import BaseTestCase
from factories.user_project_factory import (
    UserProjectSkillFactoryFake,
    UserProjectFactory,
    SkillFactory,
)
from factories.user_factory import UserFactory
from app.repositories.user_project_skill_repo import UserProjectSkillRepo


class TestUserProjectSkillRepo(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.repo = UserProjectSkillRepo()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_user_project_skill_method_returns_new_user_project_skill_object(
        self,
    ):
        user = UserFactory.create()
        user.save()

        user_project = UserProjectFactory.create()
        user_project.save()

        skill = SkillFactory()
        skill.save()

        user_project_skill = UserProjectSkillFactoryFake.build(
            user_project_id=user_project.id, skill_id=skill.id
        )
        new_user_project_skill = self.repo.new_user_project_skill(
            user_project_id=user_project_skill.user_project_id,
            skill_id=user_project_skill.skill_id,
        )
        self.assertIsInstance(new_user_project_skill, UserProjectSkill)
        self.assertEqual(str(new_user_project_skill.skill_id), str(skill.id))
