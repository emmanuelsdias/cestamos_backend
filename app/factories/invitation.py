from fastapi import Depends

from app.dal.user import ABCUserDal
from app.dal.invitation import ABCInvitationDal
from app.factories.dal_factories import get_user_dal, get_invitation_dal
from app.services.invitation import ABCInvitationService, InvitationService


def get_invitation_service(
    invitation_dal: ABCInvitationDal = Depends(get_invitation_dal),
    user_dal: ABCUserDal = Depends(get_user_dal)
) -> ABCInvitationService:
    client = InvitationService(invitation_dal, user_dal)
    try:
        yield client
    finally:
        pass