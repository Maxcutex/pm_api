import factory
from app.utils import db
from app.models import Skill
from faker import Faker


class SkillFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Skill
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("city")
    skill_category_id = factory.Sequence(lambda n: n)

