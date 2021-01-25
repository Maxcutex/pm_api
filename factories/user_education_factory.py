import factory
from faker import Faker
from faker.providers import internet, company, job, date_time, lorem, address

from app.models import UserEducation
from app.utils import db
from factories.user_factory import UserFactory

fake = Faker()
fake.add_provider(internet)
fake.add_provider(company)
fake.add_provider(job)
fake.add_provider(date_time)
fake.add_provider(lorem)
fake.add_provider(address)
words = ["Computer Science", "Electrical Engineering", "Machine Learning", "Physcology"]


class UserEducationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserEducation
        sqlalchemy_session = db.session

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    institution_name = fake.company()
    course_name = "Physcology"
    degree_earned = "B.Sc"
    institution_city = fake.city()
    institution_country = fake.country()
    accomplishments = "db.Column(db.Text, nullable=False)"
    start_date = fake.date_between()
    end_date = fake.date_between()
    is_deleted = False


class UserEducationFactoryFake(factory.Factory):
    class Meta:
        model = UserEducation

    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    institution_name = fake.company()
    course_name = "Physcology"
    degree_earned = "B.Sc"
    institution_city = fake.city()
    institution_country = fake.country()
    accomplishments = "db.Column(db.Text, nullable=False)"
    start_date = fake.date_between()
    end_date = fake.date_between()
    is_deleted = False
