import datetime

import factory
from app.models import UserSkill
from app.utils import db
from faker import Faker
from faker.providers import misc

from factories import SkillFactory, UserFactory

fake = Faker()
fake.add_provider(misc)


class UserSkillFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserSkill
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    skill_level = "intermediate"  # change to a faker of random enum values
    years = 4  # Change to a random number faker
    skill = factory.SubFactory(SkillFactory)
    skill_id = factory.SelfAttribute("skill.id")
    is_deleted = fake.boolean(chance_of_getting_true=0)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")


class UserSkillFactoryFake(factory.Factory):
    class Meta:
        model = UserSkill

    id = factory.Sequence(lambda n: n)
    skill_level = "intermediate"  # change to a faker of random enum values
    years = 4  # Change to a random number faker
    skill = factory.SubFactory(SkillFactory)
    skill_id = factory.SelfAttribute("skill.id")
    is_deleted = fake.boolean(chance_of_getting_true=0)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
