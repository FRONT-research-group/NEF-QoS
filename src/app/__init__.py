'''
Docstring
'''
from fastapi import FastAPI
from app.routers import Northbound_apis

# FastAPI object customization
FASTAPI_TITLE = "AsSessionWithQoS"
FASTAPI_DESCRIPTION = "Qos API"
FASTAPI_VERSION = "0.109.0"
FASTAPI_OPEN_API_URL = "/"
FASTAPI_DOCS_URL = "/docs"

_app = FastAPI(title=FASTAPI_TITLE,
              description=FASTAPI_DESCRIPTION,
              version=FASTAPI_VERSION,
              docs_url=FASTAPI_DOCS_URL,
              openapi_url=FASTAPI_OPEN_API_URL)

_app.include_router(Northbound_apis.router, prefix="/3gpp-as-session-with-qos/v1")