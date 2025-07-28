import socket
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded
from app.utils.app_config import PCF_BASE_URL, PCF_PORT


def pcf_delete_request(session_id):
    host = '10.220.2.73'
    port = 8086
    path = (f'/npcf-policyauthorization/v1/app-sessions/{session_id}/delete')  # Replace with correct session ID

    sock = socket.create_connection((host, port))
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    stream_id = conn.get_next_available_stream_id()
    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':method', 'POST'),
            (':scheme', 'http'),
            (':authority', f'{PCF_BASE_URL}:{PCF_PORT}'),
            (':path', path),
            ('accept', 'application/json'),
            ('content-length', '0'),
        ],
        end_stream=True  # No body
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
                print("🔹 Response headers:", event.headers)
            elif isinstance(event, DataReceived):
                print("🔹 Response body:", event.data.decode())
            elif isinstance(event, StreamEnded):
                response_ended = True

        sock.sendall(conn.data_to_send())

    sock.close()

