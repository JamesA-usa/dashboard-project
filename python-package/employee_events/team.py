# Import the QueryBase class
# YOUR CODE HERE
from .query_base import QueryBase

# Import dependencies for sql execution
#### YOUR CODE HERE
from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Create a subclass of QueryBase
# called  `Team`
#### YOUR CODE HERE
class Team(QueryBase):

    # Set the class attribute `name`
    # to the string "team"
    #### YOUR CODE HERE
    name = "team"


    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE
    def names(self):
        
        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        #### YOUR CODE HERE
        query_string = f"""
            select 
                {self.name}_name, {self.name}_id
            from
                {self.name}
            """
        
        results = super().query(query_string)
        return results
    

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE
    def username(self, id):

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        #### YOUR CODE HERE
        query_string = f""" 
            select
                {self.name}_name
            from
                {self.name}
            where
                {self.name}.{self.name}_id = {id}
            """
        results = super().query(query_string)
        return results


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE
    def model_data(self, id):

        # return f"""
        #     SELECT positive_events, negative_events FROM (
        #             SELECT employee_id
        #                  , SUM(positive_events) positive_events
        #                  , SUM(negative_events) negative_events
        #             FROM {self.name}
        #             JOIN employee_events
        #                 USING({self.name}_id)
        #             WHERE {self.name}.{self.name}_id = {id}
        #             GROUP BY employee_id
        #            )
        #         """
        query_string = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        
        results = super().pandas_query(query_string)
        return results