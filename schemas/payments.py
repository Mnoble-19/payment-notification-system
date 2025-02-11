# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class BankNotificationRequest(BaseModel):
    notification_text: str = Field(
        ...,  # ... means required
        description="Raw bank notification text",
        min_length=1
    )

class TransactionResponse(BaseModel):
    transaction_id: UUID
    customer_id: str
    amount: float
    transaction_date: datetime
    description: str
    status: str
    created_at: datetime

class BankNotificationResponse(BaseModel):
    status: str = Field(..., example="success")
    transaction_id: UUID
    customer_id: str
    message: Optional[str] = Field(None, example="Transaction processed successfully")

class ErrorResponse(BaseModel):
    detail: str
    status_code: int

class CustomerTransactionsResponse(BaseModel):
    customer_id: str
    transactions: List[TransactionResponse]

class HealthCheckResponse(BaseModel):
    status: str = Field(..., example="healthy")
    timestamp: datetime = Field(default_factory=datetime.now)