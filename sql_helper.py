import mysql.connector as connector
import pandas as pd

from config import *

db_config = {
    'host': DATABASE_HOST,
    'user': DATABASE_USER,
    'password': DATABASE_PW,
    'database': DATABASE
}

def connect_to_db():
    '''
    Connect to database
    '''
    try:
        conn = connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except connector.Error as err:
        print(f'Error: {err}')
        return None
    
def close_connection(conn):
    '''
    Close conn to database
    '''
    if conn.is_connected():
        conn.close()
        print('Connection closed')

def get_all_data_from_table(conn, table_name):
    '''
    Generic function to perform query data
    :param conn: Connection object
    :param query: Generic SQL Select Query
    :param table_name: Table name

    Opens and closes cursor within function using connection parameter
    '''
    query = f'''
        SELECT *
        FROM {table_name}
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())
        result.columns = get_table_columns(conn, table_name)
        # print('Query executed successfully')
        return result
    except connector.Error as err:
        print(f'Error: {err}')
        conn.rollback()
    finally:
        cursor.close()

def get_table_columns(conn, table_name):
    '''
    Returns a list of column names
    '''
    query = f'''
        DESCRIBE {table_name};
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = [row[0] for row in cursor.fetchall()]
        # print(f'Table columns: {result}')
    except connector.Error as err:
        print(f'Error: {err}')
        conn.rollback()
    finally:
        cursor.close()
    return result

def single_insert_into_table(conn, tup, column_names, table_name):
    '''
    Function to add in single row of data
    :param conn: Connection object
    :param tup: Tuple containing information to be inserted
    :param column_names: Tuple containing column names
    :param table_name: Table name
    '''
    query = f'''
        INSERT INTO {table_name} ({column_names})
        VALUES ({tup})
    '''
    try:
        cursor = conn.cursor()
        # Construct the parameterized query
        query = f'''
            INSERT INTO {table_name} ({", ".join(column_names)})
            VALUES ({", ".join(['%s'] * len(tup))})
        '''
        # Execute the query with parameters
        cursor.execute(query, tup)
        conn.commit()
        print('Data inserted successfully')
    except connector.Error as err:
        print(f'Error inserting data: {err}')
        conn.rollback()
    finally:
        cursor.close()
    return 1

def bulk_insert_into_table(conn, data_df, table_name):
    '''
    Generic function to insert data (pandas dataframe) into a table
    :param conn: Connection object
    :param data_df: Pandas dataframe containing data to be inserted
    :param table_name: Table name

    Opens and closes cursor within function using connection parameter
    '''
    columns = ', '.join(data_df.columns)

    #Generate placeholders for the values in the DataFrame 
    #%s, %s, %s ... for dynamic SQL input
    placeholders = ', '.join(['%s'] * len(data_df.columns))

    query = f'''
        INSERT INTO {table_name} ({columns}) 
        VALUES ({placeholders})
    '''

    #Extract values from the DataFrame and insert into the table
    #Create list of values corresponding to placeholders variables
    values = [tuple(row) for row in data_df.values]

    try:
        cursor = conn.cursor()
        for value in values:
            try:
                cursor.execute(query, value)
            except connector.Error as err:
                print(f'Error inserting data: {err}')
        conn.commit()
        print('Data inserted successfully')
    except connector.Error as err:
        print(f'Error: {err}')
        conn.rollback()
    finally:
        cursor.close()
    return 1

def get_all_with_filter(conn: connector, filter_list: list, table_name: str, column_filter: str):
    '''
    Returns all rows under given filter constraints for a single column search else returns an empty dataframe
    Supports query of multiple filters in a list
    
    Parameters:
        - conn: Connector object
        - filter_list: List of values to search for
        - table_name: Name of table
        - column_filter: Name of column to search in
    '''
    filter_query = ', '.join([f"'{filter}'" for filter in filter_list])
    query = f'''
        SELECT *
        FROM {table_name}
        WHERE {column_filter}
        IN ({filter_query});
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())
        if not result.empty:
            col_names = get_table_columns(conn, table_name)
            result.columns = col_names
        else:
            print("No results")
            return result
    except connector.Error as err:
        print(f'Error: {err}')
        conn.rollback()
    finally:
        cursor.close()
    return result