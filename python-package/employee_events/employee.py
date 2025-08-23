from query_base import QueryBase
from sql_execution import execute, execute_df
from typing import List, Tuple
from pandas import DataFrame

class Employee(QueryBase):
    """Queries for the `employee` table."""
    name = "employee"

    @property
    def id_field(self) -> str:
        return f"{self.name}_id"

    def names(self) -> List[Tuple[str, int]]:
        """Return [(full_name, employee_id), ...] for all employees."""
        sql = f"""
            SELECT
                first_name || ' ' || last_name AS full_name,
                {self.id_field} AS id
            FROM {self.name}
        """
        return execute(sql)

    def username(self, id: int) -> List[Tuple[str]]:
        """Return [(full_name,)] for the employee with the given id."""
        id = int(id)  # keep f-string usage; ensure numeric
        sql = f"""
            SELECT
                first_name || ' ' || last_name AS full_name
            FROM {self.name}
            WHERE {self.name}.{self.id_field} = {id}
        """
        return execute(sql)

    def model_data(self, id: int) -> DataFrame:
        """Return a DataFrame with summed positive/negative events for an employee."""
        id = int(id)
        sql = f"""
            SELECT
                SUM(positive_events) AS positive_events,
                SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events USING({self.id_field})
            WHERE {self.name}.{self.id_field} = {id}
        """
        return execute_df(sql)
