from datetime import date

from werkzeug.security import generate_password_hash

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
        "date_of_birth": "1970-04-23",
        "is_active": True,
        "is_deleted": False,
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
        "date_of_birth": "1970-04-23",
        "is_active": True,
        "is_deleted": False,
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
