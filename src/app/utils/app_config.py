import os
import json

NEF_BASE_URL = os.getenv("NEF_BASE_URL", "http://localhost:8002")
PCF_BASE_URL = os.getenv("PCF_BASE_URL", "10.220.2.73")
PCF_PORT = int(os.getenv("PCF_PORT", 8086))




QOS_MAPPING = json.loads(os.getenv("QOS_MAPPING", json.dumps({
    ## NON-GBR up to UL/DL each profile is configured* example qod_4 max 80Mbps UL/DL but can be less depending on network conditions
    
    "qod_1": {"marBwDl": "120 Mbps", "marBwUl": "120 Mbps", "mediaType": "CONTROL"}, #NOTE not working cause of DNN=internet, CONTROL is for ims
    "QOS_E": {"marBwDl": "1 Mbps", "marBwUl": "1 Mbps", "mediaType": "VIDEO"},
    "QOS_L": {"marBwDl": "20 Mbps", "marBwUl": "20 Mbps", "mediaType": "AUDIO"},
    "QOS_M": {"marBwDl": "8 Mbps", "marBwUl": "8 Mbps", "mediaType": "VIDEO"},
    "QOS_S": {"marBwDl": "4 Mbps", "marBwUl": "4 Mbps", "mediaType": "VIDEO"},
    
    "qod_test": {"marBwDl": "10 Mbps", "marBwUl": "2 Mbps", "mediaType": "AUDIO"}
    
})))