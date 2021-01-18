"""
Unit tests for the User Project Controller.
"""
from datetime import datetime, date
from unittest.mock import patch

from app.controllers.user_project_controller import UserProjectController
from app.models import User, UserProject, UserProjectSkill
from app.repositories.user_project_repo import UserProjectRepo
from factories.skill_category_factory import (
    CategoryWithSkillsFactory,
)
from tests.base_test_case import BaseTestCase


class TestUserProjectController(BaseTestCase):
    def setUp(self):
        self.BaseSetUp()
        self.skill_category = CategoryWithSkillsFactory.create(skills=4)
        self.skill_category.save()
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
        self.mock_user_project = UserProject(
            id=1,
            project_name="InstitutionName",
            project_url="InstitutionName",
            project_description="InstitutionName",
            start_date=date(year=2018, month=1, day=31),
            end_date=date(year=2020, month=1, day=31),
            user_id=self.mock_user.id,
            is_current=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_user_project_skill = UserProjectSkill(
            user_project_id=self.mock_user_project.id, skill_id=self.skill_one.id
        )

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(UserProjectRepo, "get_unpaginated")
    def test_list_user_projects_ok_response(
        self,
        mock_user_project_repo_get_unpaginated,
    ):
        """Test list_user_projects OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get_unpaginated.return_value.items = [
                self.mock_user_project,
            ]
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.list_user_projects(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserProjectRepo, "get")
    def test_get_user_project_when_invalid_or_missing(self, mock_user_project_repo_get):
        """Test get_user_project invalid repo response."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get.return_value = None
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.get_user_project(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Invalid User Project or Missing user_project_id"
            )

    @patch.object(UserProjectRepo, "get")
    def test_get_user_project_ok_response(self, mock_user_project_repo_get):
        """Test get_user_project OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get.return_value = self.mock_user_project
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.get_user_project(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            # import pdb
            # pdb.set_trace()
            # assert result.get_json()["payload"]["user_project"]["skills"][0] == "OK"
            # assert result.get_json()["msg"] == "OK"

    @patch.object(UserProjectController, "request_params")
    def test_create_user_project_start_date_less_than_end_date_response(
        self,
        mock_user_project_controller_request_params,
    ):
        """
        Test create user project is invalid when start date is greater than end date

        :param mock_user_project_controller_request_params:
        :return:
        """
        with self.app.app_context():
            mock_user_project_controller_request_params.return_value = (
                1,
                "Institution name",
                "http://www.test.com",
                "Job title",
                date(year=2028, month=1, day=31),
                date(year=2020, month=1, day=31),
                False,
                [self.skill_one.id, self.skill_two.id],
            )
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.create_user_project()

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Start Date cannot be greater than End date "
            )

    @patch.object(UserProjectController, "request_params")
    @patch.object(UserProjectRepo, "find_first")
    def test_create_user_project_ok_response(
        self,
        mock_user_project_repo_find_first,
        mock_user_project_controller_request_params,
    ):
        """Test create_user_project OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_project_controller_request_params.return_value = (
                1,
                "Institution name",
                "http://www.test.com",
                "Job title",
                date(year=2018, month=1, day=31),
                date(year=2020, month=1, day=31),
                False,
                [self.skill_one.id, self.skill_two.id],
            )
            mock_user_project_repo_find_first.return_value = None
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.create_user_project()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"
            assert (
                result.get_json()["payload"]["user_project"]["skills"][0]["name"]
                == self.skill_one.name
            )

    @patch.object(UserProjectController, "request_params")
    @patch.object(UserProjectRepo, "get")
    def test_update_user_project_when_user_project_doesnot_exist(
        self,
        mock_user_project_repo_get,
        mock_user_project_controller_request_params,
    ):
        """Test update_user_project when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get.return_value = None
            mock_user_project_controller_request_params.return_value = (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.update_user_project(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_project_id provided"
            )

    @patch.object(UserProjectRepo, "find_first")
    @patch.object(UserProjectController, "request_params")
    @patch.object(UserProjectRepo, "get")
    def test_update_user_project_ok_response(
        self,
        mock_user_project_repo_get,
        mock_user_project_controller_request_params,
        mock_user_project_repo_find_first,
    ):
        """Test update_user_project when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get.return_value = self.mock_user_project
            mock_user_project_repo_find_first.return_value = None
            mock_user_project_controller_request_params.return_value = (
                1,
                1,
                "Institution name",
                "http://www.test.com",
                "Job title",
                date(year=2018, month=1, day=31),
                date(year=2020, month=1, day=31),
                True,
                [self.skill_one.id, self.skill_two.id],
            )
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.update_user_project(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            assert (
                result.get_json()["payload"]["user_project"]["skills"][0]["name"]
                == self.skill_one.name
            )

    @patch.object(UserProjectRepo, "get")
    def test_delete_user_project_when_user_project_is_invalid(
        self, mock_user_project_repo_get
    ):
        """Test delete_user_project when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get.return_value = None
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.delete_user_project(1)

            # Assert
            assert result.status_code == 404
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_project_id provided"
            )

    @patch.object(UserProjectRepo, "get")
    @patch.object(UserProjectRepo, "update")
    def test_delete_user_project_ok_response(
        self, mock_user_project_repo_update, mock_user_project_repo_get
    ):
        """Test delete_user_project when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_project_repo_get.return_value = self.mock_user_project
            mock_user_project_repo_update.return_value = self.mock_user_project
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.delete_user_project(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "user project deleted"

    @patch.object(UserProjectController, "request_params")
    @patch.object(UserProjectRepo, "find_first")
    def test_user_project_create_with_skills_valid(
        self,
        mock_user_project_repo_find_first,
        mock_user_project_controller_request_params,
    ):
        """
        Test create_user_project with skills OK response.
        """
        # Arrange
        with self.app.app_context():
            mock_user_project_controller_request_params.return_value = (
                1,
                "Institution name",
                "http://www.test.com",
                "Job title",
                date(year=2018, month=1, day=31),
                date(year=2020, month=1, day=31),
                False,
                [self.skill_one.id, self.skill_two.id],
            )
            mock_user_project_repo_find_first.return_value = None
            user_project_controller = UserProjectController(self.request_context)

            # Act
            result = user_project_controller.create_user_project()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"

    def test_user_project_create_with_skills_invalid_skills(self):
        pass
