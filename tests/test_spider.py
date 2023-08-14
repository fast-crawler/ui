import os
import sys
import asyncio

import pytest
from tests.conftest import client




def test_all(client):
    response = client.get("/all")
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 1
    assert len(content[0]) == 11
    assert content[0]["name"].startswith("MySpider")
