from botovod.dbdrivers.gino import db, Follower

from .mixins import CommonMixin
from .types import StateEnum


class FollowerState(CommonMixin, db.Model):
    __tablename__ = "follower_states"

    follower_id = db.Column(db.Integer,
                            db.ForeignKey(f"{Follower.__tablename__}.id", ondelete="CASCADE"),
                            nullable=False, unique=True, index=True)
    state = db.Column(db.Enum(StateEnum), nullable=False, default=StateEnum.START)
    data = db.Column(db.Unicode, nullable=False, default="{}")
