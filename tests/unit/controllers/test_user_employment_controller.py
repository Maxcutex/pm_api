"""
Unit tests for the User Employment Controller.
"""
from datetime import datetime, date
from unittest.mock import patch

from app.controllers.user_employment_controller import UserEmploymentController
from app.models import User, UserEmployment, UserEmploymentSkill
from app.repositories.user_employment_repo import UserEmploymentRepo
from factories.skill_category_factory import (
    CategoryWithSkillsFactory,
    SkillFactory,
    SkillFactoryFake,
)
from tests.base_test_case import BaseTestCase


class TestUserEmploymentController(BaseTestCase):
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
        self.mock_user_employment = UserEmployment(
            id=1,
            institution_name="InstitutionName",
            job_title="InstitutionName",
            start_date=date(year=2018, month=1, day=31),
            end_date=date(year=2020, month=1, day=31),
            user_id=self.mock_user.id,
            is_current=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.mock_user_employment_skill = UserEmploymentSkill(
            user_employment_id=self.mock_user_employment.id, skill_id=self.skill_one.id
        )

    def tearDown(self):
        self.BaseTearDown()

    @patch.object(UserEmploymentRepo, "get_unpaginated")
    def test_list_user_employments_ok_response(
        self,
        mock_user_employment_repo_get_unpaginated,
    ):
        """Test list_user_employments OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get_unpaginated.return_value.items = [
                self.mock_user_employment,
            ]
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.list_user_employment_history(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"

    @patch.object(UserEmploymentRepo, "get")
    def test_get_user_employment_when_invalid_or_missing(
        self, mock_user_employment_repo_get
    ):
        """Test get_user_employment invalid repo response."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get.return_value = None
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.get_user_employment(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Invalid User Employment or Missing user_employment_id"
            )

    @patch.object(UserEmploymentRepo, "get")
    def test_get_user_employment_ok_response(self, mock_user_employment_repo_get):
        """Test get_user_employment OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get.return_value = self.mock_user_employment
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.get_user_employment(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            # import pdb
            # pdb.set_trace()
            # assert result.get_json()["payload"]["user_employment"]["skills"][0] == "OK"
            # assert result.get_json()["msg"] == "OK"

    @patch.object(UserEmploymentController, "request_params")
    def test_create_user_employment_start_date_less_than_end_date_response(
        self,
        mock_user_employment_controller_request_params,
    ):
        """
        Test create user employment is invalid when start date is greater than end date

        :param mock_user_employment_controller_request_params:
        :return:
        """
        with self.app.app_context():
            mock_user_employment_controller_request_params.return_value = (
                1,
                "Institution name",
                "Job title",
                date(year=2028, month=1, day=31),
                date(year=2020, month=1, day=31),
                False,
                [self.skill_one.id, self.skill_two.id],
            )
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.create_user_employment()

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"]
                == "Start Date cannot be greater than End date "
            )

    @patch.object(UserEmploymentController, "request_params")
    @patch.object(UserEmploymentRepo, "find_first")
    def test_create_user_employment_ok_response(
        self,
        mock_user_employment_repo_find_first,
        mock_user_employment_controller_request_params,
    ):
        """Test create_user_employment OK response."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_controller_request_params.return_value = (
                1,
                "Institution name",
                "Job title",
                date(year=2018, month=1, day=31),
                date(year=2020, month=1, day=31),
                False,
                [self.skill_one.id, self.skill_two.id],
            )
            mock_user_employment_repo_find_first.return_value = None
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.create_user_employment()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"
            assert (
                result.get_json()["payload"]["user_employment"]["skills"][0]["name"]
                == self.skill_one.name
            )

    @patch.object(UserEmploymentController, "request_params")
    @patch.object(UserEmploymentRepo, "get")
    def test_update_user_employment_when_user_employment_doesnot_exist(
        self,
        mock_user_employment_repo_get,
        mock_user_employment_controller_request_params,
    ):
        """Test update_user_employment when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get.return_value = None
            mock_user_employment_controller_request_params.return_value = (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.update_user_employment(1)

            # Assert
            assert result.status_code == 400
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_employment_id provided"
            )

    @patch.object(UserEmploymentRepo, "find_first")
    @patch.object(UserEmploymentController, "request_params")
    @patch.object(UserEmploymentRepo, "get")
    def test_update_user_employment_ok_response(
        self,
        mock_user_employment_repo_get,
        mock_user_employment_controller_request_params,
        mock_user_employment_repo_find_first,
    ):
        """Test update_user_employment when role doesn't exist."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get.return_value = self.mock_user_employment
            mock_user_employment_repo_find_first.return_value = None
            mock_user_employment_controller_request_params.return_value = (
                1,
                1,
                "Institution name",
                "Job title",
                date(year=2018, month=1, day=31),
                date(year=2020, month=1, day=31),
                True,
                [self.skill_one.id, self.skill_two.id],
            )
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.update_user_employment(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "OK"
            assert (
                result.get_json()["payload"]["user_employment"]["skills"][0]["name"]
                == self.skill_one.name
            )

    @patch.object(UserEmploymentRepo, "get")
    def test_delete_user_employment_when_user_employment_is_invalid(
        self, mock_user_employment_repo_get
    ):
        """Test delete_user_employment when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get.return_value = None
            user_employment_controler = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controler.delete_user_employment(1)

            # Assert
            assert result.status_code == 404
            assert (
                result.get_json()["msg"] == "Invalid or incorrect "
                "user_employment_id provided"
            )

    @patch.object(UserEmploymentRepo, "get")
    @patch.object(UserEmploymentRepo, "update")
    def test_delete_user_employment_ok_response(
        self, mock_user_employment_repo_update, mock_user_employment_repo_get
    ):
        """Test delete_user_employment when the role is invalid."""
        # Arrange
        with self.app.app_context():
            mock_user_employment_repo_get.return_value = self.mock_user_employment
            mock_user_employment_repo_update.return_value = self.mock_user_employment
            user_employment_controler = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controler.delete_user_employment(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()["msg"] == "user employment deleted"

    @patch.object(UserEmploymentController, "request_params")
    @patch.object(UserEmploymentRepo, "find_first")
    def test_user_employment_create_with_skills_valid(
        self,
        mock_user_employment_repo_find_first,
        mock_user_employment_controller_request_params,
    ):
        """
        Test create_user_employment with skills OK response.
        """
        # Arrange
        with self.app.app_context():
            mock_user_employment_controller_request_params.return_value = (
                1,
                "Institution name",
                "Job title",
                date(year=2018, month=1, day=31),
                date(year=2020, month=1, day=31),
                False,
                [self.skill_one.id, self.skill_two.id],
            )
            mock_user_employment_repo_find_first.return_value = None
            user_employment_controller = UserEmploymentController(self.request_context)

            # Act
            result = user_employment_controller.create_user_employment()

            # Assert
            assert result.status_code == 201
            assert result.get_json()["msg"] == "OK"

    def test_user_employment_create_with_skills_invalid_skills(self):
        pass
