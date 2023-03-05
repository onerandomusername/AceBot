from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class HighlightLang(MappedAsDataclass, Base):
    __tablename__ = "highlight_lang"
    __table_args__ = (
        sa.UniqueConstraint("guild_id", "user_id", name="highlight_lang_guild_id_user_id_key"),
    )

    id: Mapped[int] = mapped_column(init=False)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger(), nullable=False, server_default=sa.text("0")
    )
    lang: Mapped[str] = mapped_column(sa.String(32), nullable=False)


class HighlightMsg(MappedAsDataclass, Base):
    __tablename__ = "highlight_msg"

    id: Mapped[int] = mapped_column(sa.Integer(), init=False)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    channel_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
    message_id: Mapped[int] = mapped_column(sa.BigInteger(), nullable=False)
