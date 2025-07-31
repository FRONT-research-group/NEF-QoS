#TODO insert the configuration here 
#TODO Open5gs core IP etc... 

import os
import json

NEF_BASE_URL = os.getenv("NEF_BASE_URL", "http://localhost:8081")
PCF_BASE_URL = os.getenv("PCF_BASE_URL", "10.220.2.73")
PCF_PORT = int(os.getenv("PCF_PORT", 8086))




QOS_MAPPING = json.loads(os.getenv("QOS_MAPPING", json.dumps({
    "qod_1": {"marBwDl": "120 Mbps", "marBwUl": "120 Mbps", "mediaType": "CONTROL"},
    "qod_2": {"marBwDl": "20 Mbps", "marBwUl": "20 Mbps", "mediaType": "AUDIO"},
    "qod_3": {"marBwDl": "40 Mbps", "marBwUl": "40 Mbps", "mediaType": "VIDEO"},
    "qod_4": {"marBwDl": "80 Mbps", "marBwUl": "80 Mbps", "mediaType": "VIDEO"}
})))