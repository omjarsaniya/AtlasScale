from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from atlasscale.database.connection import Base


class JobModel(Base):
    __tablename__ = "jobs"

    job_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    task: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )