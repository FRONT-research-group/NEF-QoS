from app.schemas.qos_models import AsSessionWithQosSubscriptionWithSubscriptionId
from typing import List, Dict

# In-memory store for subscriptions
SUBSCRIPTION_STORE: Dict[str, List[AsSessionWithQosSubscriptionWithSubscriptionId]] = {}

def in_memory_db():
    # Code here for real database 
    return SUBSCRIPTION_STORE