import factory
from app.utils import db
from app.models.skills_category import SkillsCategory
from faker import Faker
from faker.providers import misc


fake = Faker()
fake.add_provider(misc)


class SkillsCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SkillsCategory
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    help = factory.Faker("paragraph")
    is_active = fake.boolean(chance_of_getting_true=75)
    is_deleted = fake.boolean(chance_of_getting_true=0)


class SkillsCategoryFactoryFake(factory.Factory):
    class Meta:
        model = SkillsCategory

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    help = factory.Faker("paragraph")
    is_active = fake.boolean(chance_of_getting_true=75)
    is_deleted = fake.boolean(chance_of_getting_true=0)
