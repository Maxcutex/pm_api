from datetime import datetime

from app.controllers.base_controller import BaseController
from app.repositories import UserRoleRepo, RoleRepo, UserRepo
from app.models import Role, User
from app.utils.auth import Auth
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.id_generator import PushID


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
            andela_user_profile = self.andela_service.get_user_by_email_or_id(
                user_role.user_id
            ) or self.andela_service.get_user_by_email_or_id(user_role.email)

            if andela_user_profile:
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
                admin_user_profile["email"] = andela_user_profile["email"]
                admin_user_profile["name"] = andela_user_profile["name"]
                admin_user_profile["id"] = andela_user_profile["id"]
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

    def list_all_users(self):

        params = self.get_params_dict()
        page = params.get("page")
        per_page = params.get("per_page")

        users = self.user_repo.paginate(error_out=False, page=page, per_page=per_page)
        if users.items:
            user_list = [user.serialize() for user in users.items]
            for user in user_list:
                associated_roles = [
                    user_role.role_id
                    for user_role in self.user_role_repo.filter_by(
                        user_id=user["userId"]
                    ).items
                ]
                role_objects = Role.query.filter(Role.id.in_(associated_roles)).all()
                roles = [{"id": role.id, "name": role.name} for role in role_objects]
                user["userRoles"] = roles
                del user["userTypeId"]
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

        password_hash = generate_password_hash(password)
        if not role:
            return self.handle_response(
                f"Role with userTypeId(roleId) {role_id} does not exist",
                status_code=400,
            )

        if self.user_repo.exists(email=email) and email is not None:
            return self.handle_response(
                f"User with email '{email}' already exists", status_code=400
            )

        user = self.user_repo.new_user(*user_info, password=password_hash).serialize()

        user_role = self.user_role_repo.new_user_role(role_id=role_id, user_id=email)
        # get user role and set to user
        user.__setitem__(
            "user_roles",
            [user_role.role.to_dict(only=["id", "name", "help", "timestamps"])],
        )

        return self.handle_response("OK", payload={"user": user}, status_code=201)

    def list_user(self, email):

        user = self.user_repo.find_first(email=email)

        if user:
            user_data = user.serialize()
            user_roles = self.user_role_repo.filter_all(email=email)
            user_data["user_roles"] = [
                user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
            ]
            return self.handle_response(
                "OK", payload={"user": user_data}, status_code=200
            )

        return self.handle_response("User not found", status_code=404)

    def update_user(self, email):
        user = self.user_repo.get(email=email)

        if not user:
            return self.handle_response(
                msg="FAIL", payload={"user": "User not found"}, status_code=404
            )

        if user.is_deleted:
            return self.handle_response(
                msg="FAIL", payload={"user": "User already deleted"}, status_code=400
            )

        user_info = self.request_params_dict(
            "first_name", "last_name", "email", "roleId"
        )

        if user_info.get("role_id"):
            role_id = user_info["role_id"]
            if not self.role_repo.exists(id=role_id):
                return self.handle_response(
                    f"Role with id {role_id} doesnot exist", status_code=400
                )
            self.user_role_repo.update(user.user_type, role_id=role_id)

        user = self.user_repo.update(user, **user_info)
        user_data = user.serialize()

        user_roles = self.user_role_repo.filter_all(email=email)
        user_data["user_roles"] = [
            user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
        ]

        return self.handle_response("OK", payload={"user": user_data}, status_code=200)

    def authenticate_user(self, user_email, password_entered):
        user = self.user_repo.get(email=user_email)

        if user is not None and check_password_hash(user.password, password_entered):
            time_limit = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            user_roles = self.user_role_repo.filter_all(email=user_email)
            user_roles_list = [
                user_role.role.to_dict(only=["id", "name"]) for user_role in user_roles
            ]
            user_data = {
                "UserInfo": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "name": f"{user.first_name} {user.last_name}",
                    "picture": "",
                    "roles": user_roles_list,
                },
                "iat": datetime.datetime.utcnow(),
                "exp": time_limit,
                "aud": "webspoons.com",
                "iss": "accounts.webspoons.com",
            }
            token = Auth.encode_token(user_data)
            return self.handle_response("OK", payload={"token": token}, status_code=200)

        return self.handle_response(
            "Username/password combination is wrong", status_code=404
        )
