from __future__ import annotations

from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


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
