# TODO: Fix the tests -> USE PYTEST

# import unittest
# from unittest.mock import patch

# from fastapi.testclient import TestClient
# from main import app


# class WebSocketEndpointTests(unittest.TestCase):
#     @patch("main.websocket_endpoint")
#     def test_websocket_endpoint(self, websocket_endpoint_mock):
#         # Mock the websocket_endpoint function
#         websocket_endpoint_mock.return_value = None

#         client = TestClient(app)
#         with client.websocket_connect("/ws") as websocket:
#             # Perform necessary assertions or interactions with the websocket
#             pass


# if __name__ == "__main__":
#     unittest.main()
