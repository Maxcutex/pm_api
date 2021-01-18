import factory
from faker import Faker
from faker.providers import internet, company, job, date_time, lorem, address

from app.models import UserEmployment, UserEmploymentSkill
from app.utils import db
from factories.skill_category_factory import SkillFactory
from factories.user_factory import UserFactory

fake = Faker()
fake.add_provider(internet)
fake.add_provider(company)
fake.add_provider(job)
fake.add_provider(date_time)
fake.add_provider(lorem)
fake.add_provider(address)


class UserEmploymentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserEmployment
        sqlalchemy_session = db.session

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    institution_name = fake.company()
    employment_type = "full"
    institution_url = fake.uri()
    institution_city = fake.city()
    institution_country = fake.country()
    institution_size = "11-50 employees"
    work_summary = fake.paragraph(nb_sentences=5)
    accomplishments = fake.paragraph(nb_sentences=5)
    job_title = fake.job()
    start_date = fake.date_between()
    end_date = fake.date_between()


class UserEmploymentFactoryFake(factory.Factory):
    class Meta:
        model = UserEmployment

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    institution_name = fake.company()
    job_title = fake.job()
    employment_type = "full"
    institution_url = fake.uri()
    institution_city = fake.city()
    institution_country = fake.country()
    institution_size = "11-50 employees"
    work_summary = fake.paragraph(nb_sentences=5)
    accomplishments = fake.paragraph(nb_sentences=5)
    start_date = fake.date_between()
    end_date = fake.date_between()
    is_current = False


class UserEmploymentSkillFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserEmploymentSkill
        sqlalchemy_session = db.session

    user_employment = factory.SubFactory(UserEmploymentFactory)
    user_employment_id = factory.SelfAttribute("user_employment.id")
    skill = factory.SubFactory(SkillFactory)
    skill_id = factory.SelfAttribute("skill.id")


class UserEmploymentSkillFactoryFake(factory.Factory):
    class Meta:
        model = UserEmploymentSkill

    user_employment = factory.SubFactory(UserEmploymentFactory)
    user_employment_id = factory.SelfAttribute("user_employment.id")
    skill = factory.SubFactory(SkillFactory)
    skill_id = factory.SelfAttribute("skill.id")
