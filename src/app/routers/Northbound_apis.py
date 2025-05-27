from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from typing import List, Dict

from app.schemas.qos_models import (
    AsSessionWithQosSubscription,
    AsSessionWithQosSubscriptionWithSubscriptionId,
    AsSessionWithQosSubscriptionPatch,
    UserPlaneNotificationData
)
from app.utils.log import get_app_logger
from app.services.Northbound_apis_svc import (
    get_subscriptions_based_on_scsAsId,
    create_subscription_for_a_given_scsAsId,
    get_ResponseBody_by_scsAsId_and_subscriptionId,
    put_scsAsId_and_subscriptionId,
    patch_scsAsId_and_subscriptionId,
    delete_subscriptionId
)
from app.services.db import in_memory_db


logger = get_app_logger()


router = APIRouter()


@router.get(
    "/{scsAsId}/subscriptions",
    tags=["Create and Get Subscriptions based on SCS/AS ID"],
    status_code=status.HTTP_200_OK,
    response_model=List[AsSessionWithQosSubscriptionWithSubscriptionId],
    description="Get all active subscriptions for a given SCS/AS ID"
)
async def get_subscriptions(
    scsAsId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> List[AsSessionWithQosSubscriptionWithSubscriptionId]:
    
    return await get_subscriptions_based_on_scsAsId(scsAsId, store)


@router.post(
    "/{scsAsId}/subscriptions",
    tags=["Create and Get Subscriptions based on SCS/AS ID"],
    status_code=status.HTTP_201_CREATED,
    response_model=AsSessionWithQosSubscriptionWithSubscriptionId,
    description="Create a new QoS subscription for the given SCS/AS ID"
)
async def create_subscription(
    scsAsId: str,
    initial_model: AsSessionWithQosSubscription,
    response: Response,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db))-> AsSessionWithQosSubscriptionWithSubscriptionId:

    return await create_subscription_for_a_given_scsAsId(scsAsId, initial_model, response, store)

@router.get(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    tags=["Request body based on SCS/AS ID and Subscription ID"],
    status_code=status.HTTP_200_OK,
    response_model=AsSessionWithQosSubscription,
    description="Get a specific subscription for the given SCS/AS ID"
)
async def get_scsAsId_and_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

    return await get_ResponseBody_by_scsAsId_and_subscriptionId(scsAsId, subscriptionId, store)

@router.put(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    tags=["Request body based on SCS/AS ID and Subscription ID"],
    status_code=status.HTTP_200_OK,
    response_model=AsSessionWithQosSubscription,
    description="Update a specific subscription for the given SCS/AS ID"
)
async def update_with_PUT_scsAsId_and_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    initial_model: AsSessionWithQosSubscription,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

    return await put_scsAsId_and_subscriptionId(scsAsId, subscriptionId, initial_model, store)


@router.patch(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    tags=["Request body based on SCS/AS ID and Subscription ID"],
    status_code=status.HTTP_200_OK,
    response_model=AsSessionWithQosSubscription,
    description="Update a specific subscription for the given SCS/AS ID"
)
async def update_with_PATCH_scsAsId_and_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    initial_model: AsSessionWithQosSubscriptionPatch,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

    return await patch_scsAsId_and_subscriptionId(scsAsId, subscriptionId, initial_model, store)

@router.delete(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    tags=["Request body based on SCS/AS ID and Subscription ID"],
    status_code=status.HTTP_200_OK,
    description="Delete a specific subscription for the given SCS/AS ID"
)
async def delete_with_subscriptionId(
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)
) -> UserPlaneNotificationData:

    return await delete_subscriptionId(scsAsId, subscriptionId, store)