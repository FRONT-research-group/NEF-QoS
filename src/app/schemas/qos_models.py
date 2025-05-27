from typing import Optional, List
from pydantic import BaseModel, IPvAnyAddress, HttpUrl, field_validator
import re
from enum import Enum


FLOW_DESCRIPTION_REGEX = re.compile(
    r'^permit (in|out) (ip|tcp|udp) from '
    r'([0-9a-fA-F:.]+|any)(?: (?:(?:0|[1-9][0-9]{0,4})))? to '
    r'([0-9a-fA-F:.]+|any)(?: (?:(?:0|[1-9][0-9]{0,4})))?$'
)

FORBIDDEN_KEYWORDS = ["!", "options", "assigned", ",", "-", ".."]


class FlowInfo(BaseModel):
    """Validates the Flow-Description format as per 3GPP TS 129_214 clause 5.3.8"""
    flowId: int
    flowDescriptions: Optional[List[str]] = None

    @field_validator('flowDescriptions')
    @classmethod
    def validate_flow_descriptions(cls, v):
        if v is None:
            return v
        for rule in v:
            if not FLOW_DESCRIPTION_REGEX.match(rule):
                raise ValueError(f"Invalid Flow-Description format: {rule}")
            if any(bad in rule for bad in FORBIDDEN_KEYWORDS):
                raise ValueError(f"Disallowed keyword or format in Flow-Description: {rule}")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "flowId": 1,
                "flowDescriptions": [
                    "permit in ip from 10.45.0.4 to any",
                    "permit out ip from any to 10.45.0.4"
                ]
            }]
        }
    }



class AsSessionWithQosSubscription(BaseModel):
    notificationDestination: HttpUrl
    supportedFeatures: Optional[str] = None
    exterAppId: Optional[str] = None
    qosReference: Optional[str] = None
    ueIpv4Addr: Optional[IPvAnyAddress] = None
    flowInfo: Optional[List] = None
    requestTestNotification: Optional[bool] = True

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "notificationDestination": "https://example.com/callback",
                    "supportedFeatures": "003C",
                    "qosReference": "qod_2",
                    "ueIpv4Addr": "10.45.0.3",
                    "flowInfo": [
                        {
                            "flowId": 1,
                            "flowDescriptions": [
                                "permit in ip from 10.45.0.4 to any",
                                "permit out ip from any to 10.45.0.4"
                            ]
                        }
                    ],
                    "requestTestNotification": True
                }
            ]
        }
    }
class AsSessionWithQosSubscriptionWithSubscriptionId(AsSessionWithQosSubscription):
    """This Class is used to add the subscriptionId to the existing AsSessionWithQosSubscription model"""
    subscriptionId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {   
                    "subscriptionId": "UUID-example",
                    "notificationDestination": "https://example.com/callback",
                    "supportedFeatures": "003C",
                    "ueIpv4Addr": "192.168.0.1",
                    "qosReference": "qod_2",
                    "flowInfo": [
                        {
                            "flowId": 1,
                            "flowDescriptions": [
                                "permit in ip from 10.45.0.4 to any",
                                "permit out ip from any to 10.45.0.4"
                            ]
                        }
                    ],
                    "requestTestNotification": True
                }
            ]
        }
    }

class AsSessionWithQosSubscriptionPatch(BaseModel):
    """This Class is used to patch the existing AsSessionWithQosSubscription model"""
    notificationDestination: Optional[HttpUrl] = None
    exterAppId: Optional[str] = None
    qosReference: Optional[str] = None
    flowInfo: Optional[List[FlowInfo]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "notificationDestination": "https://example.com/callback",
                    "exterAppId": "external-app-123",
                    "qosReference": "qos_42",
                    "flowInfo": [
                        {
                            "flowId": 1,
                            "flowDescriptions": [
                                "permit in ip from 10.45.1.4 to any",
                                "permit out ip from any to 10.45.0.4"
                            ]
                        }
                    ]
                }
            ]
        }
    }

class UserPlaneEvent(str, Enum):
    """Table 5.2.1.3.3-1: Enumeration Event as per 3GPP TS 29.122"""

    SESSION_TERMINATION = "SESSION_TERMINATION"
    LOSS_OF_BEARER = "LOSS_OF_BEARER"
    RECOVERY_OF_BEARER = "RECOVERY_OF_BEARER"
    RELEASE_OF_BEARER = "RELEASE_OF_BEARER"
    USAGE_REPORT = "USAGE_REPORT"
    FAILED_RESOURCES_ALLOCATION = "FAILED_RESOURCES_ALLOCATION"
    SUCCESSFUL_RESOURCES_ALLOCATION = "SUCCESSFUL_RESOURCES_ALLOCATION"

class UserPlaneEventReport(BaseModel):
    event: UserPlaneEvent

class UserPlaneNotificationData(BaseModel):
    transaction: HttpUrl
    eventReports: List[UserPlaneEventReport]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaction": "https://example.com/callback/transaction-123",
                    "eventReports": [
                        {
                            "event": UserPlaneEvent.SESSION_TERMINATION
                        }
                    ]
                }
            ]
        }
    }
