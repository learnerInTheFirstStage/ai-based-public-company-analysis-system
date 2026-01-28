from typing import List, Dict, Any
from app.models.schemas import TrendSignal

class TrendAnalysisAgent:
    def run(self, data: Dict[str, Any]) -> List[TrendSignal]:
        print("[TrendAnalysisAgent] Analyzing trends")
        trends = []
        
        # Revenue Growth
        if "revenue" in data and "prev_revenue" in data:
            growth = (data["revenue"] - data["prev_revenue"]) / data["prev_revenue"]
            direction = "up" if growth > 0 else "down"
            trends.append(TrendSignal(
                metric="Revenue Growth",
                trend=direction,
                confidence=0.95,
                description=f"Revenue changed by {growth:.1%} YoY"
            ))
            
        return trends
