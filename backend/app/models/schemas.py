from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FinancialData(BaseModel):
    ticker: str
    period: str
    year: int
    raw_text: Optional[str] = None
    structured_data: Dict[str, Any] = {}

class MetricOutput(BaseModel):
    metric_name: str
    value: float
    unit: str
    explanation: Optional[str] = None

class HistoricalDataPoint(BaseModel):
    year: int
    revenue: float
    net_income: float
    operating_cash_flow: float

class Reference(BaseModel):
    title: str
    url: str
    context: Optional[str] = None

class TrendSignal(BaseModel):
    metric: str
    trend: str  # "up", "down", "stable"
    confidence: float
    description: str

class RiskFlag(BaseModel):
    risk_category: str
    description: str
    severity: str  # "low", "medium", "high"
    reference_id: Optional[int] = None

class AnalysisResult(BaseModel):
    ticker: str
    summary: str
    details: str
    metrics: List[MetricOutput]
    history: List[HistoricalDataPoint] = []
    trends: List[TrendSignal]
    risks: List[RiskFlag]
    references: List[Reference] = []
