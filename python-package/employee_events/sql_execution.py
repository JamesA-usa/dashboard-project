from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
#### YOUR CODE HERE
db_path = Path("python-package/employee_events/employee_events.db")


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:

    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    #### YOUR CODE HERE

    @staticmethod
    def pandas_query(sql_query):
        # """
        # Method that receives an SQL query as a string
        # and returns the query's result as a panda df.
        # """
        connection = connect(db_path)
        try:
            result = pd.read_sql_query(sql_query, connection)
        finally:
            connection.close()  # Ensure the database connection is closed
        return result

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    #### YOUR CODE HERE

    @staticmethod
    def query(sql_query):
        #"""
        # Returns SQL query as a string
        # and returns the query's result as a list of tuples.
        # """
        connection = connect(db_path)
        try:
            cursor = connection.cursor()
            result = cursor.execute(sql_query).fetchall()
        finally:
            connection.close()
        return result


# Leave this code unchanged
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
