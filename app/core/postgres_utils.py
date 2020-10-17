import sys
import json

# see http://initd.org/psycopg/docs/usage.html
import psycopg2
# from psycopg2.extras import RealDictCursor
# see https://stackoverflow.com/questions/10252247/how-do-i-get-a-list-of-column-names-from-a-psycopg2-cursor
#  about half way down
import psycopg2.extras

# see https://stackoverflow.com/questions/50174683/how-to-load-data-into-pandas-from-a-large-database
#   even though I am not worried about the large aspect for now
import pandas as pd
# see pandas 1.0.3 api reference guid:
#   https://pandas.pydata.org/pandas-docs/stable/reference/index.html
#   older pandas: see https://pandas.pydata.org/pandas-docs/version/0.13/api.html, search for sql
import pandas.io.sql as psql

# see https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_introduction.htm
# from sqlalchemy import create_engine

import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

#############################################
#
#
#
#############################################


def connect_postgres(dbname, user, password, host, port):
    try:
        print('\nAttempting to connect to a postgres database using psycopq2')
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        print('Successfully connected to the postgres database, and created a cursor for it')
        db = {'conn': conn, 'cursor': cursor}
        # see https://www.psycopg.org/docs/extras.html
        db['cursor_json'] = db['conn'].cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # use the next one if you want records without the columns names
        # db['cursor_json'] = db['conn'].cursor(cursor_factory=psycopg2.extras.DictCursor)
        return db
    except Exception as e:
        print ("\nI am unable to connect to the database")
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

        print('\nExiting program because failed to connect to opus database\n')
        sys.exit()

def create_schema(db, schema_name):
    print('\nEntering create_schema function, with schema name ' + schema_name)
    q = "CREATE SCHEMA IF NOT EXISTS " + schema_name
    try:
        db['cursor'].execute(q)
        db['conn'].commit()
        print('\nExecuted the CREATE SCHEMA IF NOT EXISTS command, and committed')
    except Exception as e:
        print ("\nUnable to execute the CREATE SCHEMA IF NOT EXISTS command")
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)



def set_search_path(db, path):
    try:
        db['cursor'].execute("set search_path to " + path)
        db['conn'].commit()
        print('\nSet search_path to "' + path + '" and committed')
    except Exception as e:
        print ("\nUnable to set search_path to '" + path + "', perhaps because that doesn't exist as a schema")
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)


def execute_db_update(db, update):
    try:
        db['cursor'].execute(update)
        db['conn'].commit()
        print('\nSuccessfully executed the db update and committed')
    except Exception as e:
        print ("\nUnable to execute the db update")
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)


def execute_db_query(db, query):
    try:
        db['cursor'].execute(query)
        db['conn'].commit()
    except Exception as e:
        print ("\nUnable to execute the given query")
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

def delete_all_from_table(db, table):
    q = '''
           DELETE
           FROM table
        '''
    q = q.replace('table', table)
    execute_db_update(db, q)


'''
def add_indexes_to_mimiciii_tables(db):
    print('\nEntered add_indexes_to_mimiciii_tables')
    q = {}
    q['chartevents__itemid'] = """ 
           create index chartevents__itemid
           on chartevents(itemid)
         """
    q['chartevents__hadm_id'] = """ 
           create index chartevents__hadm_id
           on chartevents(hadm_id)
         """
    q['chartevents__subject_id'] = """ 
           create index chartevents__subject_id
           on chartevents(subject_id)
         """
    q['inputevents_mv__subj_item_starttime'] = """
           create index inputevents_mv__subj_item_starttime 
           on inputevents_mv(subject_id, itemid, starttime)
         """
    q['labevents__subject_id'] = """ 
           create index labevents__subject_id
           on labevents(subject_id)
         """
    q['d_items__category'] = """ 
           create index d_items__category
           on d_items(category)
         """
    for key in q:
        try:
            db['cursor'].execute(q[key])
            db['conn'].commit()
            print('  Successfully created index ' + key)
        except: #Exception as e:
            db['conn'].rollback()
            print('  Failed to create index ' + key + ', probably because it already exists')
            """
            # to use this part, also adjust the "except" line 3 lines above
            print('  The exception error message is as follows:')
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            """

    print('Added indexes for mimiciii tables (if needed), including a commit')
'''


def close_postgres(db):
    try:
        db['cursor'].close()
        db['conn'].close()
        print('\nHave closed the cursor and connection to the database')
    except:
        print('\nInput to the close_postgres function call is not holding a postgres connection and cursor')



# following about the third comment down in
# https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table
# Assumes that:
#     table_name has been defined (and typically, is empty)
#     table_name column names are same as df (but I think can be in different order)
#     table_name column data types match with df column data types
#     if table_name does not include a schema name, then already a "set search_path to ...' has been invoked
#     db is a structure with 'conn' and 'cursor', created using connect_postgres() above
def load_df_into_table_with_same_columns(df, db, table_name):
    print('\nEntering routine will load a dataframe into the postgres table ' + table_name)
    if len(df) > 0:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        #create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table_name,columns,values)

        try:
            psycopg2.extras.execute_batch(db['cursor'], insert_stmt, df.values)
            db['conn'].commit()
            print('Succeeded with the insertion of dataframe records into postgres table')
        except Exception as e:  # if you don't want the exception comment, then drop "Exception as e"
            db['conn'].rollback()
            print('  Failed to load dataframe into the table with name "' + table_name + '"')
            print('  The exception error message is as follows:')
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

        return


def import_query_into_df(query, db):
    try:
        df = pd.read_sql_query(query, db['conn'])
        print('Succeeded in pulling query output into a dataframe')
        return df
    except Exception as e:  # if you don't want the exception comment, then drop "Exception as e"
        db['conn'].rollback()
        print('  Failed to pull query output into a dataframe')
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        return


def export_table_to_csv(table, db, dirName, timestamp):
    print('\nEntering function to exoirt table "' + table + '" to csv file')
    q = "select * from " + table

    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(q)
    # timestamp = datetime.now().strftime('%Y-%m-%d--%H-%M')
    # dirName = OPUS_DATA_OUTPUTS_DIR
    fileName = timestamp + '_' + table + '.csv'

    with open(dirName + fileName, 'w') as f:
        db['cursor'].copy_expert(outputquery, f)
    f.close()
    print('   Wrote csv file ' + dirName + fileName )
    # util_general.print_current_time()


def export_query_to_csv(db, q, timestamp, dirName, filenameroot):
    print('\nEntering function to write output of a query into csv file')

    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(q)
    # timestamp = datetime.now().strftime('%Y-%m-%d--%H-%M')
    # dirName = OPUS_DATA_OUTPUTS_DIR
    fileName = timestamp + '__' + filenameroot + '.csv'

    try:
        with open(dirName + fileName, 'w') as f:
            db['cursor'].copy_expert(outputquery, f)
        f.close()
        print('\nSuccessfully ran query and wrote output into csv file: \n' + dirName + fileName )
        # util_general.print_current_time()
    except Exception as e:
        print ("\nException in function export_query_to_csv ")

        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

        print("\nNow closing the database connection")
        close_postgres(db)





def export_query_to_json(db, q):
    try:
        db['cursor_json'].execute(q)
        # the "default=str" takes care of date objects from Postgres, and maps them to string
        #    so that JSON can serialize it
        return json.dumps(db['cursor_json'].fetchall(), indent=2, default=str)
    except Exception as e:
        print ("\nException in function export_query_to_json ")

        err_msg = ''
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
            err_msg = err_msg + str(e.message)
        else:
            print(e)
            err_msg = err_msg + str(e)
        print('\nerr_msg is: ' + err_msg)

        print("\nNow closing the database connection")
        close_postgres(db)
        return {"ERROR" : "Failed to write query into json, with exception message: '" \
                          + err_msg + "'"}


        # print('\nExiting program because failed to connect to opus database\n')
        # sys.exit()


# illustration of using sqlalchemy
def testdb(db_eng):
    print('\nEntered the function testdb')
    q1 = "set search_path to opus"
    q2 = "CREATE TABLE IF NOT EXISTS films  (title text, director text, year text)"
    q3 = """
           INSERT INTO opus.films (title, director, year)
           VALUES ('Doctor Strange', 'Scott Derrickson', '2016')
	 """
    with db_eng.connect() as conn:
        conn.execute(q1)
        conn.execute(q2)
        conn.execute(q3)


def return_row_after_insert(db, query):
    row = {}
    try:
        db['cursor'].execute(query)
        row = db['cursor'].fetchone()
        db['conn'].commit()
        print('Succeeded with the insertion of dataframe records into postgres table')
    except Exception as e:  # if you don't want the exception comment, then drop "Exception as e"
        db['conn'].rollback()
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    return row


def execute_db_bulk_update(db, query, rows):
    try:
        psycopg2.extras.execute_batch(db['cursor'], query, rows)
        db['conn'].commit()
        print('\nSuccessfully executed the db update and committed')
    except Exception as e:
        print ("\nUnable to execute the db update")
        print('  The exception error message is as follows:')
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
