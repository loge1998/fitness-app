from datetime import datetime

from app.db.helper import get_db_cursor


def add_task(**kwargs):
    title = kwargs.get('title', '')
    due_date = kwargs.get('due_date', str(datetime.now()))
    is_completed = kwargs.get('is_completed', False)

    with get_db_cursor(commit=True) as cursor:
        query = """
            INSERT INTO TASKS(title, due_date, is_completed) VALUES(%s, %s, %s) RETURNING id;
        """
        query = cursor.mogrify(query, [title, due_date, is_completed])
        cursor.execute(query)
        result = cursor.fetchone()
        task_id = result['id']
        cursor.execute(f"SELECT * FROM TASKS WHERE id = '{task_id}'")
        return dict(cursor.fetchone())


def get_task_by_id(task_id):
    with get_db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM TASKS WHERE id = '{task_id}'")
        result = cursor.fetchone()
        return dict(result)
