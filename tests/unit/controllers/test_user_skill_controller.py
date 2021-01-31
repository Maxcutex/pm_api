"""
Unit tests for the User Skills Controller.
"""
from datetime import datetime, date
from unittest.mock import patch

from app.controllers.user_skill_controller import UserSkillController
from app.models import User, UserSkill
from app.repositories.user_skill_repo import UserSkillRepo
from factories import UserFactory
from factories.skill_category_factory import (
    CategoryWithSkillsFactory,
)
from factories.user_factory import UserFactoryFake
from factories.user_skill_factory import UserSkillFactory
from tests.base_test_case import BaseTestCase


class TestUserSkillController(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.skill_category = CategoryWithSkillsFactory.create(skills=4)
        self.skill_category.save()
        self.user = UserFactory.create()
        self.user.save()
        self.skill_one = self.skill_category.skills[0]
        self.skill_two = self.skill_category.skills[1]
        self.skill_three = self.skill_category.skills[2]
        self.skill_four = self.skill_category.skills[3]
        self.mock_user = User(
            id=1,
            first_name="test",
            last_name="test",
            gender="male",
            password="test",
            is_active=True,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_user_skill = UserSkillFactory.create(
            skill_level="expert",
            years=4,
            skill=self.skill_one,
            user=self.user,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_user_skill.save()

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(UserSkillRepo, "get_unpaginated")
    def test_list_user_skills_ok_response(
        self,
        mock_user_skill_repo_get_unpaginated,
    ):
        """Test list_user_skills OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get_unpaginated.return_value.items = [
                self.mock_user_skill,
            ]
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.list_user_skills(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserSkillRepo, "get")
    def test_get_user_skill_when_invalid_or_missing(self, mock_user_skill_repo_get):
        """Test get_user_skill invalid repo response."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get.return_value = None
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.get_user_skill(99)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Invalid User Project or Missing user_skill_id"
            )

    @patch.object(UserSkillRepo, "get")
    def test_get_user_skill_ok_response(self, mock_user_skill_repo_get):
        """Test get_user_skill OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get.return_value = self.mock_user_skill
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.get_user_skill(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            # import pdb
            # pdb.set_trace()
            # assert result.get_json()["payload"]["user_skill"]["skills"][0] == "OK"
            # assert result.get_json()["msg"] == "OK"

    @patch.object(UserSkillController, "request_params")
    @patch.object(UserSkillRepo, "find_first")
    def test_create_user_skill_ok_response(
        self,
        mock_user_skill_repo_find_first,
        mock_user_skill_controller_request_params,
    ):
        """Test create_user_skill OK response."""
        # Arrange
        user = UserFactoryFake.build()
        with self.app.app_context():
            mock_user_skill_controller_request_params.return_value = (
                "expert",
                5,
                self.skill_one.id,
                user.id,
            )
            mock_user_skill_repo_find_first.return_value = None
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.create_user_skill()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"
            assert (
                result.get_json()["payload"]["user_skill"]["skill_id"]
                == self.skill_one.id
            )

    @patch.object(UserSkillController, "request_params")
    @patch.object(UserSkillRepo, "get")
    def test_update_user_skill_when_user_skill_doesnot_exist(
        self,
        mock_user_skill_repo_get,
        mock_user_skill_controller_request_params,
    ):
        """Test update_user_skill when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get.return_value = None
            mock_user_skill_controller_request_params.return_value = (
                None,
                None,
                None,
                None,
                None,
            )
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.update_user_skill(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_skill_id provided"
            )

    @patch.object(UserSkillRepo, "find_first")
    @patch.object(UserSkillController, "request_params")
    @patch.object(UserSkillRepo, "get")
    def test_update_user_skill_ok_response(
        self,
        mock_user_skill_repo_get,
        mock_user_skill_controller_request_params,
        mock_user_skill_repo_find_first,
    ):
        """Test update_user_skill when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get.return_value = self.mock_user_skill
            mock_user_skill_repo_find_first.return_value = self.mock_user_skill
            mock_user_skill_controller_request_params.return_value = (
                self.user.id,
                self.mock_user_skill.id,
                "expert",
                5,
                self.skill_one.id,
            )
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.update_user_skill(self.mock_user_skill.id)
            print(result)
            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            assert (
                result.get_json()["payload"]["user_skill"]["skill_id"]
                == self.skill_one.id
            )

    @patch.object(UserSkillRepo, "get")
    def test_delete_user_skill_when_user_skill_is_invalid(
        self, mock_user_skill_repo_get
    ):
        """Test delete_user_skill when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get.return_value = None
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.delete_user_skill(1)

            # Assert
            assert result.status_code == 404
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_skill_id provided"
            )

    @patch.object(UserSkillRepo, "get")
    @patch.object(UserSkillRepo, "update")
    def test_delete_user_skill_ok_response(
        self, mock_user_skill_repo_update, mock_user_skill_repo_get
    ):
        """Test delete_user_skill when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_skill_repo_get.return_value = self.mock_user_skill
            mock_user_skill_repo_update.return_value = self.mock_user_skill
            user_skill_controller = UserSkillController(self.request_context)

            # Act
            result = user_skill_controller.delete_user_skill(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "user skill deleted"
