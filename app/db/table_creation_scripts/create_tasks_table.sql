create table TASKS(
	ID serial primary key,
	TITLE varchar(100),
	DUE_DATE date null,
	IS_COMPLETED bool default false );