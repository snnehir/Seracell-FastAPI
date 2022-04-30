# CAUTION: testcontainers==3.5.0 is not working on my machine that's why I'm still using version 3.4.2
import unittest
import asyncio
from app.utils.security import get_hashed_password
from unittest import mock
from databases import Database
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from app.main import app
import nest_asyncio

nest_asyncio.apply()  # RuntimeError: Cannot run the event loop while another loop is running
loop = asyncio.get_event_loop()
client = TestClient(app)
TEST_POSTGRES = None  # Test container


# mock "fetch" function in db.py
async def fetch_test_db(query, is_one=True, values=None):
    db = Database(TEST_POSTGRES.get_connection_url())
    await db.connect()
    if is_one:
        result = await db.fetch_one(query, values=values)
    else:
        result = await db.fetch_all(query, values=values)

    await db.disconnect()
    return result


# mock "execute" function in db.py
async def execute_test_db(query, is_many=False, values=None):
    db = Database(TEST_POSTGRES.get_connection_url())
    await db.connect()
    if is_many:
        result = await db.execute_many(query, values=values)
    else:
        result = await db.execute(query, values=values)
    await db.disconnect()
    return result


class SeraCellTest(unittest.TestCase):
    # work that needs to happen before tests run
    def setUp(self):
        init_test_db()

    # work that needs to happen after tests run
    def tearDown(self):
        stop_and_remove_test_db()

    # redis container does not work in testcontainers==3.4.2
    @mock.patch('app.utils.database.db_functions.fetch', side_effect=fetch_test_db)
    def test_token_successful(self, f):
        insert_user("user2", "mint", "admin")
        response = client.post("/token", dict(username="user2", password="mint", role="admin"))
        # verify response
        print(response.content)
        assert response.status_code == 200
        assert "access_token" in response.json()

    @mock.patch('app.utils.database.db_functions.execute', side_effect=execute_test_db)
    @mock.patch('app.utils.database.db_functions.fetch', side_effect=fetch_test_db)
    def test_post_greenhouse(self, f, f2):
        authorization_header = get_authorization_header()
        sera_dict = {"sera_name": "Sera1", "city": "Ankara", "zipcode": "06300"}
        response = client.post("/v1/sera/", json=sera_dict, headers=authorization_header)
        # print(response.content)
        assert response.status_code == 201
        assert check_created_sera("Sera1", "Ankara", "06300")

    @mock.patch('app.utils.database.db_functions.fetch', side_effect=fetch_test_db)
    def test_get_all_greenhouses(self, f):
        authorization_header = get_authorization_header()
        response = client.get("/v1/sera/", headers=authorization_header)
        assert response.status_code == 200

    @mock.patch('app.utils.database.db_functions.execute', side_effect=execute_test_db)
    @mock.patch('app.utils.database.db_functions.fetch', side_effect=fetch_test_db)
    def test_update_greenhouse(self, f, f2):
        authorization_header = get_authorization_header()
        # Create sera for user
        sera_dict = {"sera_name": "Sera Before", "city": "Ankara", "zipcode": "06300"}
        response = client.post("/v1/sera/", json=sera_dict, headers=authorization_header)
        check_data, sera_id = check_created_sera("Sera Before", "Ankara", "06300")
        assert response.status_code == 201  # Created
        assert check_data  # Check created sera from db

        # Update that sera
        updated_sera_dict = {"sera_name": "Sera Updated", "city": "Düzce", "zipcode": "81650"}
        response2 = client.put(f"/v1/sera/{sera_id}", json=updated_sera_dict, headers=authorization_header)
        check_updated_data = check_created_sera("Sera Updated", "Düzce", "81650")
        assert response2.status_code == 200  # OK
        assert check_updated_data  # Check updated data from db


def init_test_db():
    global TEST_POSTGRES
    # create container with postgres image
    TEST_POSTGRES = PostgresContainer('postgres:latest')
    # https://github.com/testcontainers/testcontainers-python/issues/108#issuecomment-768367971
    TEST_POSTGRES.get_container_host_ip = lambda: "localhost"
    TEST_POSTGRES.start()
    create_tables()


def stop_and_remove_test_db():
    global TEST_POSTGRES
    TEST_POSTGRES.stop()


def create_tables():
    # create database with url and connect
    db = Database(TEST_POSTGRES.get_connection_url())
    loop.run_until_complete(db.connect())
    # create table
    query_users = """create table users (
                            user_id serial PRIMARY KEY, 
                            username text NOT NULL,
                            password text NOT NULL,
                            role text NOT NULL
                        );
                  """
    loop.run_until_complete(db.execute(query_users))
    query_owners = """ create table owner (
                            owner_id serial PRIMARY KEY, 
                            name text NOT NULL,
                            surname text NOT NULL,
                            mail text NOT NULL,
                            phone_number text NOT NULL
                        );
                   """
    loop.run_until_complete(db.execute(query_owners))

    query_sera = """ create table sera (
                            sera_id serial primary key,
                            sera_name text not null,
                            city text not null,
                            zipcode varchar(6),
                            owners integer[]
                        );
                 """
    loop.run_until_complete(db.execute(query_sera))

    loop.run_until_complete(db.disconnect())


# helpers I hope

def insert_user(username, password, role):
    db = Database(TEST_POSTGRES.get_connection_url())
    loop.run_until_complete(db.connect())
    query = """ insert into users(username, password, role) values(:username, :password, :role) """
    hashed_password = get_hashed_password(password)
    values = {"username": username, "password": hashed_password, "role": role}
    loop.run_until_complete(db.execute(query, values=values))
    loop.run_until_complete(db.disconnect())


def check_created_sera(sera_name, city, zipcode):
    db = Database(TEST_POSTGRES.get_connection_url())
    loop.run_until_complete(db.connect())
    query = """ select * from sera where sera_name= :sera_name 
                and city= :city and zipcode= :zipcode """
    values = {"sera_name": sera_name, "city": city, "zipcode": zipcode}
    result = loop.run_until_complete(db.fetch_one(query, values=values))
    loop.run_until_complete(db.disconnect())
    if result is not None:
        return True, result["sera_id"]
    return False


def get_authorization_header():
    insert_user("test", "test", "admin")
    response = client.post("/token", dict(username="test", password="test", role="admin"))
    # get jwt token to test other endpoints
    jwt_token = response.json()["access_token"]
    header = {"Authorization": f"Bearer {jwt_token}"}
    return header
