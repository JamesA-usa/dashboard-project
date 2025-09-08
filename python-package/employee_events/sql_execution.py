from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd


db_path = Path(__file__).parent / 'employee_events.db'


class QueryMixin:
    def pandas_query(self, query):
        connection = connect(db_path)
        df = pd.read_sql_query(query, connection)
        connection.close()
        return df

    def query(self, query):
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query).fetchall()
        connection.close()
        return result


def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result

    return run_query
