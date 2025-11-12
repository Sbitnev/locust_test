import json
import os
from locust import HttpUser, task, between

# Загружаем конфигурацию
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)


class ApiUser(HttpUser):
    """
    Тестовый пользователь Locust: выполняет запросы к API.
    Адрес host задается автоматически из config.json.
    """

    wait_time = between(1, 3)
    host = CONFIG["base_url"]

    @task
    def test_endpoints(self):
        headers = CONFIG.get("headers", {})
        for ep in CONFIG["endpoints"]:
            method = ep["method"].upper()
            path = ep["path"]
            name = ep["name"]

            if method == "GET":
                self.client.get(
                    path, params=ep.get("params", {}), headers=headers, name=name
                )
            elif method == "POST":
                self.client.post(
                    path, json=ep.get("data", {}), headers=headers, name=name
                )
