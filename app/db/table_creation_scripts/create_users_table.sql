CREATE table IF NOT EXISTS users(
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	height INT NOT NULL,
	weight INT NOT NULL,
	age INT NOT null,
	gender text not NULL
);

create table if not exists goals(
	goal_id SERIAL primary key,
	goal text not NULL
);

create table if not exists user_goals(
	user_id INT not null,
	goal_id INT not null,
	value INT not null,
	primary key(user_id,goal_id),
	CONSTRAINT userid_constraint
      FOREIGN KEY(user_id)
	  REFERENCES users(user_id),
	CONSTRAINT goalid_constraint
      FOREIGN KEY(goal_id)
	  REFERENCES goals(goal_id)
);

