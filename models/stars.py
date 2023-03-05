from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from models.base import Base


class StarMsg(MappedAsDataclass, Base):
    __tablename__ = "star_msg"
    __table_args__ = (sa.UniqueConstraint("message_id", name="star_msg_message_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    channel_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    message_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    starred_at: Mapped[datetime] = mapped_column(nullable=False)
    starrer_id: Mapped[int] = mapped_column(nullable=False)
    starrers: Mapped[List[Starrers]] = relationship(back_populates="star")
    star_message_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, default=None)


class Starboard(MappedAsDataclass, Base):
    __tablename__ = "starboard"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="starboard_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    locked: Mapped[bool] = mapped_column(nullable=False, server_default=sa.text("false"))
    channel_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, default=None)
    threshold: Mapped[Optional[int]] = mapped_column(sa.SmallInteger, default=None)
    minimum: Mapped[Optional[int]] = mapped_column(sa.SmallInteger, default=None)


class Starrers(MappedAsDataclass, Base):
    __tablename__ = "starrers"
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ["star_id"],
            ["star_msg.id"],
            ondelete="CASCADE",
            name="starrers_star_id_fkey",
        ),
        sa.UniqueConstraint("star_id", "user_id", name="starrers_star_id_user_id_key"),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    star_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)

    star: Mapped[Optional[StarMsg]] = relationship(back_populates="starrers", default=None)
