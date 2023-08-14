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
    assert len(content) == 1
    assert len(content[0]) == 11
    assert content[0]["name"].startswith("MySpider")


def test_stop_task(client):
    task_name = get_exist_task_name(client)
    response = client.post(f"/stop_task?task_name={task_name}")
    content = response.text
    assert response.status_code == 204
    assert content == ""


def test_start_task(client):
    task_name = get_exist_task_name(client)
    response = client.post(f"/start_task?task_name={task_name}")
    content = response.text
    assert response.status_code == 204
    assert content == ""


def test_toggle_task(client):
    task_name = get_exist_task_name(client)
    response = client.post(f"/toggle_task?task_name={task_name}")
    content = response.text
    assert response.status_code == 204
    assert content == ""


def test_update_task(client):
    task_name = get_exist_task_name(client)
    data = {
        "description": "sample Description",
    }

    response = client.post(f"/update_task?task_name={task_name}", data=json.dumps(data))
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 11
    assert content["description"] == data["description"]
    task_setting = get_exist_task(client)
    assert task_setting["description"] == data["description"]
