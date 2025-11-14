import os
import json

NEF_BASE_URL = os.getenv("NEF_BASE_URL", "http://localhost:8002")
PCF_BASE_URL = os.getenv("PCF_BASE_URL", "10.220.2.73")
PCF_PORT = int(os.getenv("PCF_PORT", 8086))




QOS_MAPPING = json.loads(os.getenv("QOS_MAPPING", json.dumps({
    "qod_1": {"marBwDl": "120 Mbps", "marBwUl": "120 Mbps", "mediaType": "CONTROL"}, #NOTE not working cause of DNN=internet, CONTROL is for ims
    "qod_2": {"marBwDl": "20 Mbps", "marBwUl": "20 Mbps", "mediaType": "AUDIO"},
    "qod_3": {"marBwDl": "40 Mbps", "marBwUl": "40 Mbps", "mediaType": "VIDEO"},
    "qod_4": {"marBwDl": "80 Mbps", "marBwUl": "80 Mbps", "mediaType": "VIDEO"},
    "qod_test": {"marBwDl": "10 Mbps", "marBwUl": "2 Mbps", "mediaType": "AUDIO"}
    
})))