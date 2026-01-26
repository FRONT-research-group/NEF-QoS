'''
    Run this with:
      uvicorn main:_app --host 0.0.0.0 --port 8000 --reload or python3 main.py
'''
from app.utils.log import get_app_logger 
from app import _app
from app.utils.app_config import NEF_BASE_URL,PCF_BASE_URL

logger = get_app_logger()

logger.info('*** NEF-AsSessionWithQos **')
logger.info(f'NEF Base URL: {NEF_BASE_URL}')
logger.info(f'PCF Base URL: {PCF_BASE_URL}')


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(_app, host="0.0.0.0", port=8585)
