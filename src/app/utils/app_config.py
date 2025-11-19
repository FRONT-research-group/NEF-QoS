import os
import json


PCF_BASE_URL = os.getenv("PCF_BASE_URL", "10.220.2.73")
PCF_PORT = int(os.getenv("PCF_PORT", 8086))




QOS_MAPPING = json.loads(os.getenv("QOS_MAPPING", json.dumps({
    ## NON-GBR up to UL/DL each profile is configured* example QOS_M max 8 Mbps UL/DL but can be less depending on network conditions
    
    
    #NOTE not working cause of DNN=internet, CONTROL is for ims
    #"qod_1": {"marBwDl": "120 Mbps", "marBwUl": "120 Mbps", "mediaType": "CONTROL"}, 
   
   
    "QOS_E": {"marBwDl": "1 Mbps", "marBwUl": "1 Mbps", "mediaType": "VIDEO"},
    "QOS_L": {"marBwDl": "20 Mbps", "marBwUl": "20 Mbps", "mediaType": "AUDIO"},
    "QOS_M": {"marBwDl": "8 Mbps", "marBwUl": "8 Mbps", "mediaType": "VIDEO"},
    "QOS_S": {"marBwDl": "4 Mbps", "marBwUl": "4 Mbps", "mediaType": "VIDEO"},
    
    
})))