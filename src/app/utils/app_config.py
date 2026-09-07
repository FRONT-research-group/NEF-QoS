import os
import json

NEF_BASE_URL = os.getenv("NEF_BASE_URL", "http://localhost:8585")
PCF_BASE_URL = os.getenv("PCF_BASE_URL", "10.220.2.50")
PCF_PORT = int(os.getenv("PCF_PORT", 8086))




QOS_MAPPING = json.loads(os.getenv("QOS_MAPPING", json.dumps({
    ## NON-GBR up to UL/DL each profile is configured* example QOS_M max 8 Mbps UL/DL but can be less depending on network conditions
    
    
    #NOTE not working cause of DNN=internet, CONTROL is for ims
    #"qod_1": {"marBwDl": "120 Mbps", "marBwUl": "120 Mbps", "mediaType": "CONTROL"}, 
   
  "QOS_E": {
  "marBwDl": "5 Mbps", 
  "marBwUl": "5 Mbps", 
  "mirBwDl": "2 Mbps", 
  "mirBwUl": "2 Mbps", 
  "mediaType": "VIDEO"
},
"QOS_L": {
  "marBwDl": "35 Mbps", 
  "marBwUl": "18 Mbps", 
  "mirBwDl": "25 Mbps", 
  "mirBwUl": "15 Mbps", 
  "mediaType": "VIDEO"
},
"QOS_M": {
  "marBwDl": "20 Mbps", 
  "marBwUl": "10 Mbps", 
  "mirBwDl": "15 Mbps", 
  "mirBwUl": "5 Mbps", 
  "mediaType": "VIDEO"
},
"QOS_S": {
  "marBwDl": "15 Mbps", 
  "marBwUl": "10 Mbps", 
  "mirBwDl": "10 Mbps", 
  "mirBwUl": "5 Mbps", 
  "mediaType": "VIDEO"
},
"QOS_GBR_CONSERVATIVE": {
  "marBwDl": "16 Mbps", 
  "marBwUl": "12 Mbps", 
  "mirBwDl": "14 Mbps", 
  "mirBwUl": "10 Mbps", 
  "mediaType": "VIDEO"
},
"QOS_GBR_MODERATE": {
  "marBwDl": "24 Mbps", 
  "marBwUl": "16 Mbps", 
  "mirBwDl": "20 Mbps", 
  "mirBwUl": "12 Mbps", 
  "mediaType": "VIDEO"
},
"QOS_GBR_AGGRESSIVE": {
  "marBwDl": "35 Mbps",
  "marBwUl": "24 Mbps",
  "mirBwDl": "25 Mbps",
  "mirBwUl": "18 Mbps",
  "mediaType": "VIDEO"
}
})))
