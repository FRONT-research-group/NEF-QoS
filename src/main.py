'''
    Run this with:
      uvicorn main:_app --host 0.0.0.0 --port 8000 --reload
'''
from app.utils.log import get_app_logger 
from app import _app

logger = get_app_logger()

logger.info('*** NEF-QoS **')


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(_app, host="0.0.0.0", port=8001)
