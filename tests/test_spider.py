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


def test_stop_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_stop = get_task_by_name(client, task_name)
    body = {"names": [task_name]}
    response = client.post("/stop_tasks", json=body)
    task_after_stopped = get_task_by_name(client, task_name)
    assert response.status_code == 204
    assert task_before_stop["name"] == task_after_stopped["name"]
    assert task_after_stopped["disabled"] == (not task_before_stop["disabled"]) is True


def test_start_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_start = get_task_by_name(client, task_name)
    body = {"names": [task_name]}
    response = client.post("/start_tasks", json=body)
    task_after_start = get_task_by_name(client, task_name)
    assert response.status_code == 204
    assert task_before_start["name"] == task_after_start["name"]
    assert task_after_start["disabled"] == (not task_before_start["disabled"]) is False


def test_task_invalid(client: TestClient):
    body = {"names": ["SHOULD_NOT_FIND"]}
    response = client.post("/start_tasks", json=body)
    assert response.status_code == 400


def test_toggle_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_toggle = get_task_by_name(client, task_name)
    body = {"name": task_name}
    response = client.post("/toggle_task", json=body)
    task_after_toggle = get_task_by_name(client, task_name)
    assert response.status_code == 204
    assert task_before_toggle["name"] == task_after_toggle["name"]
    assert task_before_toggle["disabled"] == (not task_after_toggle["disabled"])


def test_update_task_invalid_name(client: TestClient):
    task_name = "INVALID_TASK_NAME_SHOULD_NOT_FIND"
    task_setting_for_update = {
        "settings": {"description": "sample Description"},
        "name": task_name,
    }
    response = client.post("/update_task", json=task_setting_for_update)
    task_response_update = response.json()
    assert task_response_update["detail"] == f"Task '{task_name}' not found"
    assert response.status_code == 400


def test_update_task(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_update: dict = get_task_by_name(client, task_name)
    task_setting_for_update = {
        "settings": {"description": "sample Description"},
        "name": task_name,
    }

    response = client.post(
        "/update_task",
        json=task_setting_for_update,
    )
    task_response_update = response.json()
    assert response.status_code == 200
    for key in task_before_update.keys():
        if key not in task_setting_for_update["settings"]:
            assert task_response_update[key] == task_before_update[key]

    assert (
        task_response_update["description"] == task_setting_for_update["settings"]["description"]
    )
    task_after_update = get_task_by_name(client, task_name)
    assert task_after_update["description"] == task_setting_for_update["settings"]["description"]


def test_change_task_schedule(client: TestClient):
    task_name = get_exist_task_name(client)
    task_before_change_schedule = get_task_by_name(client, task_name)
    new_task_schedule = "every 52 minute"

    task_setting_for_update = {"name": task_name, "schedule": new_task_schedule}

    response = client.post(
        "/change_task_schedule",
        json=task_setting_for_update,
    )
    assert response.status_code == 204
    task_after_change_schedule = get_task_by_name(client, task_name)
    assert task_before_change_schedule["start_cond"] != task_after_change_schedule["start_cond"]
    assert task_after_change_schedule["start_cond"] == new_task_schedule
