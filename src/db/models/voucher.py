from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
import uuid

from ...core.utils import generate_time


class VoucherStatus(str, Enum):
    ACTIVE = "active"
    REDEEMED = "redeemed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class Voucher(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )

    code: str = Field(
        index=True,
        unique=True,
        nullable=False
    )

    amount: float = Field(nullable=False)

    status: VoucherStatus = Field(
        default=VoucherStatus.ACTIVE, nullable=False
    )

    created_by_id: uuid.UUID | None = Field(
        foreign_key="user.id",
        ondelete="SET NULL",
        nullable=True
    )

    created_by_name: str = Field(
        nullable=False
    )

    redeemed_by_id: uuid.UUID | None = Field(
        foreign_key="user.id",
        ondelete="SET NULL",
        nullable=True
    )

    redeemed_by_name: str | None = Field(
        nullable=True
    )

    created_at: datetime = Field(
        default_factory=generate_time,
        nullable=False
    )

    redeemed_at: datetime | None = Field(
        nullable=True
    )
