from __future__ import annotations

import enum
from datetime import datetime, timedelta
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Config(MappedAsDataclass, Base):
    __tablename__ = "config"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="config_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(nullable=False)
    prefix: Mapped[Optional[str]] = mapped_column(sa.String(8), default=None)
    mod_role_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger(), default=None)


class DocsEntry(MappedAsDataclass, Base):
    __tablename__ = "docs_entry"
    __table_args__ = sa.UniqueConstraint("link", name="docs_entry_link_key")

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(sa.Text, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(sa.Text(), insert_default=None)
    link: Mapped[Optional[str]] = mapped_column(sa.Text(), insert_default=None)
    page: Mapped[Optional[str]] = mapped_column(sa.Text(), insert_default=None)
    fragment: Mapped[Optional[str]] = mapped_column(sa.Text(), insert_default=None)

    docs_name: Mapped[List[DocsName]] = relationship(back_populates="docs")
    docs_syntax: Mapped[List[DocsSyntax]] = relationship(back_populates="docs")


class Facts(MappedAsDataclass, Base):
    __tablename__ = "facts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)


class HighlightLang(MappedAsDataclass, Base):
    __tablename__ = "highlight_lang"
    __table_args__ = (sa.UniqueConstraint("guild_id", "user_id", name="highlight_lang_guild_id_user_id_key"),)

    id: Mapped[int] = mapped_column(init=False)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False, server_default=sa.text("0"))
    lang: Mapped[str] = mapped_column(sa.String(32), nullable=False)


class HighlightMsg(MappedAsDataclass, Base):
    __tablename__ = "highlight_msg"

    id: Mapped[int] = mapped_column(sa.Integer(), init=False)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    channel_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    message_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)


class CommandType(enum.Enum):
    PREFIX = enum.auto()
    APPLICATION = enum.auto()


class Log(MappedAsDataclass, Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    channel_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    command: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    type: Mapped[str] = mapped_column(sa.Enum(CommandType, name="command_type"), nullable=False)


class SecurityAction(enum.Enum):
    TIMEOUT = enum.auto()
    KICK = enum.auto()
    BAN = enum.auto()


class ModConfig(MappedAsDataclass, Base):
    __tablename__ = "mod_config"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="mod_config_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    spam_count: Mapped[int] = mapped_column(sa.SmallInteger(), nullable=False, server_default=sa.text("8"))
    spam_per: Mapped[int] = mapped_column(sa.SmallInteger(), nullable=False, server_default=sa.text("10"))
    mention_count: Mapped[int] = mapped_column(sa.SmallInteger(), nullable=False, server_default=sa.text("8"))
    mention_per: Mapped[int] = mapped_column(sa.SmallInteger(), nullable=False, server_default=sa.text("16"))
    raid: Mapped[bool] = mapped_column(nullable=False, default=False, server_default=sa.text("false"))
    raid_default_avatar: Mapped[bool] = mapped_column(nullable=False, default=False, server_default=sa.text("false"))
    log_channel_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger(), default=None)
    mute_role_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger(), default=None)
    spam_action: Mapped[Optional[str]] = mapped_column(sa.Enum(SecurityAction, name="security_action"), default=None)
    mention_action: Mapped[Optional[str]] = mapped_column(sa.Enum(SecurityAction, name="security_action"), default=None)
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


class Remind(MappedAsDataclass, Base):
    __tablename__ = "remind"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    channel_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    made_on: Mapped[datetime] = mapped_column(nullable=False)
    remind_on: Mapped[datetime] = mapped_column(nullable=False)
    message_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, default=None)
    message: Mapped[Optional[str]] = mapped_column(sa.Text, default=None)


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


class Tag(MappedAsDataclass, Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    uses: Mapped[int] = mapped_column(nullable=False, server_default=sa.text("0"))
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(sa.String(2000), nullable=False)
    alias: Mapped[Optional[str]] = mapped_column(sa.String(32), default=None)
    edited_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    viewed_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class Trivia(MappedAsDataclass, Base):
    __tablename__ = "trivia"
    __table_args__ = (sa.UniqueConstraint("guild_id", "user_id", name="trivia_guild_id_user_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    correct_count: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default=sa.text("0"))
    wrong_count: Mapped[int] = mapped_column(sa.Integer, nullable=False, server_default=sa.text("0"))
    score: Mapped[int] = mapped_column(sa.BigInteger, nullable=False, server_default=sa.text("0"))


class TriviaStats(MappedAsDataclass, Base):
    __tablename__ = "trivia_stats"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    question_hash: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    result: Mapped[bool] = mapped_column(nullable=False)


class Welcome(MappedAsDataclass, Base):
    __tablename__ = "welcome"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="welcome_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    enabled: Mapped[bool] = mapped_column(nullable=False, server_default=sa.text("true"))
    channel_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, default=None)
    content: Mapped[Optional[str]] = mapped_column(sa.String(1024), default=None)


class DocsName(MappedAsDataclass, Base):
    __tablename__ = "docs_name"
    __table_args__ = (
        sa.ForeignKeyConstraint(["docs_id"], ["docs_entry.id"], name="docs_name_docs_id_fkey"),
        sa.UniqueConstraint("name", name="docs_name_name_key"),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    docs_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)

    docs: Mapped[Optional[DocsEntry]] = relationship(back_populates="docs_name")


class DocsSyntax(MappedAsDataclass, Base):
    __tablename__ = "docs_syntax"
    __table_args__ = (sa.ForeignKeyConstraint(["docs_id"], ["docs_entry.id"], name="docs_syntax_docs_id_fkey"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    docs_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    syntax: Mapped[str] = mapped_column(sa.Text, nullable=False)

    docs: Mapped[Optional[DocsEntry]] = relationship(back_populates="docs_syntax", default=None)


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
