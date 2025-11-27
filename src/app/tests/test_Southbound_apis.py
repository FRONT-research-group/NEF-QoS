import pytest
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from app.services.Southbound_apis_svc import (
    create_app_session_context_to_PCF,
    get_app_session_id,  # to verify mapping
)
from app.services.db import SUBSCRIPTION_STORE, map_subId_with_appsessionId  
from app.schemas.qos_models import AsSessionWithQosSubscriptionWithSubscriptionId, AsSessionWithQosSubscription
from unittest.mock import patch

from app.services.db import (
    SUBSCRIPTION_STORE,
    SUBSCRIPTION_ID_TO_APP_SESSION_ID,
    map_subId_with_appsessionId,
)
from app.services.Southbound_apis_svc import delete_app_session_context_from_PCF
from app.schemas.qos_models import AsSessionWithQosSubscriptionWithSubscriptionId




@pytest.mark.asyncio
async def test_create_app_session_context_PCF(example_subscription):
    subscription_id = str(uuid4())
    scs_as_id = "AS1586"
    subscription_with_id = AsSessionWithQosSubscriptionWithSubscriptionId(
        subscriptionId=subscription_id,
        **example_subscription
    )

    SUBSCRIPTION_STORE[scs_as_id] = [subscription_with_id]

    subscription_model = AsSessionWithQosSubscription(**example_subscription)

    fake_session_id = "fake-session-id-123"

    #  Patch the pcf_post_request to return the fake session ID and status code
    with patch("app.services.Southbound_apis_svc.pcf_post_request") as mock_post:
        mock_post.return_value = (fake_session_id, 201)

        await create_app_session_context_to_PCF(subscription_model, scs_as_id, subscription_id)

        assert mock_post.called is True
        payload = mock_post.call_args[0][0]
        assert "ascReqData" in payload

        req_data = payload["ascReqData"]
        assert req_data["notifUri"] == "https://example.com/callback"
        assert req_data["medComponents"]["1"]["medType"] == "AUDIO"
        assert req_data["medComponents"]["1"]["medSubComps"]["1"]["fDescs"] == [
            "permit in ip from 10.45.0.4 to any",
            "permit out ip from any to 10.45.0.4"
        ]

    mapped_session_id = get_app_session_id(subscription_id)
    assert mapped_session_id == fake_session_id
    





@patch("app.services.Southbound_apis_svc.pcf_delete_request")
def test_delete_app_session_context_PCF(mock_pcf_delete, example_subscription):
    """

    Test that delete_app_session_context_from_PCF:
    - Gets correct session ID
    - Deletes mapping
    - Calls pcf_delete_request with the correct session ID
    """


    subscription_id = str(uuid4())
    test_subscription = AsSessionWithQosSubscriptionWithSubscriptionId(
        subscriptionId=subscription_id,
        **example_subscription
    )

    SUBSCRIPTION_STORE['test'] = [test_subscription]

    # Map subscriptionId to appSessionId
    test_app_session_id = "test-session-456"
    map_subId_with_appsessionId(test_app_session_id)

    # Assert mapping was created
    assert SUBSCRIPTION_ID_TO_APP_SESSION_ID[test_subscription.subscriptionId] == test_app_session_id

    # Call deletion
    delete_app_session_context_from_PCF(test_subscription.subscriptionId)

    # Check mapping is removed before delete call
    assert test_subscription.subscriptionId not in SUBSCRIPTION_ID_TO_APP_SESSION_ID

    # Ensure delete call was made with correct session_id
    mock_pcf_delete.assert_called_once_with(test_app_session_id)

