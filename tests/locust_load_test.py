from locust import HttpUser, TaskSet, task


class SeracellLocustTasks(TaskSet):
    #@task
    #def token_test(self):
    #    self.client.post("/token", dict(username="user1", password="1234"))

    @task
    def test_post_greenhouse(self):
        sera_dict = {
            "sera_name": "Test Sera",
            "city": "Ankara",
            "zipcode": "06956"
        }
        authorization_header = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwidXNlcl9pZCI6MTAwLCJleHAiOjE2NDk3NDk0MDR9.GsfMFTbWz5IdvcUAOyGNs4yilTX47H7nA6IB2G5ZLII"}
        self.client.post("/v1/sera/", json=sera_dict, headers=authorization_header)


class SeracellLoadTest(HttpUser):
    tasks = [SeracellLocustTasks]
    host = "http://127.0.0.1:8000"
    # use test db instead of real db
