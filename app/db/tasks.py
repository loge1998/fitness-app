from datetime import datetime

from app.db.helper import get_db_cursor


def add_task_for_user(task_id, user_id):
    with get_db_cursor(commit=True) as cursor:
        query = """
            INSERT INTO USER_TASKS(task_id, user_id) VALUES(%s, %s);
        """

        query = cursor.mogrify(query, [task_id, user_id])
        cursor.execute(query)


def add_task(**kwargs):
    title = kwargs.get('title', '')
    due_date = kwargs.get('due_date', str(datetime.now()))
    is_completed = kwargs.get('is_completed', False)
    user_id = kwargs.get('user_id')

    with get_db_cursor(commit=True) as cursor:
        query = """
            INSERT INTO TASKS(title, due_date, is_completed) VALUES(%s, %s, %s) RETURNING id;
        """
        query = cursor.mogrify(query, [title, due_date, is_completed])
        cursor.execute(query)
        result = cursor.fetchone()
        task_id = result['id']
        cursor.execute(f"SELECT * FROM TASKS WHERE id = '{task_id}'")
        result = dict(cursor.fetchone())

    add_task_for_user(task_id, user_id)
    return result


def get_task_by_id(task_id):
    with get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM TASKS WHERE id = '{task_id}'")
        result = cursor.fetchone()
        return dict(result)
