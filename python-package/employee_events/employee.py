# Import any dependencies needed to execute sql queries
# YOUR CODE HERE
from sqlite3 import connect
from pathlib import Path
import pandas as pd
from sql_execution import QueryMixin

db_path = Path("python-package/employee_events/employee_events.db").resolve()

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
# YOUR CODE HERE
class QueryBase(QueryMixin):


    # Create a class attribute called `name`
    # set the attribute to an empty string
    # YOUR CODE HERE
    name = ""

    # Define a `names` method that receives
    # no passed arguments
    # YOUR CODE HERE
    def names(self):
        # Return an empty list
        # YOUR CODE HERE
        return []

    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    # YOUR CODE HERE
    def event_counts(self, id):
        # QUERY 3
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        query = f"""
            SELECT event_date, 
                   SUM(positive_events) as total_positive_events,
                   SUM(negative_events) as total_negative_events
            FROM {self.name}
            JOIN employee_events ON {self.name}.{self.name}_id = employee_events.{self.name}_id
            WHERE {self.name}.{self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """
        return self.pandas_query(query)


    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    # YOUR CODE HERE
    def notes(self, id):
        # QUERY 4
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        # YOUR CODE HERE
        query = f"""
            SELECT note_date, note
            FROM notes
            JOIN {self.name} ON notes.{self.name}_id = {self.name}.{self.name}_id
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(query)

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE
    def model_data(self, id):
        query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(query)
