## 3GPP Data Types for Northbound APIs
 **3GPP Reference**:
  [3GPP TS 29.122 - page 310](https://www.etsi.org/deliver/etsi_ts/129100_129199/129122/17.05.00_60/ts_129122v170500p.pdf)

### `notificationDestination`

* **Type**: `URI`
* **Description**:
  Specifies the **Uniform Resource Locator (URL)** to which the **Service Capability Exposure Function (SCEF)** sends notifications for bearer-level events.
  These events may include:

  * Establishment of a bearer
  * Modification of a bearer
  * Release of a bearer
    The URL provided allows the receiving application or service to asynchronously handle updates about bearer events in the network.
* **Usage Context**:
  The `notificationDestination` is typically provided by an application server or network function that subscribes to the notification service. It enables the SCEF to deliver notifications reliably and securely to the correct destination.



### `supportedFeatures`

* **Type**: `Optional[str]`
* **Description**:
  Identifies the **features supported** by the requester, expressed as a feature tag string. Enables negotiation of capabilities between the requesting and serving entities.

  The string represents a **hexadecimal bitmask**, where each character corresponds to 4 features (bits) in the API specification. The leftmost character represents the highest-numbered features, and the rightmost represents features 1–4. For example, "1F" indicates support for features 5–8 and 1–4. This mechanism ensures that the requester and the server only use features they both support, maintaining compatibility and flexibility across different 3GPP 5G APIs.

* **3GPP Swagger Reference**:
  - See the [TS29571_CommonData.yaml](TS-schemas/TS29571_CommonData.yaml) file for the OpenAPI schema definition of the `SupportedFeatures` data type used in 3GPP APIs.

### `qosReference`

* **Type**: `Optional[str]`
* **Description**:
  Represents a **reference to a specific QoS (Quality of Service)** configuration applicable to the bearer or flow.  
  Enables tracking and correlation of pre-configured QoS settings between network elements.


* **3GPP Swagger Reference**:
  - See the [TS29122_AsSessionWithQoS.yaml](TS-schemas/TS29122_AsSessionWithQoS.yaml) file for the OpenAPI schema definition of `qosReference`.


### `ueIpv4Addr`

* **Type**: `Optional[IPvAnyAddress]`
* **Description**:
  Specifies the **IPv4 address of the User Equipment (UE)**, used for uniquely identifying the subscriber’s IP address within the network.

### `flowInfo`

* **Type**: `Optional[List[FlowInfo]]`
* **Description**:
  An array of **FlowInfo** objects that describe IP flow information for the bearer or session.

  **Each `FlowInfo` object contains:**
  - `flowId` (`integer`):  
    Uniquely identifies the IP flow.
  - `flowDescriptions` (`array of string`, `0..2`):  
    Defines the packet filters of the IP flow, encoded according to [3GPP TS 29.214 clause 5.3.8](https://www.etsi.org/deliver/etsi_ts/129200_129299/129214/17.04.00_60/ts_129214v170400p.pdf).  
    Can include UL (uplink) and/or DL (downlink) IP flow descriptions.

  **Inclusion rules**:
  - One of `ueIpv4Addr`, `ueIpv6Addr`, or `macAddr` **shall be included**.
  - If `ueIpv4Addr` or `ueIpv6Addr` is provided, **IP flow information** (`flowInfo`) must also be provided.
  - See `flowInfo` data type for further schema details.

* **3GPP Swagger Reference**:
  - See the [TS29122_CommonData.yaml](TS-schemas/TS29122_CommonData.yaml) file for the OpenAPI schema definition of `FlowInfo`.

* **3GPP Reference**:
  - [3GPP TS 29.122 - FlowInfo Data Type (Table 5.2.1.2.8-1)](https://www.etsi.org/deliver/etsi_ts/129100_129199/129122/17.12.00_60/ts_129122v171200p.pdf)


### `requestTestNotification`

* **Type**: `Optional[bool]`
* **Default**: `True`
* **Description**:
  Indicates whether a **test notification** is requested by the subscriber or network entity.

  * `True`: Requesting test notifications to validate the delivery path.
  * `False`: No test notification requested.


