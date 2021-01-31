import factory
from app.utils import db
from app.models.client import Client

from faker import Faker
from faker.providers import internet, company, job, date_time, lorem, address

fake = Faker()
fake.add_provider(internet)
fake.add_provider(company)
fake.add_provider(job)
fake.add_provider(date_time)
fake.add_provider(lorem)
fake.add_provider(address)


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    institution_name = fake.company()
    institution_url = fake.uri()
    institution_city = fake.city()
    institution_country = fake.country()
    institution_size = "11 - 50 employees"
    status = "Lead"
    start_date = fake.date_between()


class ClientFactoryFake(factory.Factory):
    class Meta:
        model = Client

    institution_name = fake.company()
    institution_url = fake.uri()
    institution_city = fake.city()
    institution_country = fake.country()
    institution_size = "11 - 50 employees"
    status = "Lead"
    start_date = fake.date_between()
