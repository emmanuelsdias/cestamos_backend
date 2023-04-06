from fastapi import Depends

from dal.user import ABCUserDal
from dal.invitation import ABCInvitationDal
from dal.friendship import ABCFriendshipDal
from factories.dal_factories import get_user_dal, get_invitation_dal, get_friendship_dal
from services.invitation import ABCInvitationService, InvitationService


def get_invitation_service(
    user_dal: ABCUserDal = Depends(get_user_dal),
    invitation_dal: ABCInvitationDal = Depends(get_invitation_dal),
    friendship_dal: ABCFriendshipDal = Depends(get_friendship_dal),
) -> ABCInvitationService:
    client = InvitationService(user_dal, invitation_dal, friendship_dal)
    try:
        yield client
    finally:
        pass