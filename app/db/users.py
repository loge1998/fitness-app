from app.db.helper import get_db_cursor


def get_user_by_username(username):
    with get_db_cursor() as cursor:
        query = f"""
            SELECT * FROM USERS where username = '{username}';
        """

        result = cursor.execute(query)
        return dict(result)