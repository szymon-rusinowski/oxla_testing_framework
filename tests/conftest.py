import pytest
import sh
import time
import psycopg2
import random


@pytest.fixture(scope="session")
def setup_test_containers(request):
    sh.sh(_in="docker-compose --profile test up -d")

    try:
        time.sleep(20)  # Wait for container to up
        yield
    finally:
        sh.sh(_in="docker-compose --profile test down -t0")


def data_generator(entries=100):
    size = [*range(1, entries)]
    func_name = ["'Numeric'", "'String'", "'Boolean'"]
    func_sub = ["'ABS'", "'CEIL'", "'LENGTH'", "'IF'", "'SQRT'"]

    list_of_tuples = [(random.choice(func_sub), random.choice(func_name)) for _ in size]

    result_string = ""
    for tup in list_of_tuples:
        result_string += f"({tup[0]}, {tup[1]}),"
    return result_string[:-1]


@pytest.fixture(scope="session")
def erase_oxla(setup_oxla):
    yield
    cur = setup_oxla
    drop_all = "DELETE from postgres"
    cur.execute(drop_all)


@pytest.fixture(scope="session")
def erase_pg(setup_oxla):
    yield
    cur = setup_pg
    drop_all = "DELETE from postgres"
    cur.execute(drop_all)


@pytest.fixture(scope="session")
def setup_oxla(oxla_client):
    cursor = oxla_client
    cursor.execute("CREATE TABLE oxlafunctions(func_name string,func_sub string);")
    # cursor.execute(
    #     "INSERT INTO oxlafunctions VALUES('Numeric', 'ABS'),('Numeric', 'CEIL'),('String', 'LENGTH'),('Numeric', 'SQRT'),('Boolean', 'IF'),('String', 'STRPOS'),('Numeric', 'FLOOR'),('String', 'CONCAT'),('String', 'LOWER');"
    #    )
    sql_string = "INSERT INTO oxlafunctions VALUES" + data_generator(entries=100) + ";"
    cursor.execute(sql_string)
    yield cursor


@pytest.fixture(scope="session")
def setup_pg(pg_client):
    cursor = pg_client
    cursor.execute(
        "CREATE TABLE oxlafunctions(func_name varchar(255), func_sub varchar(255));"
    )
    #    cursor.execute(
    #        "INSERT INTO oxlafunctions VALUES('Numeric', 'ABS'),('Numeric', 'CEIL'),('String', 'LENGTH'),('Numeric', 'SQRT'),('Boolean', 'IF'),('String', 'STRPOS'),('Numeric', 'FLOOR'),('String', 'CONCAT'),('String', 'LOWER');"
    #   )
    sql_string = "INSERT INTO oxlafunctions VALUES" + data_generator(entries=100) + ";"
    cursor.execute(sql_string)

    yield cursor


@pytest.fixture(scope="session")
def pg_client(setup_test_containers):
    conn_pg = psycopg2.connect(
        database="postgres",
        host="localhost",
        user="postgres",
        port=5430,
    )
    cur_pg = conn_pg.cursor()
    yield cur_pg


@pytest.fixture(scope="session")
def oxla_client(setup_test_containers):
    conn_oxla = psycopg2.connect(
        database="postgres",
        host="localhost",
        user="postgres",
        port=5426,
    )
    conn_oxla.set_session(autocommit=True)
    cur_oxla = conn_oxla.cursor()
    yield cur_oxla
