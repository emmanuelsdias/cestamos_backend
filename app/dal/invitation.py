import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update, or_, and_
# from sqlalchemy import and_, or_, not_

from models.friendship import Invitation

from typing import List

class ABCInvitationDal():

    @abc.abstractmethod
    def get_invitations(self) -> List[Invitation]:
        """Gets all invitations in database"""

    @abc.abstractmethod
    def get_invitations_from_user(self, user_id) -> List[Invitation]:
        """Gets all invitations in database from a user """

    @abc.abstractmethod
    def get_invitation_from_pair(self, user_id1: int, user_id2: int) -> Invitation:
        """Gets invitation in database from a pair of users """

    @abc.abstractmethod
    def get_invitation_by_id(self, invitation_id: int) -> Invitation:
        """Gets the invitation in database with the given id"""

    @abc.abstractmethod
    def create_invitation(self, invitation: Invitation) -> Invitation:
        """Creates a new invitation in database"""

    @abc.abstractmethod
    def delete_invitation(self, invitation_id: int) -> Invitation:
        """ Deletes a invitation in database """


class InvitationDal(ABCInvitationDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_invitations(self) -> List[Invitation]:
        return self.db.query(Invitation).all()

    def get_invitations_from_user(self, user_id) -> List[Invitation]:
        return self.db.query(Invitation).filter(or_(
            Invitation.user_id1 == user_id,
            Invitation.user_id2 == user_id
            )).all()

    def get_invitation_from_pair(self, user_id1: int, user_id2: int) -> Invitation:
        return self.db.query(Invitation).filter(or_(
            and_(
                Invitation.user_id1 == user_id1,
                Invitation.user_id2 == user_id2
                ),
            and_(
                Invitation.user_id1 == user_id2,
                Invitation.user_id2 == user_id1
            )
            )).first()

    def get_invitation_by_id(self, invitation_id: int) -> Invitation:
        return self.db.query(Invitation).filter(Invitation.invitation_id == invitation_id).first()

    def create_invitation(self, invitation: Invitation) -> Invitation:
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation

    def delete_invitation(self, invitation_id: int) -> Invitation:
        deleted_invitation = self.get_invitation_by_id(invitation_id)

        self.db.query(Invitation).filter(Invitation.invitation_id == invitation_id).\
            delete()
       
        self.db.commit()
        return deleted_invitation