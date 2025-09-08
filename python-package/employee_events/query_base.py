from .sql_execution import QueryMixin


class QueryBase(QueryMixin):

    name = ''

    def names(self):
        return []

    def event_counts(self, id):
        query = f"""SELECT
            event_date,
            SUM(positive_events) AS positive_events,
            SUM(negative_events) AS negative_events
        FROM employee_events
        WHERE {self.name}_id = {id}

        GROUP BY event_date
        ORDER BY event_date;
        """
        return self.pandas_query(query)

    def notes(self, id):
        query = f"""SELECT
            note_date,
            note
            FROM notes
            WHERE {self.name}_id = {id}
            ORDER BY note_date;
            """

        return self.pandas_query(query)
