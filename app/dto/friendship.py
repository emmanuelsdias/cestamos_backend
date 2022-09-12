from typing import List
from app.dto.output_dto import OutputBaseModel



class Friendship(OutputBaseModel):
    friendship_id: int
    
    user_id1: int
    username1: str
    user_id2: int
    username2: str
