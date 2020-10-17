from app.core.postgres_utils import *
from app.core.config import config

def insert_user_to_db(user):
    conn = connect_postgres(
            dbname=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USERNAME,
            password=config.DB_PASSWORD
    )
    insert_query = "insert into users (username,password,height,weight,age,gender) values ('{}','{}',{},{},{},'{}')"
    insert_query.format(user.username,user.password,user.height,user.weight,user.age,user.gender)
    return_row_after_insert(conn, insert_query)


def get_user_by_username(conn, username):
    select_query = "select user_id from users where username = '{}'"
    select_query.format(username)



def update_user(user):




