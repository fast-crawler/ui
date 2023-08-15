import json

import pytest
from tests.conftest import client


def get_exist_task_name(client):
    response = client.get("/all")
    content = response.json()
    return content[0]["name"]


def get_exist_task(client):
    response = client.get("/all")
    content = response.json()
    return content[0]


def test_all(client):
    response = client.get("/all")
    content = response.json()
    assert response.status_code == 200
    assert len(content) > 0
    assert len(content[0]) == 11
    assert content[0]["name"].startswith("MySpider")


def test_stop_task(client):
    task_name = get_exist_task_name(client)
    task_original = get_exist_task(client)
    response = client.post(f"/stop_task?task_name={task_name}")
    task_stopped = get_exist_task(client)
    content = response.text
    assert response.status_code == 204
    assert content == ""
    assert task_original["name"] == task_stopped["name"]
    assert task_stopped["disabled"] == (not task_original["disabled"])  # == True


def test_start_task(client):
    task_name = get_exist_task_name(client)
    task_original = get_exist_task(client)
    response = client.post(f"/start_task?task_name={task_name}")
    task_started = get_exist_task(client)
    content = response.text
    assert response.status_code == 204
    assert content == ""
    assert task_original["name"] == task_started["name"]
    assert task_started["disabled"] == (not task_original["disabled"])  # == False


def test_toggle_task(client):
    task_name = get_exist_task_name(client)
    task_original = get_exist_task(client)
    response = client.post(f"/toggle_task?task_name={task_name}")
    task_toggled = get_exist_task(client)
    content = response.text
    assert response.status_code == 204
    assert content == ""
    assert task_original["name"] == task_toggled["name"]
    assert task_original["disabled"] == (not task_toggled["disabled"])


def test_update_task(client):
    task_name = get_exist_task_name(client)
    original_task_setting = get_exist_task(client)
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
    task_setting = get_exist_task(client)
    assert task_setting["description"] == data["description"]
