"""Unit tests for the skills category controller.
"""
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.controllers.skill_category_controller import SkillCategoryController
from app.models import User
from app.models.permission import Permission
from app.models.skill_category import SkillCategory
from app.repositories import UserRepo
from app.repositories.skill_category_repo import SkillCategoryRepo
from app.repositories.permission_repo import PermissionRepo

# from app.services.andela import AndelaService
from tests.base_test_case import BaseTestCase


class TestSkillCategoryController(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.mock_skills_category = SkillCategory(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Mock role",
            help="Mock help",
        )

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(SkillCategoryController, "pagination_meta")
    @patch.object(SkillCategoryRepo, "filter_by")
    def test_list_skills_categorys_ok_response(
        self,
        mock_skills_category_repo_filter_by,
        mock_skills_category_controller_pagination_meta,
    ):
        """Test list_skills_categorys OK response."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_controller_pagination_meta.return_value = {
                "total_rows": 1,
                "total_pages": 1,
                "current_page": 1,
                "next_page": False,
                "prev_page": False,
            }
            mock_skills_category_repo_filter_by.return_value.items = [
                self.mock_skills_category,
            ]
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.list_skills_categories()

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillCategoryRepo, "get")
    def test_get_skills_category_when_invalid_or_missing(
        self, mock_skills_category_repo_get
    ):
        """Test get_skills_category invalid repo response."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = None
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.get_skills_category(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()["msg"] == "Invalid or Missing skills_category_id"

    @patch.object(SkillCategoryRepo, "get")
    def test_get_skills_category_ok_response(self, mock_skills_category_repo_get):
        """Test get_skills_category OK response."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = self.mock_skills_category
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.get_skills_category(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillCategoryController, "request_params")
    @patch.object(SkillCategoryRepo, "find_first")
    def test_create_skills_category_when_name_already_exists(
        self,
        mock_skills_category_repo_find_first,
        mock_skills_category_controller_request_params,
    ):
        """Test create_skills_category when role name already exists."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_controller_request_params.return_value = (
                "Mock name",
                "Mock help",
            )
            mock_skills_category_repo_find_first.return_value = (
                self.mock_skills_category
            )
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.create_skills_category()

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Skills Category with this name already"
                " exists"
            )

    @patch.object(SkillCategoryController, "request_params")
    @patch.object(SkillCategoryRepo, "find_first")
    def test_create_skills_category_ok_response(
        self,
        mock_skills_category_repo_find_first,
        mock_skills_category_controller_request_params,
    ):
        """Test create_skills_category OK response."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_controller_request_params.return_value = (
                "Mock name",
                "Mock help",
            )
            mock_skills_category_repo_find_first.return_value = None
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.create_skills_category()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillCategoryController, "request_params")
    @patch.object(SkillCategoryRepo, "get")
    def test_update_skills_category_when_skills_category_doesnot_exist(
        self,
        mock_skills_category_repo_get,
        mock_skills_category_controller_request_params,
    ):
        """Test update_skills_category when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = None
            mock_skills_category_controller_request_params.return_value = (
                None,
                None,
                None,
            )
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.update_skills_category(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "skills_category_id provided"
            )

    @patch.object(SkillCategoryRepo, "find_first")
    @patch.object(SkillCategoryController, "request_params")
    @patch.object(SkillCategoryRepo, "get")
    def test_update_skills_category_when_name_is_already_taken(
        self,
        mock_skills_category_repo_get,
        mock_skills_category_controller_request_params,
        mock_skills_category_repo_find_first,
    ):
        """Test update_skills_category when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = self.mock_skills_category
            mock_skills_category_repo_find_first.return_value = (
                self.mock_skills_category
            )
            mock_skills_category_controller_request_params.return_value = (
                "Mock name",
                "Mock help",
                1,
            )
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.update_skills_category(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Skills Category with this name"
                " already exists"
            )

    @patch.object(SkillCategoryRepo, "find_first")
    @patch.object(SkillCategoryController, "request_params")
    @patch.object(SkillCategoryRepo, "get")
    def test_update_skills_category_when_id_do_not_match(
        self,
        mock_skills_category_repo_get,
        mock_skills_category_controller_request_params,
        mock_skills_category_repo_find_first,
    ):
        """Test update_skills_category when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = self.mock_skills_category
            mock_skills_category_repo_find_first.return_value = (
                self.mock_skills_category
            )
            mock_skills_category_controller_request_params.return_value = (
                "Mock name",
                "Mock help",
                8,
            )
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.update_skills_category(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Invalid or incorrect skills_category_id provided"
            )

    @patch.object(SkillCategoryRepo, "find_first")
    @patch.object(SkillCategoryController, "request_params")
    @patch.object(SkillCategoryRepo, "get")
    def test_update_skills_category_ok_response(
        self,
        mock_skills_category_repo_get,
        mock_skills_category_controller_request_params,
        mock_skills_category_repo_find_first,
    ):
        """Test update_skills_category when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = self.mock_skills_category
            mock_skills_category_repo_find_first.return_value = None
            mock_skills_category_controller_request_params.return_value = (
                "Mock name",
                "Mock help",
                1,
            )
            skills_category_controller = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controller.update_skills_category(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(SkillCategoryRepo, "get")
    def test_delete_skills_category_when_skills_category_is_invalid(
        self, mock_skills_category_repo_get
    ):
        """Test delete_skills_category when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = None
            skills_category_controler = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controler.delete_skills_category(1)

            # Assert
            assert result.status_code == 404
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "skills_category_id provided"
            )

    @patch.object(SkillCategoryRepo, "get")
    @patch.object(SkillCategoryRepo, "update")
    def test_delete_skills_category_ok_response(
        self, mock_skills_category_repo_update, mock_skills_category_repo_get
    ):
        """Test delete_skills_category when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_skills_category_repo_get.return_value = self.mock_skills_category
            mock_skills_category_repo_update.return_value = self.mock_skills_category
            skills_category_controler = SkillCategoryController(self.request_context)

            # Act
            result = skills_category_controler.delete_skills_category(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "skills category deleted"
