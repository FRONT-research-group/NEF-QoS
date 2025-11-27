from typing import Optional, List
from pydantic import BaseModel, IPvAnyAddress, HttpUrl, field_validator
import re
from enum import Enum


FLOW_DESCRIPTION_REGEX = re.compile(
    r'^permit (in|out) (ip|tcp|udp) from '
    r'([0-9a-fA-F:.]+(?:/\d+)?|any)(?: (?:(?:0|[1-9][0-9]{0,4})|(?:[0-9]+-[0-9]+)))? to '
    r'([0-9a-fA-F:.]+(?:/\d+)?|any)(?: (?:(?:0|[1-9][0-9]{0,4})|(?:[0-9]+-[0-9]+)))?$'
)

FORBIDDEN_KEYWORDS = ["!", "options", "assigned", ",", ".."]


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
    qosReference: Optional[str] = None
    ueIpv4Addr: Optional[IPvAnyAddress] = None
    flowInfo: Optional[List[FlowInfo]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "notificationDestination": "https://example.com/callback",
                    "supportedFeatures": "12",
                    "qosReference": "QOS_L",
                    "ueIpv4Addr": "10.45.0.4",
                    "flowInfo": [
                        {
                            "flowId": 1,
                            "flowDescriptions": [
                                "permit in ip from 10.45.0.4 to any",
                                "permit out ip from any to 10.45.0.4"
                            ]
                        }
                    ],
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
                    "supportedFeatures": "12",
                    "ueIpv4Addr": "10.45.0.4",
                    "qosReference": "qod_2",
                    "flowInfo": [
                        {
                            "flowId": 1,
                            "flowDescriptions": [
                                "permit in ip from 10.45.0.4 to any",
                                "permit out ip from any to 10.45.0.4"
                            ]
                        }
                    ],                }
            ]
        }
    }

class AsSessionWithQosSubscriptionPatch(BaseModel):
    """This Class is used to patch the existing AsSessionWithQosSubscription model"""
    notificationDestination: Optional[HttpUrl] = None

    qosReference: Optional[str] = None
    flowInfo: Optional[List[FlowInfo]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "notificationDestination": "https://example.com/callback",
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
                    "transaction": "http://localhost:8001/3gpp-as-session-with-qos/v1/example/subscriptions/4e27a197-075f-4cab-8750-23cbbc316f8c",
                    "eventReports": [
                        {
                            "event": UserPlaneEvent.SESSION_TERMINATION
                        }
                    ]
                }
            ]
        }
    }


##### FROM 3GPP TS_129514 NEF-PCF models #####

class FlowUsage(str, Enum):
    """Enumeration for flow usage as per 3GPP TS 29.214 Table 5.6.3.14-1"""
    NO_INFO = "NO_INFO"         # No information about the usage of the IP flow is provided (default).
    # RTCP = "RTCP"               # IP flow is used to transport RTCP.
    # AF_SIGNALLING = "AF_SIGNALLING"  # IP flow is used to transport AF Signalling Protocols (e.g. SIP/SDP).

# BitRate is now a type alias for str, validation is handled in MediaComponent
BitRate = str

class MediaType(str, Enum):
    """Media types as per 3GPP TS 29.214 5.6.3.4"""
    AUDIO = "AUDIO"         # The type of media is audio.
    VIDEO = "VIDEO"         # The type of media is video.
    # DATA = "DATA"           # The type of media is data.
    # APPLICATION = "APPLICATION" # The type of media is application data.
    CONTROL = "CONTROL"     # The type of media is control.
    # TEXT = "TEXT"           # The type of media is text.
    # MESSAGE = "MESSAGE"     # The type of media is message.
    # OTHER = "OTHER"         # Other type of media.


class MediaSubComponent(BaseModel):
    fNum: int
    fDescs: List[str]
    flowUsage: FlowUsage

    @classmethod
    def from_flow_info(cls, flow_info: FlowInfo) -> "MediaSubComponent":
        """mapping the FlowInfo{flowId and flowDescription} to MediaSubComponent{fnum, fDescs}"""
        return cls(
            fNum=flow_info.flowId,
            fDescs=flow_info.flowDescriptions or [],
            flowUsage=FlowUsage.NO_INFO  # Default value
        )



class FlowStatus(str, Enum):
    """Enumeration for FlowStatus as per 3GPP TS 29.514 Table 5.6.3.12-1"""
    ENABLED_UPLINK = "ENABLED-UPLINK"      # Enable uplink SDF(s), disable downlink SDF(s)
    ENABLED_DOWNLINK = "ENABLED-DOWNLINK"  # Enable downlink SDF(s), disable uplink SDF(s)
    ENABLED = "ENABLED"                    # Enable all SDF(s) in both directions
    DISABLED = "DISABLED"                  # Disable all SDF(s) in both directions
    REMOVED = "REMOVED"                    # Remove all SDF(s) and their IP filters

class MediaComponent(BaseModel):
    medCompN: int  # Identifies the media component number (ordinal number of the media component)
    fStatus: FlowStatus  # Indicates the status of the media component
    medSubComps: dict[str, MediaSubComponent]  # Map of flow number to MediaSubComponent
    medType: MediaType  # Indicates the media type of the service
    marBwUl: BitRate
    marBwDl: BitRate

#TODO check if bitrate is like 90000000 or 90 Mbps in open5gs

    @field_validator('marBwUl', 'marBwDl')
    @classmethod
    def validate_bitrate(cls, v):
        BITRATE_REGEX = re.compile(r'^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$')
        if not isinstance(v, str):
            raise TypeError('BitRate must be a string')
        if not BITRATE_REGEX.match(v):
            raise ValueError(
                "BitRate must match pattern: '^\\d+(\\.\\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$'"
            )
        return v

class AppSessionContextReqData(BaseModel):
    medComponents: dict[str, MediaComponent]
    notifUri: HttpUrl  # Notification URI for Application Session Context termination requests.
    suppFeat: Optional[str] = None
    ueIpv4: Optional[IPvAnyAddress] = None

    @classmethod
    def from_subscription(
        cls,
        from_subscription: AsSessionWithQosSubscription,
        medComponents: dict[str, MediaComponent],
        notifUri: HttpUrl
    ) -> "AppSessionContextReqData":
        
        """Create AppSessionContextReqData from subscription mapping values suppfeat and ipv4, with explicit medComponents and notifUri."""
        return cls(
            ueIpv4=from_subscription.ueIpv4Addr,
            suppFeat=from_subscription.supportedFeatures,
            medComponents=medComponents,
            notifUri=notifUri
        )


class AppSessionContext(BaseModel):
    """This Class is used to define the AppSessionContextReqData"""
    ascReqData: AppSessionContextReqData # Contains the information for the creation of a new Individual Application Session Context resource.

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ascReqData": {
                        "ueIpv4": "10.45.0.4",
                        "notifUri": "http://nef:8081/notifications/your-internal-session-id",
                        "suppFeat": "12",
                        "medComponents": {
                            "1": {
                                "medCompN": 1,
                                "fStatus": "ENABLED",
                                "medType": "VIDEO",
                                "marBwDl": "90000000",
                                "marBwUl": "6000000",
                                "medSubComps": {
                                    "3": {
                                        "fNum": 3,
                                        "fDescs": [
                                            "permit in ip from 10.45.0.4 to any",
                                            "permit out ip from any to 10.45.0.4"
                                        ],
                                        "flowUsage": "NO_INFO"
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
    }