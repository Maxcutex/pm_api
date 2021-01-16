import factory
from faker import Faker
from faker.providers import internet, company, job, date_time, lorem

from app.models import UserProject, UserProjectSkill
from app.utils import db
from factories.skill_category_factory import SkillFactory
from factories.user_factory import UserFactory

fake = Faker()
fake.add_provider(internet)
fake.add_provider(company)
fake.add_provider(job)
fake.add_provider(date_time)
fake.add_provider(lorem)


class UserProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProject
        sqlalchemy_session = db.session

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    project_name = fake.company()
    project_url = fake.uri()
    project_description = fake.paragraph(nb_sentences=5)
    start_date = fake.date_between()
    end_date = fake.date_between()


class UserProjectFactoryFake(factory.Factory):
    class Meta:
        model = UserProject

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    project_name = fake.company()
    project_url = fake.uri()
    project_description = fake.paragraph(nb_sentences=5)
    start_date = fake.date_between()
    end_date = fake.date_between()
    is_current = False


class UserProjectSkillFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProjectSkill
        sqlalchemy_session = db.session

    user_project = factory.SubFactory(UserProjectFactory)
    user_project_id = factory.SelfAttribute("user_project.id")
    skill = factory.SubFactory(SkillFactory)
    skill_id = factory.SelfAttribute("skill.id")


class UserProjectSkillFactoryFake(factory.Factory):
    class Meta:
        model = UserProjectSkill

    user_project = factory.SubFactory(UserProjectFactory)
    user_project_id = factory.SelfAttribute("user_project.id")
    skill = factory.SubFactory(SkillFactory)
    skill_id = factory.SelfAttribute("skill.id")
