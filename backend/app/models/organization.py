from datetime import datetime
from sqlalchemy import String , DateTime 
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from sqlalchemy.orm import relationship

class Organization(Base):
    __tablename__ = "organizations"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(
        String (100),
        nullable=False 
    )

    email : Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
        
        )

    phone : Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(
    default=True,
    nullable=False
    )
    teams: Mapped[list["Team"]] = relationship(
    back_populates="organization",
    cascade="all, delete-orphan"
)

