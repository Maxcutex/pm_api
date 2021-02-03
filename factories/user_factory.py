import factory
from app.utils import db
from app.models.user import User
from factories.location_factory import LocationFactory
from tests.base_test_case import fake
from faker.providers import date_time, person

fake.add_provider(date_time)
fake.add_provider(person)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = fake.email()
    password = fake.password()
    last_password = fake.password()
    location = factory.SubFactory(LocationFactory)
    location_id = factory.SelfAttribute("location.id")
    image_url = factory.Faker("url")
    gender = "male"
    date_of_birth = fake.date_between()
    employment_date = fake.date_between()
    is_active = True
    is_deleted = False


class UserFactoryFake(factory.Factory):
    class Meta:
        model = User

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = fake.email()
    password = fake.password()
    last_password = fake.password()
    location = factory.SubFactory(LocationFactory)
    location_id = factory.SelfAttribute("location.id")
    image_url = factory.Faker("url")
    gender = "male"
    date_of_birth = fake.date_between()
    employment_date = fake.date_between()
    is_active = True
    is_deleted = False
