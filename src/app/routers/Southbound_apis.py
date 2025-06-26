# #NEF -> PCF
# from fastapi import APIRouter, Depends, HTTPException
# from app.utils.log import get_app_logger

# logger = get_app_logger()


# router = APIRouter()

# @router.get("/app-sessions")
# async def get_app_sessions():
#     logger.info("PCF received NEF request to GET /app-sessions")
    
#     # Dummy response – typically you'd fetch session info from PCF logic
#     session_info = {
#         "sessionId": "abcd-1234",
#         "qosReference": "qosLowLatency",
#         "status": "active"
#     }

#     # Simulate error logic
#     if not session_info:
#         logger.warning("No session info found")
#         raise HTTPException(status_code=404, detail="No sessions found")

#     return {"message": "Session retrieved", "session": session_info}