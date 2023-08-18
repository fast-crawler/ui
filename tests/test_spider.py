import json

from fastapi.testclient import TestClient


def get_exist_task_name(client: TestClient):
    response = client.get("/all")
    content = response.json()
    return content[0]["name"]


def get_task_by_name(client: TestClient, task_name: str):
    response = client.get("/all")
    content = response.json()
    for task in content:
        if task["name"] == task_name:
            return task
    raise AssertionError("The task not found")


def test_all(client: TestClient):
    response = client.get("/all")
    content = response.json()
    assert response.status_code == 200
    assert len(content) > 0
    assert len(content[0]) == 11
    assert content[0]["name"].startswith("MockSpider")


def test_stop_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_stop = get_task_by_name(client, task_name)
    response = client.post(f"/stop_task?task_name={task_name}")
    task_after_stopped = get_task_by_name(client, task_name)
    assert response.status_code == 204
    assert task_before_stop["name"] == task_after_stopped["name"]
    assert task_after_stopped["disabled"] == (not task_before_stop["disabled"]) is True


def test_start_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_start = get_task_by_name(client, task_name)
    response = client.post(f"/start_task?task_name={task_name}")
    task_after_start = get_task_by_name(client, task_name)
    assert response.status_code == 204
    assert task_before_start["name"] == task_after_start["name"]
    assert task_after_start["disabled"] == (not task_before_start["disabled"]) is False


def test_task_invalid(client: TestClient):
    response = client.post("/start_task?task_name=SHOULD_NOT_FIND")
    assert response.status_code == 400
    response = client.post("/stop_task?task_name=SHOULD_NOT_FIND")
    assert response.status_code == 400
    response = client.post(f"/toggle_task?task_name=SHOULD_NOT_FIND")
    assert response.status_code == 400


def test_toggle_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_toggle = get_task_by_name(client, task_name)
    response = client.post(f"/toggle_task?task_name={task_name}")
    task_after_toggle = get_task_by_name(client, task_name)
    assert response.status_code == 204
    assert task_before_toggle["name"] == task_after_toggle["name"]
    assert task_before_toggle["disabled"] == (not task_after_toggle["disabled"])


def test_update_task_invalid_name(client: TestClient):
    task_name = "INVALID_TASK_NAME_SHOULD_NOT_FIND"
    task_setting_for_update = {
        "description": "sample Description",
    }

    response = client.post(
        f"/update_task?task_name={task_name}", data=json.dumps(task_setting_for_update)  # type: ignore
    )
    task_response_update = response.json()
    assert task_response_update["detail"] == f"Task '{task_name}' not found"
    assert response.status_code == 400


def test_update_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_update = get_task_by_name(client, task_name)
    task_setting_for_update = {
        "description": "sample Description",
    }

    response = client.post(
        f"/update_task?task_name={task_name}", data=json.dumps(task_setting_for_update)  # type: ignore
    )
    task_response_update = response.json()
    assert response.status_code == 200
    assert len(task_response_update) == 11
    for key in task_before_update.keys():
        if key not in task_setting_for_update:
            assert task_response_update[key] == task_before_update[key]

    assert task_response_update["description"] == task_setting_for_update["description"]
    task_after_update = get_task_by_name(client, task_name)
    assert task_after_update["description"] == task_setting_for_update["description"]


def test_change_task_schedule(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_change_schedule = get_task_by_name(client, task_name)
    new_task_schedule = "every 52 minute"

    response = client.post(
        f"/change_task_schedule?task_name={task_name}&task_schedule={new_task_schedule}",
    )
    assert response.status_code == 200

    task_after_change_schedule = response.json()
    assert task_before_change_schedule["start_cond"] != task_after_change_schedule["start_cond"]
    assert task_after_change_schedule["start_cond"] == new_task_schedule
