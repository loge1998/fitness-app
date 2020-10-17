create table IF NOT EXISTS USER_TASKS(
	id serial primary key,
	user_id INT not null,
	task_id INT not null,
	CONSTRAINT userid_in_user_tasks_constraint
      FOREIGN KEY(user_id)
	  REFERENCES users(user_id),
  	CONSTRAINT task_id_in_user_tasks_constraint
      FOREIGN KEY(task_id)
	  REFERENCES tasks(id)
);