from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).parent.parent / 'python-package/employee_events/employee_events.db'


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # initialization with default db_path (optional)
    def __init__(self, db_path=db_path):
        self.db_path = db_path

    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, query_string):
        
        # open connection
        connection = connect(self.db_path)

        # run query and store data in pandas df
        df = pd.read_sql(query_string, connection)

        # close connection
        connection.close()

        return df



    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, query_string):

         # open connection
        connection = connect(self.db_path)

        # Create a cursor to execute SQL commands
        cursor = connection.cursor()

        # Query data
        cursor.execute(query_string)

        # return data as list of tuples
        return cursor.fetchall()
    

 
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
