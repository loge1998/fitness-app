from app.db.user_goals import *
from app.db.helper import get_db_cursor


def create_user(**kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    height = kwargs.get('height')
    weight = kwargs.get('weight')
    age = kwargs.get('age')
    gender = kwargs.get('gender')
    user_details = None
    with get_db_cursor(commit=True) as cursor:
        query = "insert into users (username,password,height,weight,age,gender) values (%s,%s,%s,%s,%s,%s) returning *"
        query = cursor.mogrify(query, [username, password, height, weight, age, gender])
        cursor.execute(query)
        user_details = dict(cursor.fetchone())

    goals = kwargs.get('goals')
    for key in goals.keys():
        add_user_goals(user_details['user_id'], key, goals[key])
    return user_details


def get_user_by_id(user_id):
    with get_db_cursor() as cursor:
        cursor.execute(f"select * from users where user_id = '{user_id}'")
        result = cursor.fetchone()
        return dict(result)


def check_if_username_present(username):
    with get_db_cursor() as cursor:
        cursor.execute(f"select * from users where username = '{username}'")
        result = cursor.fetchone()
        return result is not None


def update_user_by_id(user_id, **kwargs):
    with get_db_cursor(commit=True) as cursor:
        updates = kwargs
        keys = list(updates.keys())
        for key in keys:
            if updates[key] is None:
                updates.pop(key)

        sql_template = "UPDATE users SET ({}) = %s WHERE user_id = {} returning *"
        sql = sql_template.format(', '.join(updates.keys()), user_id)
        params = (tuple(updates.values()),)
        query = cursor.mogrify(sql, params)
        cursor.execute(query, params)
        result = cursor.fetchone()
        return dict(result)


def get_user_by_username(username):
    with get_db_cursor() as cursor:
        query = f"""
                SELECT * FROM USERS where username = '{username}';
            """

        cursor.execute(query)
        result = cursor.fetchone()
        return dict(result)


def get_all_goals_for_username(username):
    with get_db_cursor() as cursor:
        query = f"""
                SELECT
                    G.*,UG.value
                FROM
                    USERS U
                LEFT JOIN user_goals UG ON
                    U.USER_ID = UG.USER_ID
                LEFT JOIN GOALS G ON
                    UG.GOAL_ID = G.GOAL_ID
                WHERE
                U.USERNAME = '{username}';
        """

        cursor.execute(query)

        return [dict(i) for i in cursor.fetchall()]

