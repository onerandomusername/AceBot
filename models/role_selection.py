from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class Role(MappedAsDataclass, Base):
    __tablename__ = "role"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="role_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    message_ids: Mapped[List[int]] = mapped_column(
        sa.ARRAY(sa.BigInteger()),
        nullable=False,
        server_default=sa.text("ARRAY[]::bigint[]"),
    )
    selectors: Mapped[List[int]] = mapped_column(
        sa.ARRAY(sa.Integer()),
        nullable=False,
        server_default=sa.text("ARRAY[]::integer[]"),
    )
    channel_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, default=None)


class RoleEntry(MappedAsDataclass, Base):
    __tablename__ = "role_entry"
    __table_args__ = (sa.UniqueConstraint("role_id", name="role_entry_role_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    emoji: Mapped[str] = mapped_column(sa.String(56), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(199), nullable=False)
    description: Mapped[str] = mapped_column(sa.String(1024), nullable=False)


class RoleSelector(MappedAsDataclass, Base):
    __tablename__ = "role_selector"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    title: Mapped[str] = mapped_column(sa.String(256), nullable=False)
    inline: Mapped[bool] = mapped_column(nullable=False, server_default=sa.text("true"))
    roles: Mapped[List[int]] = mapped_column(
        sa.ARRAY(sa.Integer()),
        nullable=False,
        server_default=sa.text("ARRAY[]::integer[]"),
    )
    description: Mapped[Optional[str]] = mapped_column(sa.String(1024), default=None)
    icon: Mapped[Optional[str]] = mapped_column(sa.String(256), default=None)
