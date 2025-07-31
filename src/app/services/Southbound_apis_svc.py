import json
from app.schemas.qos_models import (
    AppSessionContext, AppSessionContextReqData, AsSessionWithQosSubscription,
    MediaComponent, MediaSubComponent, FlowStatus, MediaType
)
from app.utils.log import get_app_logger
from app.utils.app_config import QOS_MAPPING
from app.services.db import map_subId_with_appsessionId, delete_subId_with_appsessionId, get_app_session_id
from app.helpers.pcf_http2_requests import pcf_delete_request,pcf_post_request


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
                medCompN=1,  # Always set to 1 as because we request only one qos_profile
                fStatus=FlowStatus.ENABLED,
                medType=MediaType[qos_profile["mediaType"]],
                marBwUl=qos_profile["marBwUl"],
                marBwDl=qos_profile["marBwDl"],
                medSubComps={str(flow.flowId): med_sub_comp}
            )
            med_components["1"] = med_component   # Always set to 1 as because we request only one qos_profile

    req_data = AppSessionContextReqData.from_subscription(
        from_subscription=initial_model,
        medComponents=med_components,
        notifUri=initial_model.notificationDestination #FIXME which uri?currently is using the initial_initial_model notificationDestination
    )


    app_session_context = AppSessionContext(ascReqData=req_data)


    # 
    # Convert model to dict
    payload = app_session_context.model_dump(mode="json")
    # Pass dict to function (do NOT serialize here)
    session_id = pcf_post_request(payload)

    logger.debug(f"Payload to PCF: {json.dumps(payload, indent=2)}") 
 


# Return the AppSessionContext object

    
    # logger.info("****This is a test of how the request body will be sent to PCF****")
    # here implement http2 request to PCF
    # pcf returns a 201 Created response with a Location header
    #extracting the location header to get the appSessionId
    #end we map the appsessionid with the subscriptionId cause PCF gives a int as appSessionId

    map_subId_with_appsessionId(session_id)  # appSessionId mapping

    # logger.info(app_session_context.model_dump_json(indent=2))
    # return app_session_context




def delete_app_session_context_from_PCF(subscriptionId):
    """
    Deletes the App Session Context from PCF using the app_session_id.
    """
    session_id = get_app_session_id(subscriptionId)  # Get the app session ID from the mapping
    logger.debug(f"subscriptionId: {subscriptionId} and session_id: {session_id}")

    delete_subId_with_appsessionId(subscriptionId)# Remove mapping first
    logger.debug(f"Deleted mapping for subscriptionId: {subscriptionId}")
   # delete actual app session context from PCF
    pcf_delete_request(session_id)


    logger.debug(f"Deleted App Session Context for subscriptionId: {subscriptionId} and session_id: {session_id}")



#TODO maybe add a PATCH request also dont know if we need it
# ps i tested it and it works but only for uplink downlink, if i change MediaType to video or voice it creates a new qos_flow but with the same session_id 
#NOTE GET request is not supported by open5gs