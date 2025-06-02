import httpx
from app.utils.log import get_app_logger

logger = get_app_logger()

async def send_callback_to_as(destination_url: str, subscription_id: str):
    payload = {
        "subscriptionId": subscription_id,
        "event": "QoS Session Created",
        "details": "This is a sample notification"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(str(destination_url), json=payload)
            response.raise_for_status()
            logger.info(f"Callback sent successfully to {destination_url}")
    except Exception as e:
        logger.error(f"Failed to send callback to {destination_url}: {e}")