from typing import List
from dto.output_dto import OutputBaseModel


class Friendship(OutputBaseModel):
    friendship_id: int

    user_id: int
    username: str
