"""Unit tests for the user education controller.
"""
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.controllers.user_education_controller import UserEducationController
from app.models import User
from app.models.permission import Permission
from app.models.user_education import UserEducation
from app.repositories import UserRepo
from app.repositories.user_education_repo import UserEducationRepo
from app.repositories.permission_repo import PermissionRepo

# from app.services.andela import AndelaService
from factories import UserFactory
from tests.base_test_case import BaseTestCase


class TestUserEducationController(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.mock_user = UserFactory.create()
        self.mock_user.save()
        self.mock_user_education = UserEducation(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=self.mock_user.id,
            institution_name="University of Ibadan",
            course_name="Physcology",
            degree_earned="B.Sc",
            accomplishments="db.Column(db.Text, nullable=False)",
            start_date="2004-12-01",
            end_date="2010-12-01",
            is_deleted=False,
        )

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(UserEducationRepo, "get_unpaginated")
    def test_list_user_education_ok_response(
        self,
        mock_user_education_repo_get_unpaginated,
    ):
        """Test list_user_education OK response."""
        # Arrange
        with self.app.app_context():

            mock_user_education_repo_get_unpaginated.return_value.items = [
                self.mock_user_education,
            ]
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.list_user_education(self.mock_user.id)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserEducationRepo, "get")
    def test_get_user_education_when_invalid_or_missing(
        self, mock_user_education_repo_get
    ):
        """Test get_user_education invalid repo response."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = None
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.get_user_education(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Invalid User Education or Missing user_education_id"
            )

    @patch.object(UserEducationRepo, "get")
    def test_get_user_education_ok_response(self, mock_user_education_repo_get):
        """Test get_user_education OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = self.mock_user_education
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.get_user_education(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserEducationController, "request_params")
    @patch.object(UserEducationRepo, "find_first")
    def test_create_user_education_ok_response(
        self,
        mock_user_education_repo_find_first,
        mock_user_education_controller_request_params,
    ):
        """Test create_user_education OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_education_controller_request_params.return_value = (
                self.mock_user.id,
                "institution_name",
                "course_name",
                "degree_earned",
                "accomplishments",
                "2016-12-01",
                "2020-06-10",
            )
            mock_user_education_repo_find_first.return_value = None
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.create_user_education()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserEducationController, "request_params")
    @patch.object(UserEducationRepo, "get")
    def test_update_user_education_when_user_education_doesnot_exist(
        self,
        mock_user_education_repo_get,
        mock_user_education_controller_request_params,
    ):
        """Test update_user_education when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = None
            mock_user_education_controller_request_params.return_value = (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.update_user_education(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_education_id provided"
            )

    @patch.object(UserEducationRepo, "find_first")
    @patch.object(UserEducationController, "request_params")
    @patch.object(UserEducationRepo, "get")
    def test_update_user_education_ok_response(
        self,
        mock_user_education_repo_get,
        mock_user_education_controller_request_params,
        mock_user_education_repo_find_first,
    ):
        """Test update_user_education ."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = self.mock_user_education
            mock_user_education_repo_find_first.return_value = None
            mock_user_education_controller_request_params.return_value = (
                self.mock_user.id,
                self.mock_user_education.id,
                "institution_name",
                "course_name",
                "degree_earned",
                "accomplishments",
                "2016-12-01",
                "2020-06-10",
            )
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.update_user_education(
                self.mock_user_education.id
            )

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserEducationRepo, "find_first")
    @patch.object(UserEducationController, "request_params")
    @patch.object(UserEducationRepo, "get")
    def test_update_user_education_invalid_response(
        self,
        mock_user_education_repo_get,
        mock_user_education_controller_request_params,
        mock_user_education_repo_find_first,
    ):
        """Test update_user_education when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = self.mock_user_education
            mock_user_education_repo_find_first.return_value = None
            mock_user_education_controller_request_params.return_value = (
                self.mock_user.id,
                self.mock_user_education.id,
                "institution_name",
                "course_name",
                "degree_earned",
                "accomplishments",
                "2016-12-01",
                "2020-06-10",
            )
            user_education_controller = UserEducationController(self.request_context)

            # Act
            result = user_education_controller.update_user_education(
                self.mock_user_education.id
            )

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserEducationRepo, "get")
    def test_delete_user_education_when_user_education_is_invalid(
        self, mock_user_education_repo_get
    ):
        """Test delete_user_education when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = None
            user_education_controler = UserEducationController(self.request_context)

            # Act
            result = user_education_controler.delete_user_education(1)

            # Assert
            assert result.status_code == 404
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_education_id provided"
            )

    @patch.object(UserEducationRepo, "get")
    @patch.object(UserEducationRepo, "update")
    def test_delete_user_education_ok_response(
        self, mock_user_education_repo_update, mock_user_education_repo_get
    ):
        """Test delete_user_education when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_education_repo_get.return_value = self.mock_user_education
            mock_user_education_repo_update.return_value = self.mock_user_education
            user_education_controler = UserEducationController(self.request_context)

            # Act
            result = user_education_controler.delete_user_education(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "user education deleted"
