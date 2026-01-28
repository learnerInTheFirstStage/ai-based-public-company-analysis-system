import os
from typing import List
from app.models.schemas import MetricOutput, TrendSignal, RiskFlag
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class NarrativeGenerationAgent:
    def run(self, ticker: str, metrics: List[MetricOutput], trends: List[TrendSignal], risks: List[RiskFlag]) -> tuple[str, str]:
        print(f"[NarrativeGenerationAgent] Generating story for {ticker}")
        
        # 1. Check for LLM Keys
        google_key = os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if google_key:
            print(f"[NarrativeGenerationAgent] Found Google Key: {google_key[:5]}...{google_key[-5:]}")
        else:
            print("[NarrativeGenerationAgent] No Google Key found.")
        
        llm = None
        if google_key:
            llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.3, google_api_key=google_key)
        elif openai_key:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=openai_key)
            
        # 2. Use LLM if available
        if llm:
            try:
                print(f"[NarrativeGenerationAgent] Using LLM for narrative...")
                
                # Format inputs for the prompt
                metrics_str = "\n".join([f"- {m.metric_name}: {m.value} {m.unit}" for m in metrics])
                trends_str = "\n".join([f"- {t.metric}: {t.trend} ({t.description})" for t in trends])
                risks_str = "\n".join([f"- {r.risk_category} ({r.severity}): {r.description}" for r in risks])
                
                prompt = ChatPromptTemplate.from_template(
                    """
                    You are a professional financial analyst writing a report for {ticker}.
                    Based on the provided data, generate two outputs:
                    1. An 'Executive Summary' (2-3 sentences, professional tone).
                    2. A 'Detailed Analysis' (markdown formatted, including sections for Financial Health, Trends, and Risks).
                    
                    Data:
                    [Metrics]
                    {metrics}
                    
                    [Trends]
                    {trends}
                    
                    [Risks]
                    {risks}
                    
                    Output Format:
                    Start with the Executive Summary.
                    Then add a separator "|||".
                    Then provide the Detailed Analysis in Markdown.
                    """
                )
                
                chain = prompt | llm
                response = chain.invoke({
                    "ticker": ticker, 
                    "metrics": metrics_str,
                    "trends": trends_str,
                    "risks": risks_str
                })
                
                content = response.content
                if "|||" in content:
                    summary, details = content.split("|||", 1)
                    return summary.strip(), details.strip()
                else:
                    # If LLM didn't use the separator, assume the first paragraph is summary
                    parts = content.split("\n\n", 1)
                    if len(parts) > 1:
                        return parts[0].strip(), parts[1].strip()
                    else:
                        return content[:200] + "...", content
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"[NarrativeGenerationAgent] LLM failed: {e}. Falling back to template.")

        # 3. Fallback Template Logic
        summary = f"{ticker} demonstrates strong financial performance with " + \
                  f"{len([t for t in trends if t.trend == 'up'])} positive trends."
                  
        details = "## Financial Health\n\n"
        for m in metrics:
            details += f"- **{m.metric_name}**: {m.value} ({m.explanation})\n"
            
        details += "\n## Key Trends\n\n"
        for t in trends:
            details += f"- {t.metric}: {t.trend.upper()} - {t.description}\n"
            
        details += "\n## Risk Factors\n\n"
        for r in risks:
            details += f"- [{r.severity.upper()}] {r.risk_category}: {r.description}\n"
            
        return summary, details
