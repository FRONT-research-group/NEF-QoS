# NEF for Open5GS PCF

This project demonstrates the use of the **Network Exposure Function (NEF)** to interact with **Open5GS Policy Control Function (PCF)** and apply **Policy and Charging Control (PCC)** rules to manage **5G QoS (5Qi)** flows for specific subscriber sessions.

## Purpose

* **NEF** interacts with **Open5GS PCF** to:

  * Apply **PCC rules** on a specific subscription.
  * Configure **5Qi-based QoS flows** for **uplink and downlink traffic**.

## Example QoS Flow

The following parameters define a sample **QoS flow**:

* **Downlink**: 60 Mbps
* **Uplink**: 20 Mbps
* **5Qi**: Specific to the application or traffic type, e.g., conversational voice, streaming video.

This configuration ensures that the network can handle different traffic types with guaranteed quality and bandwidth.

## How It Works

1. **Application Server (AS)** sends a request via the **Northbound APIs** to the **NEF**.
2. **NEF** forwards the policy request to the **Southbound APIs**, communicating with **Open5GS PCF**.
3. **Open5GS PCF** enforces the **PCC rules** on the subscriber session.
4. The subscriber (**UE**) experiences the applied **QoS flow** as defined (e.g., **60 Mbps Downlink, 20 Mbps Uplink**).

**Note:**  The following topology provides a conceptual overview of the flow. It does not reflect the actual flow.

![NEF QoS Flow](images/NEF-qos.png)
