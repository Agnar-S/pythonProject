import pandas as pd
import psycopg2
from psycopg2 import OperationalError
import time


def create_connection():
    try:
        conn = psycopg2.connect(
            dbname='smartpackdb',
            user='smartpackuser',
            password='B3Fug!ztZV',
            host='pmk-smartpack-sql.postgres.database.azure.com'
        )
        print("Connection to PostgreSQL DB successful")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None


def execute_query(conn, query):
    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")


def close_connection(conn):
    conn.close()
    print("Connection closed")


def load_query_results_into_dataframe(conn, query):
    return pd.read_sql_query(query, conn)


def main():
    start_time = time.time()
    connection = create_connection()

    if connection is not None:
        query = "SELECT * FROM gjenstander;"
        df = load_query_results_into_dataframe(connection, query)

        # Now you can work with the DataFrame 'df'
        print(df.head())  # For example, print the first few rows

        # Don't forget to close the connection when done
        connection.close()

    end_time = time.time()
    print(end_time - start_time)


main()
