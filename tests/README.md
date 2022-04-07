# Testing 
I had tested the API with 3 ways for learning purposes:  
  - Testing with test database end redis ```test_endpoints.py```
  - Testing with using [testcontainers](https://github.com/testcontainers/testcontainers-python) ```unit_tests_testcontainers.py```
  - Load testing with [Locust](http://docs.locust.io/en/stable/) ```locust_load_test.py```  

## 1- Testing endpoints with test database and redis 🐳
For testing endpoints, we don't want to use our actual database and redis. So before testing we need to create 2 containers:  
  - test-db:  
    ``` 
    docker run --name test-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5432:5432 -d postgres 
    ```
  - test-redis:  
    ``` 
    docker run --name test-redis -p 6379:6379 -d redis 
    ```  
After creation of these conatiners, we can run each test with clicking green run icons in PyCharm:  

  ![image](https://user-images.githubusercontent.com/57798386/162152775-1cb7b3a5-d999-4486-992e-8058b709b5d1.png)

## 2- Testing with testcontainers 🧊
In testcontainers, testing logic is smilar to the first way with one difference: we don't need to create and run containers manually anymore!  
With testcontainers we can use docker containers for functional and integration testing.  

In setUp function, a PostgreSQL database instance using PostgresContainer is created and necessary tables are created here. Before each test, setUp function is run and for each test we will have a new test database to work with.  

After each test is finished the container is stopped and removed (tearDown).

For running each test, we can use green run icons like in the first way.

## 3- Load testing with Locust
With Locust we can test our API with custom number of users and requests to observe how our system responses in different situtations. 
(Before running the test file we need to start the API with uvicorn command)  

To run ```locust_load_test.py```:

  ```
  locust -f ./tests/locust_load_test.py
  ``` 
Go to Locust's web interface from console:  

![locust-interface](https://user-images.githubusercontent.com/57798386/162164681-2e6d3a88-d914-44f5-86ac-f6adc820628f.png)

Enter number of users and spawn rate yo want to test and start swarming:

![locust-statistics](https://user-images.githubusercontent.com/57798386/162162720-d63b0497-91d3-4bb9-bb1c-78bd30d042dd.png)


