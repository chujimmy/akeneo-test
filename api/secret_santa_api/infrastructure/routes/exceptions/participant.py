from typing import Optional

from werkzeug.exceptions import BadRequest


class ApiAddParticipantPayloadBadRequest(BadRequest):
    description = "Invalid payload for add particiant request"
    error_code = "add_participant_payload_bad_request"

    def __init__(self, messages: Optional[dict] = None) -> None:
        super().__init__()
        self.messages = messages
