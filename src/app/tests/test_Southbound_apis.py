import pytest
from fastapi.testclient import TestClient
from app import _app
from pydantic import HttpUrl
from app.services.Southbound_apis_svc import QOS_MAPPING
from app.schemas.qos_models import (
    FlowInfo, AsSessionWithQosSubscription, MediaSubComponent, MediaComponent,
    AppSessionContextReqData, FlowStatus, MediaType, AppSessionContext
)
from app.services.Southbound_apis_svc import create_app_session_context_to_PCF
from app.services.db import map_subId_with_appsessionId, delete_subId_with_appsessionId, SUBSCRIPTION_ID_TO_APP_SESSION_ID



def test_create_app_session_context_to_PCF_and_maps_qos_reference():
    flow_info = FlowInfo(
        flowId=1,
        flowDescriptions=[
            "permit in ip from 10.45.0.4 to any",
            "permit out ip from any to 10.45.0.4"
        ]
    )
    subscription = AsSessionWithQosSubscription(
        notificationDestination="https://example.com/callback",
        supportedFeatures="003C",
        qosReference="qod_4",
        ueIpv4Addr="10.45.0.3",
        flowInfo=[flow_info]
    )
    app_session_context = create_app_session_context_to_PCF(subscription)
    
    result = app_session_context.model_dump()
    asc = result["ascReqData"]
    med_comp = asc["medComponents"]["1"]
    med_sub_comp = med_comp["medSubComps"]["1"]
    # Field-by-field assertions
    assert str(asc["notifUri"]) == "https://example.com/callback"
    assert asc["suppFeat"] == "003C"
    assert str(asc["ueIpv4"]) == "10.45.0.3"
    assert med_comp["medCompN"] == 1

    qos = QOS_MAPPING[subscription.qosReference]
    
    assert med_comp["fStatus"] == "ENABLED"
    assert med_comp["medType"] == qos["mediaType"]
    assert med_comp["marBwUl"] == qos["marBwUl"]
    assert med_comp["marBwDl"] == qos["marBwDl"]
    assert med_sub_comp["fNum"] == 1
    assert med_sub_comp["fDescs"] == [
        "permit in ip from 10.45.0.4 to any",
        "permit out ip from any to 10.45.0.4"
    ]
    assert med_sub_comp["flowUsage"] == "NO_INFO"



def test_mapping_subId_with_appsessionId():
    """
    Test that SUBSCRIPTION_ID_TO_APP_SESSION_ID has at least one key:value pair.
    """
    assert len(SUBSCRIPTION_ID_TO_APP_SESSION_ID) > 0, "No mappings found!"
    subscriptionId, appSessionId = next(iter(SUBSCRIPTION_ID_TO_APP_SESSION_ID.items()))
    assert subscriptionId is not None
    assert appSessionId is not None
   
def test_delete_subId_with_appsessionId():

    print("Current SUBSCRIPTION_ID_TO_APP_SESSION_ID before deletion:", SUBSCRIPTION_ID_TO_APP_SESSION_ID)
    initial_len = len(SUBSCRIPTION_ID_TO_APP_SESSION_ID)
    assert initial_len > 0, "No mappings to delete!"

    # Pick a subscriptionId to delete
    subscriptionId = next(iter(SUBSCRIPTION_ID_TO_APP_SESSION_ID.keys()))
    delete_subId_with_appsessionId(subscriptionId)

    print("Current SUBSCRIPTION_ID_TO_APP_SESSION_ID after deletion:", SUBSCRIPTION_ID_TO_APP_SESSION_ID)
    assert len(SUBSCRIPTION_ID_TO_APP_SESSION_ID) == initial_len - 1
    assert subscriptionId not in SUBSCRIPTION_ID_TO_APP_SESSION_ID