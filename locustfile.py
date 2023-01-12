from locust import HttpUser, task, between
import random
import json
from pydantic import BaseModel

class APIUser(HttpUser):
    # Setting the host name and wait_time
    host = 'http://localhost:8000'
    wait_time = between(3, 5)
    @task()
    def click(self):
        x = round(random.uniform(0, 1), 4)
        y = round(random.uniform(0, 1), 4)
        self.client.post("/add_point", json={"x": x, "y" : y})