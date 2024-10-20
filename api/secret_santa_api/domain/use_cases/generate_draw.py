import random
from typing import List, Optional

from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.ports.draw import DrawRepositoryPort
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort


class GenerateDraw:
    def __init__(
        self,
        participant_repository_port: ParticipantRepositoryPort,
        draw_repository_port: DrawRepositoryPort,
        retry_factor: int,
    ) -> None:
        self.participant_repository_port = participant_repository_port
        self.draw_repository_port = draw_repository_port
        self.retry_factor = retry_factor

    def perform(self) -> Optional[Draw]:
        participants = self.participant_repository_port.get_all_participants()

        if len(participants) < 2:
            return None

        for _i in range(len(participants) * self.retry_factor):
            try:
                draw = self.make_draw(participants)
                return self.draw_repository_port.save(draw)
            except ValueError:
                print("Could not make a draw, trying another attempt")

        return None

    def make_draw(
        self, participants: List[Participant]
    ) -> List[tuple[Participant, Participant]]:
        random.shuffle(participants)

        draw_details = []
        already_drawn_receivers: set[Participant] = set()

        for gifter in participants:
            possible_gift_receivers = set(participants).copy()
            possible_gift_receivers.remove(gifter)
            possible_gift_receivers.difference_update(already_drawn_receivers)

            if not possible_gift_receivers:
                raise ValueError(
                    "No more receivers remaining for current gifter, draw is impossible"
                )

            receiver = random.choice(sorted(possible_gift_receivers))
            already_drawn_receivers.add(receiver)

            draw_details.append((gifter, receiver))

        return draw_details
