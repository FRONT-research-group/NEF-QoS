import httpx
from app.utils.log import get_app_logger
from uuid import uuid4
from app.schemas.qos_models import UserPlaneNotificationData, UserPlaneEvent, UserPlaneEventReport



logger = get_app_logger()


async def send_callback_to_as(notification_destination: str, event: UserPlaneEvent):
    transaction_url = f"{notification_destination}/transactions/{uuid4()}"
    payload = UserPlaneNotificationData(
        transaction=transaction_url,
        eventReports=[
            UserPlaneEventReport(event=event)
        ]
    )
    
    payload_json = payload.model_dump_json()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                str(notification_destination),
                content=payload_json,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            logger.info(f"Callback sent successfully to {notification_destination}")
    except Exception as e:
        logger.error(f"Failed to send callback to {notification_destination}: {e}")

