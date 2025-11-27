# conftest.py
import pytest
from fastapi.testclient import TestClient
from app import _app
from app.services.db import in_memory_db

@pytest.fixture
def client():
    store = in_memory_db()
    store.clear()
    return TestClient(_app)

@pytest.fixture
def example_subscription():
    return {
        "flowInfo": [
            {
                "flowDescriptions": [
                    "permit in ip from 10.45.0.4 to any",
                    "permit out ip from any to 10.45.0.4"
                ],
                "flowId": 1
            }
        ],
        "notificationDestination": "https://example.com/callback",
        "qosReference": "QOS_L",
        "supportedFeatures": "003C",
        "ueIpv4Addr": "10.45.0.3"
    }
