from fastapi import  Depends, Response, Request
from typing import List, Dict
from app.schemas.qos_models import (AsSessionWithQosSubscription, 
                                    AsSessionWithQosSubscriptionWithSubscriptionId,
                                    AsSessionWithQosSubscriptionPatch, 
                                    UserPlaneNotificationData, 
                                    UserPlaneEventReport)
from app.utils.log import get_app_logger
from app.services.db import in_memory_db
from uuid import uuid4
from app.schemas.qos_models import UserPlaneEvent
from app.helpers.callback import send_callback_to_as
from app.helpers.problem_details import error_400, error_404, error_500
from app.utils.app_config import NEF_BASE_URL

logger = get_app_logger()

async def get_subscriptions_based_on_scsAsId(
    request: Request,
    scsAsId: str,
    store: Dict[str, List[AsSessionWithQosSubscription]] = Depends(in_memory_db)) -> List[AsSessionWithQosSubscription]:
    try:
        if scsAsId not in store:
            return error_404(request, f"SCS/AS '{scsAsId}' not found.")

        logger.info(f"Fetching subscriptions for {scsAsId=}")


        return store[scsAsId]
    
    except Exception as e:
        logger.error(f"Error while fetching subscriptions for {scsAsId=}: {e}")
        return error_500(request, f"Unexpected error: {str(e)}")

async def create_subscription_for_a_given_scsAsId(
    request: Request,
    scsAsId: str,
    initial_model: AsSessionWithQosSubscription,
    response: Response,
    store: Dict[str, List[AsSessionWithQosSubscription]] = Depends(in_memory_db)):

    try:
        if not initial_model:
            return error_400(request, "Request body is missing or invalid.")
        
        if scsAsId not in store:
            store[scsAsId] = []

        subscription_id = str(uuid4())
        full_subscription = AsSessionWithQosSubscriptionWithSubscriptionId(
            subscriptionId=subscription_id,
            **initial_model.model_dump()
        )
        store[scsAsId].append(full_subscription)

        response.headers["Location"] = f"/3gpp-as-session-with-qos/v1/{scsAsId}/subscriptions/{subscription_id}"
        logger.info(f"Created subscription {subscription_id} for scsAsId={scsAsId}")
        
        notification_destination = str(full_subscription.notificationDestination)

        await send_callback_to_as(notification_destination=notification_destination,
                                    event=UserPlaneEvent.SUCCESSFUL_RESOURCES_ALLOCATION)
        return full_subscription
    
    except Exception as e:
        logger.error(f"Error while creating subscription for {scsAsId=}: {e}")
        return error_500(request, f"Unexpected error: {str(e)}")

async def get_ResponseBody_by_scsAsId_and_subscriptionId(
    request: Request,
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscription]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

    try:
        subscriptions = store.get(scsAsId, [])
        for sub in subscriptions:
            if getattr(sub, "subscriptionId", None) == subscriptionId:
                return sub

        return error_404(request, detail=f"Subscription '{subscriptionId}' for SCS/AS '{scsAsId}' not found")
    except Exception as e:
        logger.error(f"Error while fetching subscription {subscriptionId} for {scsAsId=}: {e}")
        return error_500(request, f"Unexpected error: {str(e)}")



async def put_scsAsId_and_subscriptionId(
    request: Request,
    scsAsId: str,
    subscriptionId: str,
    initial_model: AsSessionWithQosSubscription,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)
) -> AsSessionWithQosSubscription:
    
    subscriptions = store.get(scsAsId, [])
    
    try:
        for i, sub in enumerate(subscriptions):
            if getattr(sub, "subscriptionId", None) == subscriptionId:
                original_ipv4 = sub.ueIpv4Addr

                if initial_model.ueIpv4Addr is not None and initial_model.ueIpv4Addr != original_ipv4:
                    return error_400(
                        request,
                        detail=f"Cannot change ueIpv4Addr from {original_ipv4} to {initial_model.ueIpv4Addr}",
                        invalid_params=[{"name": "ueIpv4Addr", "reason": "Changing ueIpv4Addr is not allowed"}]
                    )

                updated_model_data = initial_model.model_dump()
                updated_model_data['ueIpv4Addr'] = original_ipv4

                subscriptions[i] = AsSessionWithQosSubscriptionWithSubscriptionId(
                    **updated_model_data,
                    subscriptionId=subscriptionId
                )

                return AsSessionWithQosSubscription(**updated_model_data)

        return error_404(
            request,
            detail=f"Subscription '{subscriptionId}' for SCS/AS '{scsAsId}' not found"
        )
    except Exception as e:
        logger.error(f"Error while updating subscription {subscriptionId} for {scsAsId=}: {e}")
        return error_500(request, f"Unexpected error: {str(e)}")
    

async def patch_scsAsId_and_subscriptionId(
    request: Request,
    scsAsId: str,
    subscriptionId: str,
    initial_model: AsSessionWithQosSubscriptionPatch,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)
) -> AsSessionWithQosSubscription:

    subscriptions = store.get(scsAsId, [])
    try:
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
        
        return error_404(
            request,
            detail=f"Subscription '{subscriptionId}' for SCS/AS '{scsAsId}' not found"
        )
    except Exception as e:
        logger.error(f"Error while patching subscription {subscriptionId} for {scsAsId=}: {e}")
        return error_500(request, f"Unexpected error: {str(e)}")

async def delete_subscriptionId(
    request: Request,
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> UserPlaneNotificationData:

    subscriptions = store.get(scsAsId, [])
    for sub in subscriptions:
        if getattr(sub, "subscriptionId", None) == subscriptionId:
            subscriptions.remove(sub)
            logger.info(f"Deleted subscription {subscriptionId} for scsAsId={scsAsId}")

            notification_destination = str(sub.notificationDestination)
            
            transaction_url = f"{NEF_BASE_URL}/transactions/{uuid4()}"
            payload = UserPlaneNotificationData(
                transaction=transaction_url,
                eventReports=[
                    UserPlaneEventReport(event=UserPlaneEvent.SESSION_TERMINATION)
                ]
            )
            try:
                await send_callback_to_as(notification_destination, event=UserPlaneEvent.SESSION_TERMINATION)
            except Exception as e:
                logger.error(f"Callback failed: {e}")

            return payload
        
    return error_404(
        request,
        detail=f"Subscription '{subscriptionId}' for SCS/AS '{scsAsId}' not found."
    )

