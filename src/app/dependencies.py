from app.utils.log import get_app_logger
from app.provider_onboarding.provider_capif_connector import onboard_provider, offboard_provider

log = get_app_logger()

def onboard_to_capif() -> None:
    try:
        log.info("Onboarding to CAPIF process begin")
        
        onboard_provider()
    
        log.info("Onboarding to CAPIF process finished successfully")
    except Exception as exc:
        log.error("Onboarding to CAPIF process failed: %s", exc)
        raise
    
async def offboard_from_capif() -> None:
    try:
        log.info("Offboarding from CAPIF process begin")
        offboard_provider()
        log.info("Offboarding from CAPIF process finished successfully")
    except Exception as exc:
        log.error("Offboarding from CAPIF process failed: %s", exc)
        raise