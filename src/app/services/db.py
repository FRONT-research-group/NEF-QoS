from app.schemas.qos_models import AsSessionWithQosSubscriptionWithSubscriptionId
from typing import List, Dict
from app.utils.log import get_app_logger
from app.schemas.qos_models import FlowInfo
from pydantic import HttpUrl
from ipaddress import IPv4Address

logger = get_app_logger()

# In-memory store for subscriptions
SUBSCRIPTION_STORE: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = {}

# In-memory store for mapping subscriptionId to appSessionId
SUBSCRIPTION_ID_TO_APP_SESSION_ID: Dict[str, str] = {}

def in_memory_db():
    # logger.info(SUBSCRIPTION_STORE)
    # logger.info(SUBSCRIPTION_ID_TO_APP_SESSION_ID)
    return SUBSCRIPTION_STORE

def map_subId_with_appsessionId(appsessionID):
    """ Maps subscriptionId to appSessionId in the in-memory store."""
    for subscriptions in SUBSCRIPTION_STORE.values():
        for sub in subscriptions:
            if not SUBSCRIPTION_ID_TO_APP_SESSION_ID.get(sub.subscriptionId):
                SUBSCRIPTION_ID_TO_APP_SESSION_ID[sub.subscriptionId] = appsessionID
                logger.info(f"Mapped subscriptionId {sub.subscriptionId} with appSessionId {appsessionID}")
    return SUBSCRIPTION_ID_TO_APP_SESSION_ID

def get_app_session_id(subscriptionId):
    """
    Retrieves the app session ID associated with the given subscription ID.
    """
    return SUBSCRIPTION_ID_TO_APP_SESSION_ID.get(subscriptionId, None)

def delete_subId_with_appsessionId(subscriptionId):
    """
    Deletes the mapping of subscriptionId to appSessionId.
    """
    if subscriptionId in SUBSCRIPTION_ID_TO_APP_SESSION_ID:
        del SUBSCRIPTION_ID_TO_APP_SESSION_ID[subscriptionId]
    else:
        logger.warning(f"SubscriptionId {subscriptionId} not found in mappings.")




if __name__ == "__main__":

    SUBSCRIPTION_STORE = {
        'example': [
            AsSessionWithQosSubscriptionWithSubscriptionId(
                notificationDestination=HttpUrl('https://example.com/callback'),
                supportedFeatures='003C',
                qosReference='qod_2',
                ueIpv4Addr=IPv4Address('10.45.0.3'),
                flowInfo=[
                    FlowInfo(
                        flowId=1,
                        flowDescriptions=[
                            'permit in ip from 10.45.0.4 to any',
                            'permit out ip from any to 10.45.0.4'
                        ]
                    )
                ],
                subscriptionId='995082ed-b16a-4595-affb-913e63249430'
            )
        ],
        # 'example2': [
        #     AsSessionWithQosSubscriptionWithSubscriptionId(
        #         notificationDestination=HttpUrl('https://example.com/callback'),
        #         supportedFeatures='003C',
        #         qosReference='qod_2',
        #         ueIpv4Addr=IPv4Address('10.45.0.3'),
        #         flowInfo=[
        #             FlowInfo(
        #                 flowId=1,
        #                 flowDescriptions=[
        #                     'permit in ip from 10.45.0.4 to any',
        #                     'permit out ip from any to 10.45.0.4'
        #                 ]
        #             )
        #         ],
        #         subscriptionId='90f149c5-f83c-41d4-ab82-39157b4e6b1f'
        #     ),
        #     AsSessionWithQosSubscriptionWithSubscriptionId(
        #         notificationDestination=HttpUrl('https://example.com/callback'),
        #         supportedFeatures='003C',
        #         qosReference='qod_2',
        #         ueIpv4Addr=IPv4Address('10.45.0.3'),
        #         flowInfo=[
        #             FlowInfo(
        #                 flowId=1,
        #                 flowDescriptions=[
        #                     'permit in ip from 10.45.0.4 to any',
        #                     'permit out ip from any to 10.45.0.4'
        #                 ]
        #             )
        #         ],
        #         subscriptionId='eca4eba1-4a05-4d25-89eb-af247c50ef7c'
        #     ),
        #     AsSessionWithQosSubscriptionWithSubscriptionId(
        #         notificationDestination=HttpUrl('https://example.com/callback'),
        #         supportedFeatures='003C',
        #         qosReference='qod_2',
        #         ueIpv4Addr=IPv4Address('10.45.0.3'),
        #         flowInfo=[
        #             FlowInfo(
        #                 flowId=1,
        #                 flowDescriptions=[
        #                     'permit in ip from 10.45.0.4 to any',
        #                     'permit out ip from any to 10.45.0.4'
        #                 ]
        #             )
        #         ],
        #         subscriptionId='e291db4b-d727-4390-9f85-64104170e3ca'
        #     ),
        #     AsSessionWithQosSubscriptionWithSubscriptionId(
        #         notificationDestination=HttpUrl('https://example.com/callback'),
        #         supportedFeatures='003C',
        #         qosReference='qod_2',
        #         ueIpv4Addr=IPv4Address('10.45.0.3'),
        #         flowInfo=[
        #             FlowInfo(
        #                 flowId=1,
        #                 flowDescriptions=[
        #                     'permit in ip from 10.45.0.4 to any',
        #                     'permit out ip from any to 10.45.0.4'
        #                 ]
        #             )
        #         ],
        #         subscriptionId='9dd86c39-7273-4c4e-b633-c6e387b195d5'
        #     )
        # ]
    }
    # Call the function and print the result
    print(map_subId_with_appsessionId(166))