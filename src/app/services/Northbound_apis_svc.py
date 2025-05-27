from fastapi import  Depends, HTTPException, Response
from typing import List, Dict
from app.schemas.qos_models import AsSessionWithQosSubscription, AsSessionWithQosSubscriptionWithSubscriptionId,AsSessionWithQosSubscriptionPatch
from app.utils.log import get_app_logger
from app.services.db import in_memory_db
from uuid import uuid4
from app.schemas.qos_models import UserPlaneNotificationData, UserPlaneEventReport, UserPlaneEvent

logger = get_app_logger()

async def get_subscriptions_based_on_scsAsId(
    scsAsId: str,
    store: Dict[str, List[AsSessionWithQosSubscription]] = Depends(in_memory_db)) -> List[AsSessionWithQosSubscription]:
    

    if scsAsId not in store:
        raise HTTPException(status_code=404, detail=f"SCS/AS '{scsAsId}' not found")

    logger.info(f"Fetching subscriptions for {scsAsId=}")
    return store[scsAsId]


async def create_subscription_for_a_given_scsAsId(
    scsAsId: str,
    initial_model: AsSessionWithQosSubscription,
    response: Response,
    store: Dict[str, List[AsSessionWithQosSubscription]] = Depends(in_memory_db)):


    
    if scsAsId not in store:
        store[scsAsId] = []

    subscription_id = str(uuid4())

    # add the subscriptionId to the model 
    full_subscription = AsSessionWithQosSubscriptionWithSubscriptionId(
        subscriptionId=subscription_id,
        **initial_model.model_dump()
    )

    store[scsAsId].append(full_subscription)

    response.headers["Location"] = f"/3gpp-as-session-with-qos/v1/{scsAsId}/subscriptions/{subscription_id}"

    logger.info(f"Created subscription {subscription_id} for scsAsId={scsAsId}")

    return full_subscription


async def get_ResponseBody_by_scsAsId_and_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscription]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

    subscriptions = store.get(scsAsId, [])
    for sub in subscriptions:
        if getattr(sub, "subscriptionId", None) == subscriptionId:
            return sub
    raise HTTPException(status_code=404, detail="Subscription not found")



async def put_scsAsId_and_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    initial_model: AsSessionWithQosSubscription,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)
) -> AsSessionWithQosSubscription:
    
    subscriptions = store.get(scsAsId, [])
    
    for i, sub in enumerate(subscriptions):
        if getattr(sub, "subscriptionId", None) == subscriptionId:
            original_ipv4 = sub.ueIpv4Addr
            
            if initial_model.ueIpv4Addr is not None and initial_model.ueIpv4Addr != original_ipv4:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot change ueIpv4Addr from {original_ipv4} to {initial_model.ueIpv4Addr}"
                )
            
            updated_model_data = initial_model.model_dump()
            updated_model_data['ueIpv4Addr'] = original_ipv4
            
            subscriptions[i] = AsSessionWithQosSubscriptionWithSubscriptionId(
                **updated_model_data,
                subscriptionId=subscriptionId
            )
            
            return AsSessionWithQosSubscription(**updated_model_data)

    raise HTTPException(status_code=404, detail="Subscription not found")

async def patch_scsAsId_and_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    initial_model: AsSessionWithQosSubscriptionPatch,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)
) -> AsSessionWithQosSubscription:

    subscriptions = store.get(scsAsId, [])
    
    for i, sub in enumerate(subscriptions):
        if getattr(sub, "subscriptionId", None) == subscriptionId:
            updated_data = sub.model_dump(exclude={'subscriptionId'})          
            patch_data = initial_model.model_dump(exclude_unset=True)
            updated_data.update(patch_data)
            
            
            subscriptions[i] = AsSessionWithQosSubscriptionWithSubscriptionId(
                **updated_data,
                subscriptionId=subscriptionId
            )
            
            return AsSessionWithQosSubscription(**updated_data)
    
    raise HTTPException(status_code=404, detail="Subscription not found")

async def delete_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> UserPlaneNotificationData:
    #FIXME its not correct with this transaction URL 
    subscriptions = store.get(scsAsId, [])
    for sub in subscriptions:
        if getattr(sub, "subscriptionId", None) == subscriptionId:
            subscriptions.remove(sub)
            logger.info(f"Deleted subscription {subscriptionId} for scsAsId={scsAsId}")
            
            return UserPlaneNotificationData(
                transaction=f"https://example.com/callback/transaction/{subscriptionId}",
                eventReports=[
                    UserPlaneEventReport(event=UserPlaneEvent.SESSION_TERMINATION)
                ]
            )


    raise HTTPException(status_code=404, detail="Subscription not found")