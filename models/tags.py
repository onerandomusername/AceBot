from __future__ import annotations

from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


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
