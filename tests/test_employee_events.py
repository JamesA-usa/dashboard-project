import pytest
from pathlib import Path

project_root = Path(__file__).parent.parent


@pytest.fixture
def db_path():
    return project_root/'python-package'/'employee_events'/'employee_events.db'


def test_db_exists(db_path):
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn\
        .execute("SELECT name FROM sqlite_master WHERE type='table';")\
        .fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    assert table_names.count('employee') == 1


def test_team_table_exists(table_names):
    assert table_names.count('team') == 1


def test_employee_events_table_exists(table_names):
    assert table_names.count('employee_events') == 1
