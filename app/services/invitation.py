import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from dal.invitation import ABCInvitationDal
from dal.friendship import ABCFriendshipDal
from dal.user import ABCUserDal

from dto.invitation import Invitation, InvitationCreate

from models.friendship import Invitation as InvitationModel, Friendship as FriendshipModel
from models.user import User as UserModel

from services.user_based_service import UserBasedService

from typing import List


class ABCInvitationService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_invitations(self, token) -> List[Invitation]:
        """ Returns invitations from user """
    
    @abc.abstractmethod
    def get_invitation_by_id(self, invitation_id) -> Invitation:
        """ Return the invitation with given id """

    @abc.abstractmethod
    def create_invitation(self, invitation: InvitationCreate, token: str) -> Invitation:
        """ Create a invitation """

    @abc.abstractmethod
    def delete_invitation(self, invitation_id: int, token: str, accepted: bool) -> Invitation:
        """ Delete a invitation """


class InvitationService(ABCInvitationService):

    def __init__(
        self,
        user_dal: ABCUserDal,
        invitation_dal: ABCInvitationDal,
        friendship_dal: ABCFriendshipDal,
    ):
        super().__init__(user_dal)
        self.dal = invitation_dal
        self.friendship_dal = friendship_dal

    def check_invitation_validity(self, invitation_id, user):
        invitation = self.dal.get_invitation_by_id(invitation_id)
        if invitation is None:
            raise HTTPException(
                status_code=400, detail="Invitation doesn't exist"
            )
        if not (user.user_id in [invitation.user_id1, invitation.user_id2]):
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        return invitation


    def construct_invitation_dto(self, invitation: InvitationModel) -> Invitation:
        user1 = self.user_dal.get_user_by_id(invitation.user_id1)
        user2 = self.user_dal.get_user_by_id(invitation.user_id2)
        invitation_dto = Invitation(
            invitation_id = invitation.invitation_id,
            user_id1 = user1.user_id,
            username1 = user1.username,
            user_id2 = user2.user_id,
            username2 = user2.username,
        )
        return invitation_dto


    def get_invitations(self, token) -> List[Invitation]:
        user = self.check_user_validity(token)
        invitations = self.dal.get_invitations_from_user(user.user_id)
        invitations_res = [self.construct_invitation_dto(invitation) for invitation in invitations]
        return invitations_res

    def get_invitation_by_id(self, invitation_id: int, token: str) -> Invitation:
        user = self.check_user_validity(token)

        invitation = self.check_invitation_validity(invitation_id, user)
        return self.construct_invitation_dto(invitation)

    def create_invitation(self, invitation: InvitationCreate, token: str) -> Invitation:
        user = self.check_user_validity(token)
        invited_user = self.user_dal.get_user_by_id(invitation.user_id)
        if invited_user is None:
            raise HTTPException(
                status_code=400, detail="Invited user doesn't exist"
            )
        if user.user_id == invitation.user_id:
            raise HTTPException(
                status_code=400, detail="Can't invite yourself"
            )
        if self.dal.get_invitation_from_pair(user.user_id, invitation.user_id) is not None:
            raise HTTPException(
                status_code=400, detail="Invitation already exists"
            )
        if self.friendship_dal.get_friendship_from_user_pair(user.user_id, invited_user.user_id) is not None:
            raise HTTPException(
                status_code=400, detail="Friendship already exists"
            )
        
        db_invitation = InvitationModel(
            user_id1=user.user_id,
            user_id2=invitation.user_id
        )

        created_invitation = self.dal.create_invitation(invitation=db_invitation)
        invitation_response = self.construct_invitation_dto(created_invitation)
        return invitation_response
    
    
    def delete_invitation(self, invitation_id: int, token: str, accepted: bool) -> Invitation:
        user = self.check_user_validity(token)
        invitation = self.check_invitation_validity(invitation_id, user)
        if user.user_id == invitation.user_id2:
            if accepted is None:
                raise HTTPException(
                    status_code=400, detail="missing accepted flag"
                )
            if accepted:
                new_friendship = FriendshipModel(
                    user_id1 = invitation.user_id1,
                    user_id2 = invitation.user_id2
                )
                self.friendship_dal.create_friendship(new_friendship)
        
        deleted_invitation = self.dal.delete_invitation(invitation_id)
        return self.construct_invitation_dto(deleted_invitation)