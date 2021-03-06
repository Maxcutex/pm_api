import factory
from app.utils import db
from app.models.user_role import UserRole
from factories.role_factory import RoleFactory
from factories.user_factory import UserFactory

# from factories.location_factory import LocationFactory
from tests.base_test_case import fake
from app.repositories.user_role_repo import UserRoleRepo


class UserRoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserRole
        sqlalchemy_session = db.session

    role = factory.SubFactory(RoleFactory)
    role_id = factory.SelfAttribute("role.id")
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")  # factory.Sequence(lambda n: n)
    # location = factory.SubFactory(LocationFactory)
    # location_id = factory.SelfAttribute("location.id")
    # email = fake.email()
    is_active = True
    is_deleted = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        obj = super()._create(model_class, *args, **kwargs)
        # UserRoleRepo().update_cache(obj)
        return obj


class UserRoleFactoryFake(factory.Factory):
    class Meta:
        model = UserRole

    role = factory.SubFactory(RoleFactory)
    role_id = factory.SelfAttribute("role.id")
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")  # factory.Sequence(lambda n: n)
    is_active = True
    is_deleted = False
