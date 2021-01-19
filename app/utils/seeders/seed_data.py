from datetime import date, datetime

from werkzeug.security import generate_password_hash
from faker import Faker
from faker.providers import internet, company, job, date_time, lorem, address

location_data = [
    {"id": "1", "name": "Lagos", "zone": "+1"},
    {"id": "2", "name": "Nairobi", "zone": "+3"},
    {"id": "3", "name": "Kampala", "zone": "+3"},
    {"id": "4", "name": "Kigali", "zone": "+2"},
]
role_data = [
    {"id": "1", "name": "admin", "is_active": True, "is_deleted": False},
    {"id": "2", "name": "user", "is_active": True, "is_deleted": False},
]

user_data = [
    {
        "id": "1",
        "first_name": "Eno",
        "last_name": "Bassey",
        "email": "eno.bassey@webspoons.com",
        "password": generate_password_hash("demo1"),
        "last_password": "",
        "location_id": 1,
        "image_url": "",
        "gender": "male",
        "date_of_birth": datetime.strptime("1970-04-24", "%Y-%m-%d"),
        "is_active": True,
        "is_deleted": False,
        "profile_summary": "Experienced Solutions Architect with a demonstrated history of working in the "
        "financial services industry. Skilled in Databases, IT Strategy, Mobile Payments, "
        "Software Project Management, and Solution Implementation. A strong business development "
        "professional with a Bachelor of Science (BSc) Computer Science from the University of "
        "Calabar. He is focused on delivering excellence. He is working with and researching"
        " blockchain technologies focusing on Ethereum",
    },
    {
        "id": "2",
        "first_name": "Ayo",
        "last_name": "Ajebeku",
        "email": "ayo.ajebeku@webspoons.com",
        "password": generate_password_hash("demo1"),
        "last_password": "",
        "location_id": 1,
        "image_url": "",
        "gender": "male",
        "date_of_birth": datetime.strptime("1970-04-24", "%Y-%m-%d"),
        "is_active": True,
        "is_deleted": False,
        "profile_summary": "Experienced Solutions Architect with a demonstrated history of working in the "
        "financial services industry. Skilled in Databases, IT Strategy, Mobile Payments, "
        "Software Project Management, and Solution Implementation. A strong business development "
        "professional with a Bachelor of Science (BSc) Computer Science from the University of "
        "Calabar. He is focused on delivering excellence. He is working with and researching"
        " blockchain technologies focusing on Ethereum",
    },
]

user_role_data = [
    {"id": "1", "role_id": "1", "user_id": 1, "is_active": True, "is_deleted": False},
    {"id": "2", "role_id": "1", "user_id": 2, "is_active": True, "is_deleted": False},
]

permission_data = [
    {"id": "1", "name": "view_meal_item", "role_id": "1", "keyword": "view_meal_item"},
    {
        "id": "2",
        "name": "create_meal_item",
        "role_id": "1",
        "keyword": "create_meal_item",
    },
    {
        "id": "3",
        "name": "update_meal_item",
        "role_id": "1",
        "keyword": "update_meal_item",
    },
    {
        "id": "4",
        "name": "delete_meal_item",
        "role_id": "1",
        "keyword": "delete_meal_item",
    },
    {"id": "5", "name": "create_menu", "role_id": "1", "keyword": "create_menu"},
    {"id": "6", "name": "delete_menu", "role_id": "1", "keyword": "delete_menu"},
    {"id": "7", "name": "view_menu", "role_id": "1", "keyword": "view_menu"},
    {"id": "8", "name": "update_menu", "role_id": "1", "keyword": "update_menu"},
    {"id": "9", "name": "view_orders", "role_id": "1", "keyword": "view_orders"},
    {"id": "10", "name": "view_roles", "role_id": "1", "keyword": "view_roles"},
    {"id": "11", "name": "create_roles", "role_id": "1", "keyword": "create_roles"},
    {"id": "12", "name": "delete_roles", "role_id": "1", "keyword": "delete_roles"},
    {
        "id": "13",
        "name": "view_user_roles",
        "role_id": "1",
        "keyword": "view_user_roles",
    },
    {
        "id": "14",
        "name": "create_user_roles",
        "role_id": "1",
        "keyword": "create_user_roles",
    },
    {
        "id": "15",
        "name": "delete_user_roles",
        "role_id": "1",
        "keyword": "delete_user_roles",
    },
    {
        "id": "16",
        "name": "view_permissions",
        "role_id": "1",
        "keyword": "view_permissions",
    },
    {
        "id": "17",
        "name": "create_permissions",
        "role_id": "1",
        "keyword": "create_permissions",
    },
    {
        "id": "18",
        "name": "delete_permissions",
        "role_id": "1",
        "keyword": "delete_permissions",
    },
    {"id": "19", "name": "delete_vendor", "role_id": "1", "keyword": "delete_vendor"},
    {
        "id": "20",
        "name": "delete_engagement",
        "role_id": "1",
        "keyword": "delete_engagement",
    },
    {"id": "21", "name": "view_ratings", "role_id": "1", "keyword": "view_ratings"},
    {"id": "22", "name": "view_users", "role_id": "1", "keyword": "view_users"},
    {"id": "23", "name": "delete_user", "role_id": "1", "keyword": "delete_user"},
    {"id": "24", "name": "create_user", "role_id": "1", "keyword": "create_user"},
    {"id": "25", "name": "update_user", "role_id": "1", "keyword": "update_user"},
    {"id": "26", "name": "view_user_self", "role_id": "2", "keyword": "view_user_self"},
    {
        "id": "27",
        "name": "update_user_self",
        "role_id": "2",
        "keyword": "update_user_self",
    },
    {
        "id": "28",
        "name": "view_skills_categories",
        "role_id": "1",
        "keyword": "view_skills_categories",
    },
    {
        "id": "29",
        "name": "delete_skills_categories",
        "role_id": "1",
        "keyword": "delete_skills_categories",
    },
    {
        "id": "30",
        "name": "create_skills_categories",
        "role_id": "1",
        "keyword": "create_skills_categories",
    },
    {
        "id": "31",
        "name": "update_skills_categories",
        "role_id": "1",
        "keyword": "update_skills_categories",
    },
    {
        "id": "32",
        "name": "view_user_employment_history",
        "role_id": "1",
        "keyword": "view_user_employment_history",
    },
    {
        "id": "33",
        "name": "delete_user_employment_history",
        "role_id": "1",
        "keyword": "delete_user_employment_history",
    },
    {
        "id": "34",
        "name": "create_user_employment_history",
        "role_id": "1",
        "keyword": "create_user_employment_history",
    },
    {
        "id": "35",
        "name": "update_user_employment_history",
        "role_id": "1",
        "keyword": "update_user_employment_history",
    },
]
skill_category_data = [
    {
        "id": "1",
        "name": "Languages",
        "help": "Languages",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "2",
        "name": "Databases",
        "help": "Databases",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "3",
        "name": "OS",
        "help": "Servers",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "4",
        "name": "Version Control",
        "Version Control": "2",
        "is_active": True,
        "is_deleted": False,
    },
    {"id": "5", "name": "Cloud", "Cloud": "2", "is_active": True, "is_deleted": False},
    {
        "id": "6",
        "name": "Project Management",
        "help": "Project Management",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "7",
        "name": "Message",
        "help": "Message",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "8",
        "name": "CI/CD",
        "help": "CI/CD",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "9",
        "name": "Testing",
        "help": "Testing",
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "10",
        "name": "Containers",
        "help": "Containers",
        "is_active": True,
        "is_deleted": False,
    },
]

skill_data = [
    {
        "id": "1",
        "name": "Python",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "2",
        "name": "C#",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "3",
        "name": "Ruby",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "4",
        "name": "Node",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "5",
        "name": "C++",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "6",
        "name": "SQL Server",
        "skill_category_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "7",
        "name": "MySql",
        "skill_category_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "8",
        "name": "Postgres",
        "skill_category_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "9",
        "name": "SQLite",
        "skill_category_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "10",
        "name": "MongoDb",
        "skill_category_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "11",
        "name": "Cassandra",
        "skill_category_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "12",
        "name": "Linux",
        "skill_category_id": 3,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "13",
        "name": "Unix",
        "skill_category_id": 3,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "14",
        "name": "Windows",
        "skill_category_id": 3,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "15",
        "name": "Mac",
        "skill_category_id": 3,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "16",
        "name": "Github",
        "skill_category_id": 4,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "17",
        "name": "BitBucket",
        "skill_category_id": 4,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "18",
        "name": "GitLab",
        "skill_category_id": 4,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "19",
        "name": "SVN",
        "skill_category_id": 4,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "20",
        "name": "AWS",
        "skill_category_id": 5,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "21",
        "name": "Google",
        "skill_category_id": 5,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "22",
        "name": "Heroku",
        "skill_category_id": 5,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "23",
        "name": "Alibaba",
        "skill_category_id": 5,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "24",
        "name": "Jira",
        "skill_category_id": 6,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "25",
        "name": "Trello",
        "skill_category_id": 6,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "26",
        "name": "Kafka",
        "skill_category_id": 7,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "27",
        "name": "RabbitMq",
        "skill_category_id": 7,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "28",
        "name": "Amazon SQS",
        "skill_category_id": 7,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "29",
        "name": "MQ",
        "skill_category_id": 7,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "30",
        "name": "CircleCI",
        "skill_category_id": 8,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "31",
        "name": "TravisCI",
        "skill_category_id": 8,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "32",
        "name": "Jenkins",
        "skill_category_id": 8,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "33",
        "name": "Jest",
        "skill_category_id": 9,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "34",
        "name": "Mocha",
        "skill_category_id": 9,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "35",
        "name": "Docker",
        "skill_category_id": 10,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "36",
        "name": "Kubernetes",
        "skill_category_id": 10,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "37",
        "name": "React",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "38",
        "name": "Vue",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "39",
        "name": "Angular",
        "skill_category_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
]

user_skill_data = [
    {
        "id": "1",
        "user_id": 1,
        "skill_level": "expert",
        "years": 5,
        "skill_id": 1,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "2",
        "user_id": 1,
        "skill_level": "intermediate",
        "years": 5,
        "skill_id": 6,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "3",
        "user_id": 1,
        "skill_level": "beginner",
        "years": 5,
        "skill_id": 12,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "4",
        "user_id": 1,
        "skill_level": "expert",
        "years": 5,
        "skill_id": 16,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "5",
        "user_id": 1,
        "skill_level": "expert",
        "years": 5,
        "skill_id": 24,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "6",
        "user_id": 2,
        "skill_level": "expert",
        "years": 5,
        "skill_id": 36,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "7",
        "user_id": 2,
        "skill_level": "intermediate",
        "years": 5,
        "skill_id": 2,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "8",
        "user_id": 2,
        "skill_level": "expert",
        "years": 5,
        "skill_id": 7,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "9",
        "user_id": 2,
        "skill_level": "intermediate",
        "years": 5,
        "skill_id": 13,
        "is_active": True,
        "is_deleted": False,
    },
    {
        "id": "10",
        "user_id": 2,
        "skill_level": "beginner",
        "years": 5,
        "skill_id": 18,
        "is_active": True,
        "is_deleted": False,
    },
]


# user_employment_data = UserEmploymentFactoryFake.build_batch(10, user_id=1)
# user_employment_data += UserEmploymentFactoryFake.build_batch(10, user_id=2)
user_employment_data = [
    {
        "user_id": 1,
        "institution_name": "fake.company1",
        "employment_type": "full",
        "institution_url": "fake.uri()",
        "institution_city": "fake.city()",
        "institution_country": "fake.country()",
        "institution_size": "11-50 employees",
        "work_summary": "fake.paragraph(nb_sentences=5)",
        "accomplishments": "fake.paragraph(nb_sentences=5)",
        "job_title": "fake.job()",
        "start_date": "2010-12-01",
        "end_date": "2013-11-01",
        "is_current": False,
    },
    {
        "user_id": 1,
        "institution_name": "fake.company2",
        "employment_type": "full",
        "institution_url": "fake.uri()",
        "institution_city": "fake.city()",
        "institution_country": "fake.country()",
        "institution_size": "11-50 employees",
        "work_summary": "fake.paragraph(nb_sentences=5)",
        "accomplishments": "fake.paragraph(nb_sentences=5)",
        "job_title": "fake.job()",
        "start_date": "2013-12-01",
        "end_date": "2017-12-01",
        "is_current": False,
    },
    {
        "user_id": 1,
        "institution_name": "fake.company3",
        "employment_type": "full",
        "institution_url": "fake.uri()",
        "institution_city": "fake.city()",
        "institution_country": "fake.country()",
        "institution_size": "11-50 employees",
        "work_summary": "fake.paragraph(nb_sentences=5)",
        "accomplishments": "fake.paragraph(nb_sentences=5)",
        "job_title": "fake.job()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
    {
        "user_id": 2,
        "institution_name": "fake.company11",
        "employment_type": "full",
        "institution_url": "fake.uri()",
        "institution_city": "fake.city()",
        "institution_country": "fake.country()",
        "institution_size": "11-50 employees",
        "work_summary": "fake.paragraph(nb_sentences=5)",
        "accomplishments": "fake.paragraph(nb_sentences=5)",
        "job_title": "fake.job()",
        "start_date": "2010-12-01",
        "end_date": "2013-11-01",
        "is_current": False,
    },
    {
        "user_id": 2,
        "institution_name": "fake.company22",
        "employment_type": "full",
        "institution_url": "fake.uri()",
        "institution_city": "fake.city()",
        "institution_country": "fake.country()",
        "institution_size": "11-50 employees",
        "work_summary": "fake.paragraph(nb_sentences=5)",
        "accomplishments": "fake.paragraph(nb_sentences=5)",
        "job_title": "fake.job()",
        "start_date": "2013-12-01",
        "end_date": "2017-12-01",
        "is_current": False,
    },
    {
        "user_id": 2,
        "institution_name": "fake.company33",
        "employment_type": "full",
        "institution_url": "fake.uri()",
        "institution_city": "fake.city()",
        "institution_country": "fake.country()",
        "institution_size": "11-50 employees",
        "work_summary": "fake.paragraph(nb_sentences=5)",
        "accomplishments": "fake.paragraph(nb_sentences=5)",
        "job_title": "fake.job()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
]
user_employment_skill_data = [
    {"user_employment_id": 1, "skill_id": 1},
    {"user_employment_id": 1, "skill_id": 6},
    {"user_employment_id": 1, "skill_id": 16},
    {"user_employment_id": 1, "skill_id": 27},
    {"user_employment_id": 2, "skill_id": 2},
    {"user_employment_id": 2, "skill_id": 7},
    {"user_employment_id": 2, "skill_id": 17},
    {"user_employment_id": 2, "skill_id": 28},
    {"user_employment_id": 3, "skill_id": 3},
    {"user_employment_id": 3, "skill_id": 8},
    {"user_employment_id": 3, "skill_id": 18},
    {"user_employment_id": 3, "skill_id": 24},
    {"user_employment_id": 3, "skill_id": 35},
    {"user_employment_id": 4, "skill_id": 3},
    {"user_employment_id": 4, "skill_id": 8},
    {"user_employment_id": 4, "skill_id": 18},
    {"user_employment_id": 4, "skill_id": 24},
    {"user_employment_id": 4, "skill_id": 35},
    {"user_employment_id": 5, "skill_id": 1},
    {"user_employment_id": 5, "skill_id": 6},
    {"user_employment_id": 5, "skill_id": 16},
    {"user_employment_id": 5, "skill_id": 27},
    {"user_employment_id": 6, "skill_id": 2},
    {"user_employment_id": 6, "skill_id": 7},
    {"user_employment_id": 6, "skill_id": 17},
    {"user_employment_id": 6, "skill_id": 28},
]

user_education_data = [
    {
        "institution_name": "University of Calabar",
        "course_name": "Computer Science",
        "degree_earned": "Bsc",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "user_id": 1,
    },
    {
        "institution_name": "University of Lagos",
        "course_name": "Computer Science",
        "degree_earned": "Bsc",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "user_id": 2,
    },
]

user_project_data = [
    {
        "user_id": 1,
        "project_name": "fake.company1",
        "project_description": "full",
        "project_url": "fake.uri()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
    {
        "user_id": 1,
        "project_name": "fake.company2",
        "project_description": "full",
        "project_url": "fake.uri()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
    {
        "user_id": 1,
        "project_name": "fake.company3",
        "project_description": "full",
        "project_url": "fake.uri()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
    {
        "user_id": 2,
        "project_name": "fake.company1",
        "project_description": "full",
        "project_url": "fake.uri()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
    {
        "user_id": 2,
        "project_name": "fake.company2",
        "project_description": "full",
        "project_url": "fake.uri()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
    {
        "user_id": 2,
        "project_name": "fake.company3",
        "project_description": "full",
        "project_url": "fake.uri()",
        "start_date": "2017-12-01",
        "end_date": "2021-06-01",
        "is_current": True,
    },
]

user_project_skill_data = [
    {"user_project_id": 1, "skill_id": 1},
    {"user_project_id": 1, "skill_id": 6},
    {"user_project_id": 1, "skill_id": 16},
    {"user_project_id": 1, "skill_id": 27},
    {"user_project_id": 2, "skill_id": 2},
    {"user_project_id": 2, "skill_id": 7},
    {"user_project_id": 2, "skill_id": 17},
    {"user_project_id": 2, "skill_id": 28},
    {"user_project_id": 3, "skill_id": 3},
    {"user_project_id": 3, "skill_id": 8},
    {"user_project_id": 3, "skill_id": 18},
    {"user_project_id": 3, "skill_id": 24},
    {"user_project_id": 3, "skill_id": 35},
    {"user_project_id": 4, "skill_id": 3},
    {"user_project_id": 4, "skill_id": 8},
    {"user_project_id": 4, "skill_id": 18},
    {"user_project_id": 4, "skill_id": 24},
    {"user_project_id": 4, "skill_id": 35},
    {"user_project_id": 5, "skill_id": 1},
    {"user_project_id": 5, "skill_id": 6},
    {"user_project_id": 5, "skill_id": 16},
    {"user_project_id": 5, "skill_id": 27},
    {"user_project_id": 6, "skill_id": 2},
    {"user_project_id": 6, "skill_id": 7},
    {"user_project_id": 6, "skill_id": 17},
    {"user_project_id": 6, "skill_id": 28},
]
