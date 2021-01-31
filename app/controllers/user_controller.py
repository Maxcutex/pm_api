import datetime

from app.controllers.base_controller import BaseController
from app.repositories import UserRoleRepo, RoleRepo, UserRepo, PermissionRepo
from app.models import Role, User
from app.services.aws_s3_service import AwsS3Service
from app.utils.auth import Auth
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.id_generator import PushID

ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png"])


class UserController(BaseController):
    """
    User Controller.
    """

    def __init__(self, request):
        """
        Constructor.

        Parameters:
        -----------
            request
        """

        BaseController.__init__(self, request)
        self.user_role_repo = UserRoleRepo()
        self.role_repo = RoleRepo()
        self.user_repo = UserRepo()
        self.perm_repo = PermissionRepo()

    def list_admin_users(self, admin_role_id: int = 1) -> list:
        """
        List admin users.

        Parameters:
        -----------
        admin_role_id {int}
            Admin role ID (default: {1}).

        Returns:
        --------
        list
            List of admin users' profiles.
        """

        user_roles = self.user_role_repo.filter_by(
            role_id=admin_role_id, is_active=True
        )

        admin_users_list = []
        for user_role in user_roles.items:
            admin_user_profile = {}
            user = self.user_repo.find_first(id=user_role.user_id)

            if user:
                associated_roles = [
                    user_role.role_id
                    for user_role in self.user_role_repo.filter_by(
                        user_id=user_role.user_id
                    ).items
                ]
                role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
                roles = [
                    {"role_id": role.id, "role_name": role.name}
                    for role in role_objects
                ]
                admin_user_profile["email"] = user.email
                admin_user_profile["name"] = f"{user.first_name} {user.last_name}"
                admin_user_profile["id"] = user.id
                admin_user_profile["roles"] = roles
                admin_user_profile["user_role_id"] = user_role.id

                admin_users_list.append(admin_user_profile)

        return self.handle_response(
            "OK",
            payload={
                "adminUsers": admin_users_list,
                "meta": self.pagination_meta(user_roles),
            },
        )

    def check_email(self, email):

        if self.user_repo.exists(email=email) and email is not None:
            return self.handle_response(
                f"User with email '{email}' already exists",
                status_code=200,
                payload={"useable": False},
            )
        return self.handle_response("Email is Valid!!!", payload={"useable": True})

    def list_all_users(self):

        params = self.get_params_dict()
        page = params.get("page")
        per_page = params.get("per_page")

        users = self.user_repo.paginate(error_out=False, page=page, per_page=per_page)
        user_list = []
        if users.items:
            for user in users.items:
                user_item = user.serialize()
                if user.employment_date is not None:
                    user_item["employment_date"] = user.employment_date.strftime(
                        "%b %d, %Y"
                    )
                user_list.append(user_item)
            for user in user_list:
                associated_roles = [
                    user_role.role_id
                    for user_role in self.user_role_repo.filter_by(
                        user_id=user["id"]
                    ).items
                ]
                role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
                roles = [{"id": role.id, "name": role.name} for role in role_objects]
                user["user_roles"] = roles
                del user["password"]
            return self.handle_response(
                "OK", payload={"users": user_list, "meta": self.pagination_meta(users)}
            )
        return self.handle_response("No users found", status_code=404)

    def delete_user(self, id):
        user = self.user_repo.get(id)
        if user:
            if user.is_deleted:
                return self.handle_response(
                    "User has already been deleted", status_code=400
                )

            updates = {}
            updates["is_deleted"] = True

            self.user_repo.update(user, **updates)

            return self.handle_response("User deleted", payload={"status": "success"})
        return self.handle_response("Invalid or incorrect id provided", status_code=404)

    def create_user(self):
        # push_id = PushID()
        # next_id = push_id.next_id()

        user_info = self.request_params(
            "first_name",
            "last_name",
            "email",
            "role_id",
            "gender",
            "date_of_birth",
            "location_id",
            "password",
        )

        (
            first_name,
            last_name,
            email,
            role_id,
            gender,
            date_of_birth,
            location_id,
            password,
        ) = user_info
        role = self.role_repo.find_first(id=role_id)
        if not role:
            return self.handle_response(
                f"Role with userTypeId(roleId) {role_id} does not exist",
                status_code=400,
            )
        if self.user_repo.exists(email=email) and email is not None:
            return self.handle_response(
                f"User with email '{email}' already exists", status_code=400
            )
        try:
            user = self.user_repo.new_user(*user_info).serialize()
            del user["password"]
            user_role = self.user_role_repo.new_user_role(
                role_id=role_id, user_id=user["id"]
            )

            # get user role and set to user
            user.__setitem__(
                "user_roles",
                [user_role.role.to_dict(only=["id", "name", "help", "timestamps"])],
            )

            return self.handle_response("OK", payload={"user": user}, status_code=201)
        except Exception as e:
            return self.handle_response(
                "User could not be created" + str(e), status_code=404
            )

    def register(self):

        user_info = self.request_params(
            "first_name",
            "last_name",
            "email",
            "role_id",
            "gender",
            "date_of_birth",
            "employment_date",
            "location_id",
            "password",
        )

        (
            first_name,
            last_name,
            email,
            role_id,
            gender,
            date_of_birth,
            employment_date,
            location_id,
            password,
        ) = user_info

        role = self.role_repo.find_first(id=role_id)
        if not role:
            return self.handle_response(
                f"Role with userTypeId(roleId) {role_id} does not exist",
                status_code=400,
            )
        if self.user_repo.exists(email=email) and email is not None:
            return self.handle_response(
                f"User with email '{email}' already exists", status_code=400
            )
        try:
            user = self.user_repo.new_user(*user_info).serialize()
            del user["password"]
            user_role = self.user_role_repo.new_user_role(
                role_id=role_id, user_id=user["id"]
            )

            # get user role and set to user
            user.__setitem__(
                "user_roles",
                [user_role.role.to_dict(only=["id", "name", "help", "timestamps"])],
            )

            return self.handle_response("OK", payload={"user": user}, status_code=201)
        except Exception as e:
            return self.handle_response(
                "User could not be registered" + str(e), status_code=404
            )

    def list_user(self, id):

        user = self.user_repo.find_first(id=id)

        if user:
            user_data = user.serialize()
            del user_data["password"]
            user_roles = self.user_role_repo.get_unpaginated(user_id=id)

            if user_data["employment_date"] is not None:
                user_data["employment_date_formatted"] = user.employment_date.strftime(
                    "%b %d, %Y"
                )
            user_data["user_roles"] = [
                user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
            ]
            return self.handle_response(
                "OK", payload={"user": user_data}, status_code=200
            )

        return self.handle_response("User not found", status_code=404)

    def update_user_summary(self, update_id):
        (profile_summary,) = self.request_params(
            "profile_summary",
        )

        user = self.user_repo.find_first_(id=update_id)
        if not user:
            return self.handle_response(
                msg="FAIL", payload={"user": "User not found"}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL", payload={"user": "User already deleted"}, status_code=400
            )

        updates = {
            "profile_summary": profile_summary,
        }

        user = self.user_repo.update(user, **updates)

        user_data = user.serialize()
        del user_data["password"]
        user_roles = self.user_role_repo.get_unpaginated(user_id=update_id)
        user_data["user_roles"] = [
            user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
        ]

        return self.handle_response("OK", payload={"user": user_data}, status_code=200)

    def update_profile_image(self, update_id):
        (image_url,) = self.request_params(
            "image_url",
        )

        user = self.user_repo.find_first_(id=update_id)
        if not user:
            return self.handle_response(
                msg="FAIL", payload={"user": "User not found"}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL", payload={"user": "User already deleted"}, status_code=400
            )

        updates = {
            "image_url": image_url,
        }

        user = self.user_repo.update(user, **updates)

        user_data = user.serialize()
        del user_data["password"]
        user_roles = self.user_role_repo.get_unpaginated(user_id=update_id)
        user_data["user_roles"] = [
            user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
        ]

        return self.handle_response("OK", payload={"user": user_data}, status_code=200)

    def generate_presigned_url(self, file_name, expiration):
        aws_service = AwsS3Service()
        return aws_service.generate_presigned_post(file_name, expiration)

    def self_update_account_details(self, update_id):
        (
            user_id,
            password,
            location_id,
            date_of_birth,
            gender,
            experience_years,
            personal_email,
            job_title,
            phone,
        ) = self.request_params(
            "user_id",
            "password",
            "location_id",
            "date_of_birth",
            "gender",
            "experience_years",
            "personal_email",
            "job_title",
            "phone",
        )
        user = self.user_repo.find_first_(id=user_id)

        if not user:
            return self.handle_response(
                msg="FAIL", payload={"user": "User not found"}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL", payload={"user": "User already deleted"}, status_code=400
            )
        updates = {
            "password": generate_password_hash(password),
            "location_id": location_id,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "experience_years": experience_years,
            "personal_email": personal_email,
            "job_title": job_title,
            "phone": phone,
        }
        user = self.user_repo.update(user, **updates)
        user_data = user.serialize()
        del user_data["password"]
        user_roles = self.user_role_repo.get_unpaginated(user_id=user_id)
        user_data["user_roles"] = [
            user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
        ]

        return self.handle_response("OK", payload={"user": user_data}, status_code=200)

    def update_user(self, user_id):
        user = self.user_repo.find_first_(id=user_id)

        if not user:
            return self.handle_response(
                msg="FAIL", payload={"user": "User not found"}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL", payload={"user": "User already deleted"}, status_code=400
            )

        user_info = self.request_params_dict(
            "role_id",
            "gender",
            "date_of_birth",
            "employment_date",
            "first_name",
            "last_name",
        )

        if user_info.get("role_id"):
            role_id = user_info["role_id"]
            if not self.role_repo.exists(id=role_id):
                return self.handle_response(
                    f"Role with id {role_id} doesnot exist", status_code=400
                )
            # refactor this to get value of role to be updated

            user_role = self.user_role_repo.find_first(user_id=user_id)
            self.user_role_repo.update(user_role, user_id=user_id, role_id=role_id)

        user = self.user_repo.update(user, **user_info)
        user_data = user.serialize()
        del user_data["password"]
        user_roles = self.user_role_repo.get_unpaginated(user_id=user_id)
        user_data["user_roles"] = [
            user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
        ]

        return self.handle_response("OK", payload={"user": user_data}, status_code=200)

    def update_user_info(self, user_id):
        user = self.user_repo.find_first_(id=user_id)

        if not user:
            return self.handle_response(
                msg="FAIL", payload={"user": "User not found"}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL", payload={"user": "User already deleted"}, status_code=400
            )

        user_info = self.request_params_dict(
            "first_name",
            "last_name",
            "job_title",
            "experience_years",
            "phone",
            "personal_email",
            "git_hub",
            "linked_in",
        )
        import pdb

        pdb.set_trace()
        user = self.user_repo.update(user, **user_info)
        user_data = user.serialize()
        del user_data["password"]
        user_roles = self.user_role_repo.get_unpaginated(user_id=user_id)
        user_data["user_roles"] = [
            user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
        ]

        return self.handle_response("OK", payload={"user": user_data}, status_code=200)

    def authenticate_user(self):
        username, password = self.request_params("username", "password")
        user = self.user_repo.find_first(email=username)

        if user is not None and check_password_hash(user.password, password):
            time_limit = datetime.datetime.utcnow() + datetime.timedelta(days=3)
            user_roles = self.user_role_repo.get_unpaginated(user_id=user.id)
            user_roles_list = [
                user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
            ]
            user_data = {
                "UserInfo": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "name": f"{user.first_name} {user.last_name}",
                    "picture": "",
                    "roles": user_roles_list,
                    "date_time_now": datetime.datetime.utcnow().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "date_time_exp": time_limit.strftime("%Y-%m-%d %H:%M:%S"),
                    "date_time_delta": datetime.timedelta(days=3),
                },
                "iat": datetime.datetime.utcnow(),
                "exp": time_limit,
                "aud": "webspoons.com",
                "iss": "accounts.webspoons.com",
            }
            token = Auth.encode_token(user_data)
            return self.handle_response(
                "OK", payload={"token": token, "user": user.email}, status_code=200
            )

        return self.handle_response(
            "Username/password combination is wrong", status_code=400
        )
