from app.models.schemas import AnalysisResult, MetricOutput, TrendSignal, RiskFlag
from app.agents.data_understanding import DataUnderstandingAgent
from app.agents.metric_computation import MetricComputationAgent
from app.agents.trend_analysis import TrendAnalysisAgent
from app.agents.risk_signal import RiskSignalAgent
from app.agents.narrative_generation import NarrativeGenerationAgent
import asyncio

async def run_analysis(ticker: str) -> AnalysisResult:
    """
    Orchestrates the agent workflow:
    1. Data Understanding
    2. Metric Computation
    3. Trend Analysis
    4. Risk Signal
    5. Narrative Generation
    """
    
    # Initialize Agents
    data_agent = DataUnderstandingAgent()
    metric_agent = MetricComputationAgent()
    trend_agent = TrendAnalysisAgent()
    risk_agent = RiskSignalAgent()
    narrative_agent = NarrativeGenerationAgent()

    print(f"Starting analysis for {ticker}...")
    
    # 1. Data Understanding Agent
    financial_data = data_agent.run(ticker)
    
    # 2. Metric Computation Agent
    metrics = metric_agent.run(financial_data.structured_data)
    
    # 3. Trend Analysis Agent
    trends = trend_agent.run(financial_data.structured_data)
    
    # 4. Risk Signal Agent
    risks = risk_agent.run(ticker, financial_data.structured_data)
    
    # 5. Narrative Generation Agent
    summary, details = narrative_agent.run(ticker, metrics, trends, risks)
    
    # 6. References (Dynamic)
    references = [
        {
            "title": f"{ticker} Annual Report (SEC EDGAR)", 
            "url": f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={ticker}&action=getcompany", 
            "context": "Official SEC Filings (10-K, 10-Q)"
        },
        {
            "title": f"{ticker} Yahoo Finance Profile", 
            "url": f"https://finance.yahoo.com/quote/{ticker}", 
            "context": "Market Data & News"
        }
    ]
    
    # Extract history from data agent output
    history = financial_data.structured_data.get("history", [])

    return AnalysisResult(
        ticker=ticker,
        summary=summary,
        details=details,
        metrics=metrics,
        history=history,
        trends=trends,
        risks=risks,
        references=references
    )
