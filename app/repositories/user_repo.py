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
        first_name, last_name, email, image_url, *extras = args

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            image_url=image_url,
            user_id=kwargs.get("user_id"),
            user_type_id=kwargs.get("user_type").id,
        )
        user.save()
        return user
