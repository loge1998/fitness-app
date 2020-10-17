from app.db.users import get_user_by_username


def get_user_id_by_username(username):
    user = get_user_by_username(username)
    return user['user_id']
