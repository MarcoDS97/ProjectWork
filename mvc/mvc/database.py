# database.py

import mysql.connector
import config as conf

db_config = {
    'host': conf.DB_HOST,
    'user': conf.DB_USER,
    'password': conf.DB_PASSWORD,
    'database': conf.DB_NAME
}


def create_db_connection():
    return mysql.connector.connect(**db_config)


def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def execute_query2(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
        connection.commit()
    else:
        cursor.execute(query)
    cursor.close()
    connection.close()
