from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from models.base import Base


class Facts(MappedAsDataclass, Base):
    __tablename__ = "facts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
