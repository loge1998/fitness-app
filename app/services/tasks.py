from app.db.tasks import add_task as add_task_db_service, get_task_by_id as get_task_by_id_db_service


def add_task(**kwargs):
    task = add_task_db_service(**kwargs)
    task['task_id'] = task.pop('id')
    task['due_date'] = str(task['due_date']) if task['due_date'] else None
    return task


def get_task_by_id(task_id):
    task = get_task_by_id_db_service(task_id)
    task['task_id'] = task.pop('id')
    task['due_date'] = str(task['due_date']) if task['due_date'] else None
    return task
