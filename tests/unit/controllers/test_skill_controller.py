"""Unit tests for the skill controller.
"""
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.controllers.skill_controller import SkillController
from app.models import User
from app.models.permission import Permission
from app.models.skill import Skill
from app.repositories import UserRepo
from app.repositories.skill_repo import SkillRepo
from app.repositories.permission_repo import PermissionRepo
from factories import SkillCategoryFactory, SkillFactory

from tests.base_test_case import BaseTestCase


class TestSkillController(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.mock_skill_category = SkillCategoryFactory.create()
        self.mock_skill_category.save()

        self.mock_skill = Skill(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Mock skill",
            skill_category_id=self.mock_skill_category.id,
            skill_category=self.mock_skill_category,
        )
        self.mock_skill.save()
        self.mock_skill2 = SkillFactory.create(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Mock skill2",
            skill_category_id=self.mock_skill_category.id,
            skill_category=self.mock_skill_category,
        )
        self.mock_skill2.save()

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(SkillRepo, "get_unpaginated")
    def test_list_skill_ok_response(
        self,
        mock_skill_repo_get_unpaginated,
    ):
        """Test list_skill OK response."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get_unpaginated.return_value.items = [
                self.mock_skill,
            ]
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.list_skills()
            print(result.__dict__)
            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillRepo, "find_first")
    def test_get_skill_when_invalid_or_missing(self, mock_skill_repo_find_first):
        """Test get_skill invalid repo response."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_find_first.return_value = None
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.get_skill(99)

            # Assert
            assert result.status_code == 400
            assert result.get_json()["msg"] == "Invalid or Missing skill_id"

    @patch.object(SkillRepo, "find_first")
    def test_get_skill_ok_response(self, mock_skill_repo_find_first):
        """Test get_skill OK response."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_find_first.return_value = self.mock_skill
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.get_skill(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillController, "request_params")
    @patch.object(SkillRepo, "find_first")
    def test_create_skill_when_name_and_category_id_already_exists(
        self,
        mock_skill_repo_find_first,
        mock_skill_controller_request_params,
    ):
        """Test create_skill when name and category id already exists."""
        # Arrange
        with self.app.app_context():

            mock_skill_controller_request_params.return_value = (
                self.mock_skill.name,
                self.mock_skill.skill_category_id,
            )
            mock_skill_repo_find_first.return_value = self.mock_skill
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.create_skill()

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == f"Skill name {self.mock_skill.name} with category name "
                f"{self.mock_skill.skill_category.name} already exists"
            )

    @patch.object(SkillController, "request_params")
    @patch.object(SkillRepo, "find_first")
    def test_create_skill_ok_response(
        self,
        mock_skill_repo_find_first,
        mock_skill_controller_request_params,
    ):
        """Test create_skill OK response."""
        # Arrange
        with self.app.app_context():
            mock_skill_controller_request_params.return_value = (
                "Skill Name",
                self.mock_skill_category.id,
            )
            mock_skill_repo_find_first.return_value = None
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.create_skill()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillController, "request_params")
    @patch.object(SkillRepo, "find_first")
    @patch.object(SkillRepo, "get")
    def test_update_skill_when_skill_doesnot_exist(
        self,
        mock_skill_repo_get,
        mock_skill_repo_find_first,
        mock_skill_controller_request_params,
    ):
        """Test update_skill when skill doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get.return_value = None
            mock_skill_repo_find_first.return_value = None
            mock_skill_controller_request_params.return_value = (
                99,
                None,
                None,
            )
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.update_skill(99)

            # Assert
            assert result.status_code == 404
            assert result.get_json()["msg"] == "Skill Not Found"

    @patch.object(SkillRepo, "get")
    @patch.object(SkillRepo, "find_first")
    @patch.object(SkillController, "request_params")
    def test_update_skill_when_name_is_already_taken(
        self,
        mock_skill_controller_request_params,
        mock_skill_repo_find_first,
        mock_skill_repo_get,
    ):
        """Test update_skill when name already exists."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get.return_value = self.mock_skill2
            mock_skill_repo_find_first.return_value = self.mock_skill
            mock_skill_controller_request_params.return_value = (
                self.mock_skill.id,
                self.mock_skill2.name,
                self.mock_skill_category.id,
            )
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.update_skill(self.mock_skill.id)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == f"Skill name 'Mock skill2' with category name {self.mock_skill_category.name} already exists"
            )

    @patch.object(SkillRepo, "find_first")
    @patch.object(SkillController, "request_params")
    @patch.object(SkillRepo, "get")
    def test_update_skill_when_id_do_not_match(
        self,
        mock_skill_repo_get,
        mock_skill_controller_request_params,
        mock_skill_repo_find_first,
    ):
        """Test update_skill when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get.return_value = self.mock_skill
            mock_skill_repo_find_first.return_value = self.mock_skill
            mock_skill_controller_request_params.return_value = (
                "Mock name",
                "Mock help",
                8,
            )
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.update_skill(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()["msg"] == "Invalid or incorrect skill_id provided"

    @patch.object(SkillRepo, "get")
    @patch.object(SkillRepo, "find_first")
    @patch.object(SkillController, "request_params")
    def test_update_skill_ok_response(
        self,
        mock_skill_controller_request_params,
        mock_skill_repo_find_first,
        mock_skill_repo_get,
    ):
        """Test update_skill when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get.return_value = self.mock_skill
            mock_skill_repo_find_first.return_value = self.mock_skill
            mock_skill_controller_request_params.return_value = (
                self.mock_skill.id,
                "New mockwer",
                self.mock_skill.skill_category_id,
            )
            skill_controller = SkillController(self.request_context)

            # Act
            result = skill_controller.update_skill(self.mock_skill.id)
            print(result.__dict__)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillRepo, "get")
    def test_delete_skill_when_skill_is_invalid(self, mock_skill_repo_get):
        """Test delete_skill when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get.return_value = None
            skill_controler = SkillController(self.request_context)

            # Act
            result = skill_controler.delete_skill(1)

            # Assert
            assert result.status_code == 404
            assert (
                result.get_json()["msg"] == "Invalid or incorrect " "skill_id provided"
            )

    @patch.object(SkillRepo, "get")
    @patch.object(SkillRepo, "update")
    def test_delete_skill_ok_response(
        self, mock_skill_repo_update, mock_skill_repo_get
    ):
        """Test delete_skill when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_skill_repo_get.return_value = self.mock_skill
            mock_skill_repo_update.return_value = self.mock_skill
            skill_controler = SkillController(self.request_context)

            # Act
            result = skill_controler.delete_skill(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "skill deleted"
