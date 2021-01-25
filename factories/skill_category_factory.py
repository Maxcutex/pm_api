import factory
from app.models import Skill
from app.utils import db
from app.models.skill_category import SkillCategory
from faker import Faker
from faker.providers import misc


fake = Faker()
fake.add_provider(misc)


class SkillCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SkillCategory
        sqlalchemy_session = db.session

    name = factory.Faker("name")
    help = factory.Faker("paragraph")
    is_active = fake.boolean(chance_of_getting_true=75)
    is_deleted = fake.boolean(chance_of_getting_true=0)


class CategoryWithSkillsFactory(SkillCategoryFactory):
    @factory.post_generation
    def skills(obj, create, extracted, **kwargs):
        """
        If called like: CategoryWithSkillsFactory(skills=4) it generates a Skill Category with 4
        skills.  If called without `skills` argument, it generates a
        random amount of skills for this category
        """
        if not create:
            # Build, not create related
            return

        if extracted:
            for n in range(extracted):
                SkillFactory(skill_category=obj)
        else:
            import random

            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                SkillFactory(skill_category=obj)


class SkillCategoryFactoryFake(factory.Factory):
    class Meta:
        model = SkillCategory

    name = factory.Faker("name")
    help = factory.Faker("paragraph")
    is_active = fake.boolean(chance_of_getting_true=75)
    is_deleted = fake.boolean(chance_of_getting_true=0)


class SkillFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Skill
        sqlalchemy_session = db.session

    name = fake.job()
    skill_category = factory.SubFactory(SkillCategoryFactory)
    skill_category_id = factory.SelfAttribute("skill_category.id")
    is_active = True
    is_deleted = False


class SkillFactoryFake(factory.Factory):
    class Meta:
        model = Skill

    name = fake.job()
    skill_category = factory.SubFactory(SkillCategoryFactory)
    skill_category_id = factory.SelfAttribute("skill_category.id")
    is_active = True
    is_deleted = False
