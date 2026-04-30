from pydantic import BaseModel, Field
from typing import List, Optional

class MarketAnalysis(BaseModel):
    key_trends: List[str]
    market_size: str

class CompetitorAnalysis(BaseModel):
    competitors: List[str]
    positioning: List[str]

class FinalReport(BaseModel):
    product: str
    market: MarketAnalysis
    competition: CompetitorAnalysis
    summary: str
