import datetime

from werkzeug.security import generate_password_hash

from app.repositories.base_repo import BaseRepo
from app.models.user import User


class UserRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, User)

    def new_user(self, *args, **kwargs):
        """
        function for creating a new user

        :parameter
            args: a list containing the following positional values
                  [first_name, last_name, email, user_id, photo]

        """
        (
            first_name,
            last_name,
            email,
            role_id,
            gender,
            date_of_birth,
            location_id,
            password,
            *extras,
        ) = args
        print(args)
        phash = generate_password_hash(password)
        print(phash)
        print(password)
        print(date_of_birth)
        print("email ==", email)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            date_of_birth=datetime.datetime.strptime(date_of_birth, "%Y-%m-%d"),
            location_id=location_id,
            password=phash,
        )
        user.save()
        return user
