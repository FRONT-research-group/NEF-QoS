from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from typing import Optional, List, Dict

# Utility function to build the ProblemDetails JSON
def create_problem_details(
    status_code: int,
    title: str,
    detail: Optional[str] = None,
    instance: Optional[str] = None,
    invalid_params: Optional[List[Dict[str, str]]] = None,
    retry_after: Optional[str] = None
) -> JSONResponse:
    """Specific error handlers TS 29.122 clause 5.2.6 mandatory codes"""
    
    problem = {
        "title": title,
        "status": status_code
    }
    if detail:
        problem["detail"] = detail
    if instance:
        problem["instance"] = instance
    if invalid_params:
        problem["invalidParams"] = invalid_params
    if retry_after:
        problem["retryAfter"] = retry_after
    return JSONResponse(status_code=status_code, content=problem, media_type="application/problem+json")


def error_400(request: Request, detail: str, invalid_params: Optional[List[Dict[str, str]]] = None):
    return create_problem_details(400, "Bad Request", detail, str(request.url), invalid_params)

def error_401(request: Request, detail: str = "Unauthorized"):
    return create_problem_details(401, "Unauthorized", detail, str(request.url))

def error_403(request: Request, detail: str = "Forbidden"):
    return create_problem_details(403, "Forbidden", detail, str(request.url))

def error_404(request: Request, detail: str = "Not Found"):
    return create_problem_details(404, "Not Found", detail, str(request.url))

def error_406(request: Request, detail: str = "Not Acceptable"):
    return create_problem_details(406, "Not Acceptable", detail, str(request.url))

def error_411(request: Request, detail: str = "Length Required"):
    return create_problem_details(411, "Length Required", detail, str(request.url))

def error_413(request: Request, detail: str = "Payload Too Large"):
    return create_problem_details(413, "Payload Too Large", detail, str(request.url))

def error_415(request: Request, detail: str = "Unsupported Media Type"):
    return create_problem_details(415, "Unsupported Media Type", detail, str(request.url))

def error_429(request: Request, detail: str = "Too Many Requests", retry_after: Optional[str] = None):
    return create_problem_details(429, "Too Many Requests", detail, str(request.url), retry_after=retry_after)

def error_500(request: Request, detail: str = "Internal Server Error"):
    return create_problem_details(500, "Internal Server Error", detail, str(request.url))

def error_503(request: Request, detail: str = "Service Unavailable"):
    return create_problem_details(503, "Service Unavailable", detail, str(request.url))


# Generate OpenAPI responses from problem_details functions
def generate_error_responses():
    """Generate OpenAPI error responses schema from problem_details functions"""
    
    error_definitions = {
        400: {"title": "Bad Request", "has_invalid_params": True},
        401: {"title": "Unauthorized", "has_invalid_params": False},
        403: {"title": "Forbidden", "has_invalid_params": False},
        404: {"title": "Not Found", "has_invalid_params": False},
        406: {"title": "Not Acceptable", "has_invalid_params": False},
        411: {"title": "Length Required", "has_invalid_params": False},
        413: {"title": "Payload Too Large", "has_invalid_params": False},
        415: {"title": "Unsupported Media Type", "has_invalid_params": False},
        429: {"title": "Too Many Requests", "has_retry_after": True},
        500: {"title": "Internal Server Error", "has_invalid_params": False},
        503: {"title": "Service Unavailable", "has_invalid_params": False},
    }
    
    responses = {}
    
    for status_code, config in error_definitions.items():
        schema_props = {
            "title": {"type": "string"},
            "status": {"type": "integer"},
            "detail": {"type": "string"},
            "instance": {"type": "string"}
        }
        
        example = {
            "title": config["title"],
            "status": status_code,
            "detail": config["title"],
            "instance": "/scs-as-id/subscriptions"
        }
        
        # Add invalidParams for 400 errors
        if config.get("has_invalid_params"):
            schema_props["invalidParams"] = {
                "type": "array",
                "items": {"type": "object"}
            }
            example["invalidParams"] = [{"param": "example", "reason": "invalid value"}]
        
        # Add retryAfter for 429 errors
        if config.get("has_retry_after"):
            schema_props["retryAfter"] = {"type": "string"}
            example["retryAfter"] = "60"
        
        responses[status_code] = {
            "description": config["title"],
            "content": {
                "application/problem+json": {
                    "schema": {
                        "type": "object",
                        "properties": schema_props,
                        "required": ["title", "status"]
                    },
                    "example": example
                }
            }
        }
    
    return responses
