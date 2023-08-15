import json

from fastapi.testclient import TestClient


def get_exist_task_name(client: TestClient):
    response = client.get("/all")
    content = response.json()
    return content[0]["name"]


def get_exist_task(client: TestClient, task_name: str):
    response = client.get("/all")
    content = response.json()
    for task in content:
        if task["name"] == task_name:
            return task
    raise AssertionError("Task is found")


def test_all(client: TestClient):
    response = client.get("/all")
    content = response.json()
    assert response.status_code == 200
    assert len(content) > 0
    assert len(content[0]) == 11
    assert content[0]["name"].startswith("MySpider")


def test_stop_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_stop = get_exist_task(client, task_name)
    response = client.post(f"/stop_task?task_name={task_name}")
    task_after_stopped = get_exist_task(client, task_name)
    assert response.status_code == 204
    assert task_before_stop["name"] == task_after_stopped["name"]
    assert task_after_stopped["disabled"] == (not task_before_stop["disabled"]) is True


def test_start_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_original = get_exist_task(client, task_name)
    response = client.post(f"/start_task?task_name={task_name}")
    task_started = get_exist_task(client, task_name)
    content = response.text
    assert response.status_code == 204
    assert content == ""
    assert task_original["name"] == task_started["name"]
    assert task_started["disabled"] == (not task_original["disabled"]) is False


def test_task_invalid(client: TestClient):
    response = client.post("/start_task?task_name=SHOULD_NOT_FIND")
    assert response.status_code != 200


def test_toggle_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_original = get_exist_task(client, task_name)
    response = client.post(f"/toggle_task?task_name={task_name}")
    task_toggled = get_exist_task(client, task_name)
    content = response.text
    assert response.status_code == 204
    assert content == ""
    assert task_original["name"] == task_toggled["name"]
    assert task_original["disabled"] == (not task_toggled["disabled"])


def test_update_task(client: TestClient):
    task_name = get_exist_task_name(client)
    original_task_setting = get_exist_task(client, task_name)
    data = {
        "description": "sample Description",
    }

    response = client.post(f"/update_task?task_name={task_name}", data=json.dumps(data))
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 11
    for key in original_task_setting.keys():
        if key not in data:
            assert content[key] == original_task_setting[key]

    assert content["description"] == data["description"]
    task_setting = get_exist_task(client, task_name)
    assert task_setting["description"] == data["description"]
