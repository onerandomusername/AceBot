from __future__ import annotations

import enum
from datetime import datetime, timedelta
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class SecurityAction(enum.Enum):
    TIMEOUT = enum.auto()
    KICK = enum.auto()
    BAN = enum.auto()


class ModConfig(MappedAsDataclass, Base):
    __tablename__ = "mod_config"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="mod_config_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    spam_count: Mapped[int] = mapped_column(
        sa.SmallInteger(), nullable=False, server_default=sa.text("8")
    )
    spam_per: Mapped[int] = mapped_column(
        sa.SmallInteger(), nullable=False, server_default=sa.text("10")
    )
    mention_count: Mapped[int] = mapped_column(
        sa.SmallInteger(), nullable=False, server_default=sa.text("8")
    )
    mention_per: Mapped[int] = mapped_column(
        sa.SmallInteger(), nullable=False, server_default=sa.text("16")
    )
    raid: Mapped[bool] = mapped_column(
        nullable=False, default=False, server_default=sa.text("false")
    )
    raid_default_avatar: Mapped[bool] = mapped_column(
        nullable=False, default=False, server_default=sa.text("false")
    )
    log_channel_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger(), default=None)
    mute_role_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger(), default=None)
    spam_action: Mapped[Optional[str]] = mapped_column(
        sa.Enum(SecurityAction, name="security_action"), default=None
    )
    mention_action: Mapped[Optional[str]] = mapped_column(
        sa.Enum(SecurityAction, name="security_action"), default=None
    )
    raid_age: Mapped[Optional[timedelta]] = mapped_column(INTERVAL, default=None)


class ModEventType(enum.Enum):
    TIMEOUT = enum.auto()
    BAN = enum.auto()


class ModTimer(MappedAsDataclass, Base):
    __tablename__ = "mod_timer"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    event: Mapped[str] = mapped_column(sa.Enum(ModEventType, name="mod_event_type"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(nullable=False, server_default=sa.text("false"))
    mod_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger)
    duration: Mapped[Optional[timedelta]] = mapped_column(INTERVAL, default=None)
    reason: Mapped[Optional[str]] = mapped_column(sa.Text, default=None)
    userdata: Mapped[Optional[dict]] = mapped_column(sa.JSON, default=None)
