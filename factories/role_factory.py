import factory
from app.utils import db
from app.models.role import Role
from faker import Faker
from faker.providers import misc

fake = Faker()
fake.add_provider(misc)


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    is_active = fake.boolean(chance_of_getting_true=75)
    is_deleted = fake.boolean(chance_of_getting_true=0)
    help = "A Help Message"
