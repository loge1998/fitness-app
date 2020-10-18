from app.db.users import get_user_by_username
from app.db.users import create_user as create_user_db_service, \
    check_if_username_present as db_check_if_username_present, get_user_by_id as db_get_user_id, \
    update_user_by_id as db_update_user_by_id, get_user_by_username as db_get_user_by_username,\
    get_all_goals_for_username

def get_user_id_by_username(username):
    user = get_user_by_username(username)
    return user['user_id']


def check_if_username_present(username):
    return db_check_if_username_present(username)


def signup_user(**kwargs):
    return create_user_db_service(**kwargs)


def update_user_details(user_id, **kwargs):
    return db_update_user_by_id(user_id, **kwargs)


def get_user_by_id(user_id):
    return db_get_user_id(user_id)


def get_user_by_username(username):
    return db_get_user_by_username(username)


def get_all_goals_of_user(username):
    return get_all_goals_for_username(username)

