from datetime import datetime

from pydantic import BaseModel, Field


class TradeLog(BaseModel):
    date: datetime = Field(..., description="거래일")
    symbol: str = Field(..., description="종목코드")
    label: str = Field(..., description="종목명")
    side: str = Field(..., description="거래방향(매수/매도)")
    quantity: int = Field(..., description="수량")
    price: float = Field(..., description="평균가")
    amount: float = Field(..., description="거래금액")
    transaction_costs: float | None = Field(None, description="수수료+제세금")
    pnl: float | None = Field(None, description="손익금액")
    return_pct: float | None = Field(None, description="수익률(%)")
