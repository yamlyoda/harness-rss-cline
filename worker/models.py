from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    source = Column(String(255), nullable=False, index=True)
    title = Column(Text, nullable=False)
    link = Column(Text, unique=True, nullable=False)
    published_at = Column(Text, nullable=True)
    published_at_normalized = Column(DateTime, nullable=True)
    text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    entities = relationship(
        "Entity", back_populates="news", cascade="all, delete-orphan"
    )


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True)
    news_id = Column(
        Integer,
        ForeignKey("news.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text = Column(Text, nullable=False, index=True)
    label = Column(String(50), nullable=False, index=True)
    count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    news = relationship("News", back_populates="entities")
