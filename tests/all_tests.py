from starlette.testclient import TestClient
from main import app
from utils.db.db import fetch, execute
import asyncio  # test functions are not asynchronous
from utils.security import get_hashed_password
from models.sera import Sera

client = TestClient(app)
loop = asyncio.get_event_loop()


def insert_user(username, password, role):
    query = """ insert into users(username, password, role) values(:username, :password, :role) """
    # in authentication hashed password is compared with hashed password inside db
    hashed_password = get_hashed_password(password)
    values = {"username": username, "password": hashed_password, "role": role}
    # use asyncio to run async functions inside a sync function
    loop.run_until_complete(execute(query, False, values))


def clear_all_db():
    query1 = """ delete from users """
    query2 = """ delete from sera """
    query3 = """ delete from owner """
    loop.run_until_complete(execute(query1, False))
    loop.run_until_complete(execute(query2, False))
    loop.run_until_complete(execute(query3, False))


def check_created_sera(sera_name, city, zipcode):
    query = """ select * from sera where sera_name= :sera_name 
                and city= :city and zipcode= :zipcode """
    values = {"sera_name": sera_name, "city": city, "zipcode": zipcode}
    result = loop.run_until_complete(fetch(query, True, values))
    if result is not None:
        return True
    return False


def get_authorization_header():
    insert_user("test", "test", "admin")
    response = client.post("/token", dict(username="test", password="test", role="admin"))
    # get jwt token to test other endpoints
    jwt_token = response.json()["access_token"]
    header = {"Authorization": f"Bearer {jwt_token}"}
    return header


def test_token_successful():
    insert_user("user2", "mint", "admin")
    response = client.post("/token", dict(username="user2", password="mint", role="admin"))
    print(response)
    # verify response
    assert response.status_code == 200
    assert "access_token" in response.json()
    clear_all_db()


def test_token_unauthorised():
    insert_user("user2", "mint", "admin")
    response = client.post("/token", dict(username="user2", password="mint2", role="admin"))
    print(response)
    # verify response
    assert response.status_code == 401
    clear_all_db()


# Authorization header must be added to all endpoints since we have it as dependency
# test sera insertion
def test_post_greenhouse():
    authorization_header = get_authorization_header()
    sera_dict = {"sera_name": "Sera1", "city": "Ankara", "zipcode": "06300"}
    response = client.post("/v1/sera/", json=sera_dict, headers=authorization_header)
    # print(response.content)
    assert response.status_code == 201
    assert check_created_sera("Sera1", "Ankara", "06300")
    clear_all_db()


def test_post_greenhouse_fail():
    authorization_header = get_authorization_header()
    sera_dict = {"sera_name": "Sera1", "city": "Ankara", "zipcode": "063AA"}
    response = client.post("/v1/sera/", json=sera_dict, headers=authorization_header)
    # print(response.content)
    assert response.status_code != 201
    assert not check_created_sera("Sera1", "Ankara", "063AA")
    clear_all_db()


# test getting current user's sera
def test_get_all_greenhouses():
    authorization_header = get_authorization_header()
    response = client.get("/v1/sera/", headers=authorization_header)
    print(response.content)
    assert response.status_code == 200
