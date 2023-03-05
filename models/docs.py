from __future__ import annotations

from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from models.base import Base


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
    __table_args__ = (
        sa.ForeignKeyConstraint(["docs_id"], ["docs_entry.id"], name="docs_syntax_docs_id_fkey"),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    docs_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    syntax: Mapped[str] = mapped_column(sa.Text, nullable=False)

    docs: Mapped[Optional[DocsEntry]] = relationship(back_populates="docs_syntax", default=None)
