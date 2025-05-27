import socket
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded
import json
# requests to open5gs using sockets, cause requests doesn't support http2 without TLS


def delete_request():
    """
    Sends a DELETE request to pcf using HTTP/2 over a socket connection.
    """
    host = '10.220.2.73'
    port = 8086
    path = '/npcf-policyauthorization/v1/app-sessions/166/delete'

    sock = socket.create_connection((host, port))
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    stream_id = conn.get_next_available_stream_id()
    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':method', 'POST'),
            (':authority', host),
            (':scheme', 'http'),
            (':path', path),
            ('content-length', '0'),
        ],
        end_stream=True,
    )
    sock.sendall(conn.data_to_send())

    response_ended = False

    while not response_ended:
        data = sock.recv(65535)
        if not data:
            break

        events = conn.receive_data(data)
        for event in events:
            if isinstance(event, ResponseReceived):
                print("Response headers:", event.headers)
            elif isinstance(event, DataReceived):
                print("Response body:", event.data.decode())
            elif isinstance(event, StreamEnded):
                response_ended = True

        sock.sendall(conn.data_to_send())

    sock.close()

def post_request():
    """
    Sends a POST request to pcf using HTTP/2 over a socket connection.
    """
    host = '10.220.2.73'
    port = 8086
    path = '/npcf-policyauthorization/v1/app-sessions'

    # JSON payload
    payload = {
        "notificationDestination": "http://localhost:9091/3gpp-as-session-with-qos/v1/notifications",
        "supportedFeatures": "003C",
        "exterAppId": "externalApp-123",
        "qosReference": "qod_2",
        "ueIpv4Addr": "10.45.0.3",
        "flowInfo": [
            {
                "flowId": 1,
                "flowDescriptions": [
                    "permit in ip from 10.45.0.3 0-65535 to 10.45.0.2 0-65535",
                    "permit out ip from 10.45.0.2 0-65535 to 10.45.0.3 0-65535"
                ]
            }
        ],
        "requestTestNotification": True
    }
    body = json.dumps(payload).encode("utf-8")

    # Open socket connection
    sock = socket.create_connection((host, port))
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    # Send POST headers
    stream_id = conn.get_next_available_stream_id()
    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':method', 'POST'),
            (':authority', host),
            (':scheme', 'http'),
            (':path', path),
            ('content-type', 'application/json'),
            ('accept', 'application/json'),
            ('content-length', str(len(body))),
        ]
    )
    conn.send_data(stream_id, body, end_stream=True)
    sock.sendall(conn.data_to_send())

    # Receive response
    response_ended = False
    while not response_ended:
        data = sock.recv(65535)
        if not data:
            break

        events = conn.receive_data(data)
        for event in events:
            if isinstance(event, ResponseReceived):
                print("Response headers:", event.headers)
            elif isinstance(event, DataReceived):
                print("Response body:", event.data.decode())
            elif isinstance(event, StreamEnded):
                response_ended = True

        sock.sendall(conn.data_to_send())

    sock.close()