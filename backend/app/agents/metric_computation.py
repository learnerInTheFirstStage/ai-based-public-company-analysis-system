from typing import List, Dict, Any
from app.models.schemas import MetricOutput

class MetricComputationAgent:
    def run(self, data: Dict[str, Any]) -> List[MetricOutput]:
        print("[MetricComputationAgent] Computing metrics")
        metrics = []
        
        # Gross Margin = (Revenue - COGS) / Revenue
        if "revenue" in data and "cogs" in data:
            gm = (data["revenue"] - data["cogs"]) / data["revenue"]
            metrics.append(MetricOutput(
                metric_name="Gross Margin",
                value=round(gm, 4),
                unit="ratio",
                explanation="Percentage of revenue retained after direct costs"
            ))

        # Operating Margin = (Revenue - COGS - OpEx) / Revenue
        if "revenue" in data and "cogs" in data and "operating_expenses" in data:
            om = (data["revenue"] - data["cogs"] - data["operating_expenses"]) / data["revenue"]
            metrics.append(MetricOutput(
                metric_name="Operating Margin",
                value=round(om, 4),
                unit="ratio",
                explanation="Profitability after covering operating expenses"
            ))
            
        return metrics
