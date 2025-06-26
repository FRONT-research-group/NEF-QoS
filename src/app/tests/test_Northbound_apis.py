import pytest
from fastapi.testclient import TestClient
from app import _app
from app.routers.Northbound_apis import in_memory_db
from app.schemas.qos_models import AsSessionWithQosSubscription
from app.services.Southbound_apis_svc import create_app_session_context_to_PCF


# --- Pytest Fixtures ---

# @pytest.fixture
# def client():
#     # Clear the in-memory store before each test run
#     store = in_memory_db()
#     store.clear()
#     return TestClient(_app)


# @pytest.fixture
# def example_subscription():
#     return {
#         "flowInfo": [
#             {
#                 "flowDescriptions": [
#                     "permit in ip from 10.45.0.4 to any",
#                     "permit out ip from any to 10.45.0.4"
#                 ],
#                 "flowId": 1
#             }
#         ],
#         "notificationDestination": "https://example.com/callback",
#         "qosReference": "qod_2",
#         "supportedFeatures": "003C",
#         "ueIpv4Addr": "10.45.0.3"
#     }


# --- Test Cases ---
def test_create_subscription(client, example_subscription):
    resp = client.post(
        "/3gpp-as-session-with-qos/v1/AS1586/subscriptions",
        json=example_subscription
    )
    
    #SEND the request to PCF
    create_app_session_context_to_PCF(AsSessionWithQosSubscription(**example_subscription))

    assert resp.status_code == 201
    data = resp.json()
    assert "subscriptionId" in data
    assert resp.headers["Location"].endswith(data["subscriptionId"])

def test_get_all_subscriptions(client, example_subscription):
    # Create first
    post_resp = client.post(
        "/3gpp-as-session-with-qos/v1/AS1586/subscriptions",
        json=example_subscription
    )
    sub_id = post_resp.json()["subscriptionId"]
    # Now get all
    get_resp = client.get("/3gpp-as-session-with-qos/v1/AS1586/subscriptions")
    assert get_resp.status_code == 200
    all_data = get_resp.json()
    assert any(d["subscriptionId"] == sub_id for d in all_data)


def test_get_subscription_by_id(client, example_subscription):
    post_resp = client.post(
        "/3gpp-as-session-with-qos/v1/AS1586/subscriptions",
        json=example_subscription
    )
    sub_id = post_resp.json()["subscriptionId"]
    get_resp = client.get(f"/3gpp-as-session-with-qos/v1/AS1586/subscriptions/{sub_id}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    for key, value in example_subscription.items():
        assert get_data[key] == value


def test_put_subscription(client, example_subscription):
    post_resp = client.post(
        "/3gpp-as-session-with-qos/v1/AS1586/subscriptions",
        json=example_subscription
    )
    sub_id = post_resp.json()["subscriptionId"]
    put_payload = example_subscription.copy()
    put_payload["supportedFeatures"] = "FFFF"
    put_resp = client.put(
        f"/3gpp-as-session-with-qos/v1/AS1586/subscriptions/{sub_id}",
        json=put_payload
    )
    assert put_resp.status_code == 200
    assert put_resp.json()["supportedFeatures"] == "FFFF"


def test_patch_subscription(client, example_subscription):
    post_resp = client.post(
        "/3gpp-as-session-with-qos/v1/AS1586/subscriptions",
        json=example_subscription
    )
    sub_id = post_resp.json()["subscriptionId"]
    patch_payload = {"qosReference": "qos_4"}
    patch_resp = client.patch(
        f"/3gpp-as-session-with-qos/v1/AS1586/subscriptions/{sub_id}",
        json=patch_payload
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["qosReference"] == "qos_4"


def test_delete_subscription(client, example_subscription):
    post_resp = client.post(
        "/3gpp-as-session-with-qos/v1/AS1586/subscriptions",
        json=example_subscription
    )
    assert post_resp.status_code == 201
    sub_id = post_resp.json()["subscriptionId"]

    del_resp = client.delete(f"/3gpp-as-session-with-qos/v1/AS1586/subscriptions/{sub_id}")
    assert del_resp.status_code == 200

    del_data = del_resp.json()
    # Check for the new response structure
    assert "eventReports" in del_data
    assert isinstance(del_data["eventReports"], list)
    assert del_data["eventReports"][0]["event"] == "SESSION_TERMINATION"


def test_get_subscriptions_missing_id(client):
    """Test the GET subscriptions endpoint with a missing SCS/AS ID"""
    response = client.get("/3gpp-as-session-with-qos/v1/as999/subscriptions")
    assert response.status_code == 404
    data = response.json()
    assert "SCS/AS 'as999' not found" in data.get("detail")
