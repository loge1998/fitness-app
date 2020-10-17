from app.db.tasks import add_task as add_task_db_service, get_task_by_id as get_task_by_id_db_service
from app.services.users import get_user_id_by_username


def add_task(**kwargs):
    username = kwargs['username']
    user_id = get_user_id_by_username(username)
    task = add_task_db_service(**kwargs, user_id=user_id)
    task['task_id'] = task.pop('id')
    task['due_date'] = str(task['due_date']) if task['due_date'] else None
    return task


def get_task_by_id(task_id):
    task = get_task_by_id_db_service(task_id)
    task['task_id'] = task.pop('id')
    task['due_date'] = str(task['due_date']) if task['due_date'] else None
    return task
