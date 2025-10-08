from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    Request
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
    tags=["AsSessionWithQoS API SCS/AS level GET Operation"],
    status_code=status.HTTP_200_OK,
    response_model=List[AsSessionWithQosSubscriptionWithSubscriptionId],
    description="Read all active subscriptions for the SCS/AS"
)
async def get_all_subsciptions_based_on_SCSAS(
    request: Request,
    scsAsId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> List[AsSessionWithQosSubscriptionWithSubscriptionId]:
    
    return await get_subscriptions_based_on_scsAsId(request, scsAsId, store)


@router.post(
    "/{scsAsId}/subscriptions",
    tags=["AsSessionWithQoS API Subscription level CRUD Operations"],
    status_code=status.HTTP_201_CREATED,
    response_model=AsSessionWithQosSubscriptionWithSubscriptionId,
    description="Creates a new subscription resource"
)
async def create_subscription(
    request: Request,
    scsAsId: str,
    initial_model: AsSessionWithQosSubscription,
    response: Response,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db))-> AsSessionWithQosSubscriptionWithSubscriptionId:

    return await create_subscription_for_a_given_scsAsId(request, scsAsId, initial_model, response, store)

@router.get(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    tags=["AsSessionWithQoS API Subscription level CRUD Operations"],
    status_code=status.HTTP_200_OK,
    response_model=AsSessionWithQosSubscription,
    description="read an active subscriptions for the SCS/AS and the subscription Id"
)
async def get_with_scsAsId_and_subscriptionId(
    request: Request,
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

    return await get_ResponseBody_by_scsAsId_and_subscriptionId(request,scsAsId, subscriptionId, store)


####### NOTE PUT AND PATCH METHODS ARE COMMENTED OUT CAUSE OPEN5GS DOESNT SUPPORT IT, BUT THEY ARE 3GPP COMPLIANT ########
# @router.put(
#     "/{scsAsId}/subscriptions/{subscriptionId}",
#     tags=["AsSessionWithQoS API Subscription level CRUD Operations"],
#     status_code=status.HTTP_200_OK,
#     response_model=AsSessionWithQosSubscription,
#     description="Updates/replaces an existing subscription resource"
# )
# async def update_with_PUT_scsAsId_and_subscriptionId(
#     request: Request,
#     scsAsId: str,
#     subscriptionId: str,
#     initial_model: AsSessionWithQosSubscription,
#     store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

#     return await put_scsAsId_and_subscriptionId(request,scsAsId, subscriptionId, initial_model, store)


# @router.patch(
#     "/{scsAsId}/subscriptions/{subscriptionId}",
#     tags=["AsSessionWithQoS API Subscription level CRUD Operations"],
#     status_code=status.HTTP_200_OK,
#     response_model=AsSessionWithQosSubscription,
#     description="Updates/replaces an existing subscription resource"
# )
# async def update_with_PATCH_scsAsId_and_subscriptionId(
#     request: Request,
#     scsAsId: str,
#     subscriptionId: str,
#     initial_model: AsSessionWithQosSubscriptionPatch,
#     store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)) -> AsSessionWithQosSubscription:

#     return await patch_scsAsId_and_subscriptionId(request ,scsAsId, subscriptionId, initial_model, store)

@router.delete(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    tags=["AsSessionWithQoS API Subscription level CRUD Operations"],
    status_code=status.HTTP_200_OK,
    response_model=UserPlaneNotificationData,
    description="Deletes an already existing subscription"
)
async def delete_with_scsAsId_and_subscriptionId(
    request: Request,
    scsAsId: str,
    subscriptionId: str,
    store: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = Depends(in_memory_db)):

    return await delete_subscriptionId(request ,scsAsId, subscriptionId, store)
