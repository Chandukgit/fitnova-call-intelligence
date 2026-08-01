from datetime import datetime

from sqlalchemy import String , DateTime , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column ,relationship

from app.database.base import Base


class Team(Base):
    __tablename__ = "teams"

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    organization_id : Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    is_active : Mapped[bool] = mapped_column(
        default= True,
        nullable=False 
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.utcnow,
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.utcnow,
        onupdate= datetime.utcnow
    )

    organization: Mapped["Organization"] = relationship(
    back_populates="teams"
    )
    advisors: Mapped[list["Advisor"]] = relationship(
    back_populates="team",
    cascade="all, delete-orphan"
    )


        