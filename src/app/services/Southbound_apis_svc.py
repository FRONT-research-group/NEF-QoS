from app.schemas.qos_models import (
    AppSessionContext, AppSessionContextReqData, AsSessionWithQosSubscription,
    MediaComponent, MediaSubComponent, FlowStatus, MediaType
)
from app.utils.log import get_app_logger
from app.utils.app_config import QOS_MAPPING
from app.services.db import map_subId_with_appsessionId

logger = get_app_logger()




def create_app_session_context_to_PCF(initial_model: AsSessionWithQosSubscription):
    """
    Create the requestbody for the pcf, mapping values from the NorthboundApi
    like suppfeat, ipv4, and using QOS_MAPPING for QoS parameters.
    """

    med_components = {}
    qos_ref = initial_model.qosReference
    qos_profile = QOS_MAPPING.get(qos_ref)
    if not qos_profile:
        raise ValueError(f"Unknown qosReference: {qos_ref}")

    if initial_model.flowInfo:
        for flow in initial_model.flowInfo:
            med_sub_comp = MediaSubComponent.from_flow_info(flow)
            med_component = MediaComponent(
                medCompN=flow.flowId,
                fStatus=FlowStatus.ENABLED,
                medType=MediaType[qos_profile["mediaType"]],
                marBwUl=qos_profile["marBwUl"],
                marBwDl=qos_profile["marBwDl"],
                medSubComps={str(flow.flowId): med_sub_comp}
            )
            med_components[str(flow.flowId)] = med_component

    req_data = AppSessionContextReqData.from_subscription(
        from_subscription=initial_model,
        medComponents=med_components,
        notifUri=initial_model.notificationDestination #FIXME which uri?currently is using the initial_initial_model notificationDestination
    )
    app_session_context = AppSessionContext(ascReqData=req_data)

    
    logger.info("****This is a test of how the request body will be sent to PCF****")
    # here implement http2 request to PCF
    # pcf returns a 201 Created response with a Location header
    #extracting the location header to get the appSessionId
    #end we map the appsessionid with the subscriptionId cause PCF gives a int as appSessionId
    import random
    map_subId_with_appsessionId(random.randint(100, 999))  # Simulating appSessionId mapping


    logger.info(app_session_context.model_dump_json(indent=2))
    return app_session_context

# The PCF will respond with a 201 Created header like this:
# Name: Location
# Data type: string
# P Cardinality: M 1
# Description:
#   Contains the URI of the newly created resource, according to
#   the structure: {apiRoot}/npcf-policyauthorization/v1/app-sessions/{appSessionId}

#i want to map {appSessionId} which the pcf will return with my current UUID

# Example function to extract appSessionId from a Location header

#TODO add delete function to delete the appSessionId from the PCF