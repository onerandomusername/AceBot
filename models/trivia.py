from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class Trivia(MappedAsDataclass, Base):
    __tablename__ = "trivia"
    __table_args__ = (
        sa.UniqueConstraint("guild_id", "user_id", name="trivia_guild_id_user_id_key"),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    correct_count: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default=sa.text("0")
    )
    wrong_count: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default=sa.text("0")
    )
    score: Mapped[int] = mapped_column(sa.BigInteger, nullable=False, server_default=sa.text("0"))


class TriviaStats(MappedAsDataclass, Base):
    __tablename__ = "trivia_stats"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    question_hash: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    result: Mapped[bool] = mapped_column(nullable=False)
