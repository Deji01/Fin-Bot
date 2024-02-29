from datetime import date, datetime, timedelta 
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated

class DateRange(BaseModel):
    f"Object representing valid date range to filter database and search for financial market information. Today is {date.today()}"

    start_date: datetime = Field(..., description=f"Valid search date (start).  Example:  {date.today() - timedelta(5)}")
    end_date: datetime = Field(..., description=f"Valid search date (end). Example: {date.today()}")

class FinancialMarketData(BaseModel):
    """
    Stock Market Data Model.
    Represents information related to stock market data.
    """

    tickers = Annotated[List[Optional[str]], Field(description="List of Stock ticker symbols.")]
    date_range: DateRange