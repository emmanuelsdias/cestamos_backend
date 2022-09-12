from typing import List
from pydantic import BaseModel
from app.dto.output_dto import OutputBaseModel

class InvitationCreate(BaseModel):
    user_id: int

class Invitation(OutputBaseModel):
    invitation_id: int
    user_id1: int
    username1: str
    user_id2: int
    username2: str
    