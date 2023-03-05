from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class Welcome(MappedAsDataclass, Base):
    __tablename__ = "welcome"
    __table_args__ = (sa.UniqueConstraint("guild_id", name="welcome_guild_id_key"),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    enabled: Mapped[bool] = mapped_column(nullable=False, server_default=sa.text("true"))
    channel_id: Mapped[Optional[int]] = mapped_column(sa.BigInteger, default=None)
    content: Mapped[Optional[str]] = mapped_column(sa.String(1024), default=None)
