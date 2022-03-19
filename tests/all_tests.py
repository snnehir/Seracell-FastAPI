from starlette.testclient import TestClient
from main import app
from utils.db.db import fetch, execute
import asyncio  # test functions are not asynchronous.
from utils.security import get_hashed_password

client = TestClient(app)
loop = asyncio.get_event_loop()


def insert_user(username, password, role):
    query = """ insert into users(username, password, role) values(:username, :password, :role) """
    # in authentication hashed password is compared with hashed password inside db
    hashed_password = get_hashed_password(password)
    values = {"username": username, "password": hashed_password, "role": role}
    # use asyncio to run async functions inside a sync function
    loop.run_until_complete(execute(query, False, values))


def clear_db():
    query = """ delete from users where user_id > 0"""
    loop.run_until_complete(execute(query, False))


def test_token_successful():
    insert_user("user2", "mint", "admin")
    response = client.post("/token", dict(username="user2", password="mint", role="admin"))
    print(response)
    # verify response
    assert response.status_code == 200
    assert "access_token" in response.json()
    clear_db()

