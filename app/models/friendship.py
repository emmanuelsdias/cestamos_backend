from sqlalchemy import Column, Integer, ForeignKey
from dal.database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    invitation_id = Column(Integer, primary_key=True, index=True)

    user_id1 = Column(Integer, ForeignKey("users.user_id"))
    user_id2 = Column(Integer, ForeignKey("users.user_id"))


class Friendship(Base):
    __tablename__ = "friendships"

    friendship_id = Column(Integer, primary_key=True, index=True)

    user_id1 = Column(Integer, ForeignKey("users.user_id"))
    user_id2 = Column(Integer, ForeignKey("users.user_id"))
