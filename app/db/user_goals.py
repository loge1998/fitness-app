from app.db.helper import get_db_cursor


def add_goals(goal):
    with get_db_cursor(commit=True) as cursor:
        query = """
           insert into goals (goal) values(%s) RETURNING *;
        """
        query = cursor.mogrify(query, [goal])
        cursor.execute(query)
        return dict(cursor.fetchone())


def get_all_goals():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM goals")
        return [dict(i) for i in cursor.fetchall()]


def add_user_goals(user_id, goal_id, value):
    with get_db_cursor(commit=True) as cursor:
        query = """
          insert into user_goals (user_id, goal_id, value) values(%s, %s, %s)
        """
        query = cursor.mogrify(query, [user_id, goal_id, value])
        cursor.execute(query)





