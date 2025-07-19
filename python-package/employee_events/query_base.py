# Import any dependencies needed to execute sql queries
# YOUR CODE HERE
from sqlite3 import connect
from pathlib import Path
import pandas as pd
from .sql_execution import QueryMixin

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

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        # YOUR CODE HERE

        """ 
        Ref (from questions posted in 'Knowledge' forum): 
        `name`: Table name ("employee" or "team")
        `id`: This id is the specific employee or team ID you want to filter the results for.
        """

        query_string = f"""
            select 
                event_date as Day,
                sum(positive_events) as positive_events, 
                sum(negative_events) as negative_events
            from 
                {self.name} inner join employee_events
            on 
                employee_events.{self.name}_id = {self.name}.{self.name}_id
            where
                {self.name}.{self.name}_id = {id}
            group by
                event_date
            order by 
                event_date
            """
        results = super().pandas_query(query_string)
        return results

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    # YOUR CODE HERE
    def notes(self, id):

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        # YOUR CODE HERE
        query_string = f"""
            select 
                {self.name}_id as `{self.name} ID`,
                note_date as `Note date`, 
                note as `Description`
            from
                notes
            where
                {self.name}_id = {id}
            """
        results = super().pandas_query(query_string)
        return results
    