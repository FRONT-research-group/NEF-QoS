import json
import socket
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded
from app.utils.app_config import PCF_BASE_URL, PCF_PORT
from app.utils.log import get_app_logger

logger = get_app_logger()

def pcf_post_request(payload):
    path = '/npcf-policyauthorization/v1/app-sessions'
    body = json.dumps(payload).encode("utf-8")

    # Open TCP socket connection
    sock = socket.create_connection((PCF_BASE_URL, PCF_PORT))

    # Create and initiate HTTP/2 connection
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    # Send HTTP/2 headers
    stream_id = conn.get_next_available_stream_id()
    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':method', 'POST'),
            (':scheme', 'http'),
            (':authority', PCF_BASE_URL),
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
    session_id = None

    while not response_ended:
        data = sock.recv(65535)
        if not data:
            break

        events = conn.receive_data(data)
        for event in events:
            if isinstance(event, ResponseReceived):
                logger.info(f"Response headers: {event.headers}")
                for name, value in event.headers:
                    if name.lower() == b'location':
                        location_url = value.decode()
                        session_id = location_url.rstrip('/').split('/')[-1]
                        logger.info(f"Extracted App Session ID: {session_id}")
            elif isinstance(event, DataReceived):
                logger.info(f"Response body: {event.data.decode()}")
            elif isinstance(event, StreamEnded):
                response_ended = True

        sock.sendall(conn.data_to_send())

    sock.close()
    return session_id

if __name__ == "__main__":
    pcf_post_request()
