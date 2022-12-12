import json, enum
import boto3

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = "cf8432060222b9c1df60ae6cf416b7994002ffb025a6198390580bc9c2424dd7"

class ResponseTypes(enum.IntEnum):
    PONG = 1
    ACK_NO_SOURCE = 2
    MESSAGE_NO_SOURCE = 3
    MESSAGE_WITH_SOURCE = 4
    ACK_WITH_SOURCE = 5

class ResponseData():
    def __init__(
        self, 
        tts: bool = False,
        content: str = "",
        embeds: list = [],
        allowed_mentions: list = []
    ) -> None:
        self.tts = tts
        self.content = content
        self.embeds = embeds
        self.allowed_mentions = allowed_mentions

class Response():
    def __init__(
        self,
        type: ResponseTypes = ResponseTypes.MESSAGE_WITH_SOURCE,
        response_data: ResponseData = None
    ) -> None:
        self.type = type
        self.response_data = response_data

def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get("x-signature-ed25519")
    auth_ts = event['params']['header'].get("x-signature-timestamp")

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig))

def ping_pong(body):
    if body.get("type") == int(ResponseTypes.PONG):
        return True
    
    return False

def lambda_handler(event, context):
    print(f"event: {json.dumps(event)}")

    try:
        verify_signature(event)
    except Exception as e:
        print(f"Invalid request signature: {e}")
        return {
            "statusCode": 401
        }

    body: dict = json.loads(event.get("body"))
    
    if ping_pong(body):
        return json.dumps(Response(ResponseTypes.PONG))

    return {
        "statusCode": 404
    }