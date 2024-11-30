from locust import HttpUser, task, between
import time

@task
class Fastapi(HttpUser):
    wait_time = between(2, 5)
    host = "https://maize-classification-model.onrender.com"

    @task
    def make_prediction(self):
        self.client.post(url = "/predict")

    @task
    def retrain(self):
        self.client.post(url = "/retrain/upload")