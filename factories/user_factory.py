import factory
from app.utils import db
from app.models.user import User
from factories.location_factory import LocationFactory
from tests.base_test_case import fake


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    # user_id = factory.Faker("word")
    # user_type = factory.SubFactory(UserRoleFactory)
    email = fake.email()
    password = fake.password()
    last_password = fake.password()
    location = factory.SubFactory(LocationFactory)
    location_id = factory.SelfAttribute("location.id")
    image_url = factory.Faker("url")
    gender = factory.Faker("url")
    date_of_birth = factory.Faker("url")
