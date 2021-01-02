from app.repositories.base_repo import BaseRepo
from app.models.user_role import UserRole
from app.utils.redisset import RedisSet


class UserRoleRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserRole)
        self.redis_set = RedisSet()

    def new_user_role(self, role_id, user_id):
        user_role = UserRole(
            role_id=role_id, user_id=user_id, is_active=True, is_deleted=False
        )
        user_role.save()
        # self.update_cache(user_role)
        return user_role

    # def update_cache(self, user_role):
    #     """Populate the cache with the user email for autocomplete."""
    #     if user_role.email is not None:
    #         email = user_role.email.strip()
    #         for li in range(1, len(email)):
    #             prefix = email[0:li]
    #             self.redis_set.push(prefix)
    #         self.redis_set.push(email, True)
