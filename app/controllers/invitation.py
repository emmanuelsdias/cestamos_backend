from fastapi import APIRouter
from fastapi import Depends

from services.invitation import ABCInvitationService
from factories.invitation import get_invitation_service

from dto.invitation import Invitation, InvitationCreate
from typing import List


router = APIRouter()

@router.get("/", response_model=List[Invitation])
async def get_invitations(
    token: str = None,
    invitation_service: ABCInvitationService = Depends(get_invitation_service)
):
    return invitation_service.get_invitations(token)

@router.post("/", response_model=Invitation)
async def create_invitation(
    invitation: InvitationCreate,
    token: str = None,
    invitation_service: ABCInvitationService = Depends(get_invitation_service)
):
    return invitation_service.create_invitation(invitation, token)

@router.get("/{invitation_id}", response_model=Invitation)
async def get_invitation_by_id(
    invitation_id: int,
    token: str = None,
    invitation_service: ABCInvitationService = Depends(get_invitation_service)
):
    return invitation_service.get_invitation_by_id(invitation_id, token)


@router.delete("/{invitation_id}", response_model=Invitation)
async def delete_invitation(
    invitation_id: int,
    token: str = None,
    accepted: bool = None,
    invitation_service: ABCInvitationService = Depends(get_invitation_service)
):
    return invitation_service.delete_invitation(invitation_id, token, accepted)