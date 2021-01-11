import factory
from faker import Faker
from faker.providers import internet, company, job, date_time

from app.models import UserEmployment
from app.utils import db
from factories.user_factory import UserFactory

fake = Faker()
fake.add_provider(internet)
fake.add_provider(company)
fake.add_provider(job)
fake.add_provider(date_time)


class UserEmploymentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserEmployment
        sqlalchemy_session = db.session

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    institution_name = fake.company()
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
    start_date = fake.date_between()
    end_date = fake.date_between()
    is_current = False
