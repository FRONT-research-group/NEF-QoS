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
from app.services.db import in_memory_db, map_subId_with_appsessionId



def test_create_app_session_context_to_PCF_maps_qos_reference():
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
    Test the mapping of subscriptionId with appSessionId.
    This is a mock test to ensure that the mapping function works as expected.
    """
    # Simulate creating a mapping
    sub_id = "sub_12345"
    app_session_id = 67890
    map_subId_with_appsessionId(app_session_id)

    # Check if the mapping exists in the in-memory store
    store = in_memory_db()
    assert store.get(sub_id) == app_session_id, f"Expected {app_session_id} for {sub_id}, got {store.get(sub_id)}"