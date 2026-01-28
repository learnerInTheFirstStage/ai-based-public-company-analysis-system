import os
import json
from typing import List, Dict, Any
from app.models.schemas import RiskFlag
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class RiskSignalAgent:
    def run(self, ticker: str, financial_data: Dict[str, Any]) -> List[RiskFlag]:
        print(f"[RiskSignalAgent] Scanning risks for {ticker}...")
        
        # 1. Check for LLM Keys
        google_key = os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if google_key:
            print(f"[RiskSignalAgent] Found Google Key: {google_key[:5]}...{google_key[-5:]}")
        else:
            print("[RiskSignalAgent] No Google Key found.")

        llm = None
        if google_key:
            # Free tier friendly
            # Using 'gemini-flash-latest' as it is the stable alias for free tier
            llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0, google_api_key=google_key)
        elif openai_key:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_key)
            
        # 2. If LLM is available, use it
        if llm:
            try:
                print(f"[RiskSignalAgent] Using LLM to generate risks...")
                prompt = ChatPromptTemplate.from_template(
                    """
                    You are a financial risk analyst. Analyze the following financial data for {ticker}.
                    Identify 3-5 potential risks based on the numbers (e.g., declining margins, high debt, negative cash flow).
                    
                    Financial Data:
                    {data}
                    
                    Return the output ONLY as a valid JSON array of objects with these keys:
                    - "risk_category": string (e.g. "Liquidity", "Solvency", "Profitability", "Market")
                    - "description": string (concise explanation)
                    - "severity": string ("low", "medium", "high")
                    
                    Do not include markdown formatting like ```json. Just the raw JSON string.
                    """
                )
                
                chain = prompt | llm
                
                # Simplify data for LLM to save tokens
                simple_data = {
                    "revenue": financial_data.get("revenue"),
                    "net_income": financial_data.get("net_income"),
                    "debt": financial_data.get("total_debt"),
                    "equity": financial_data.get("total_equity"),
                    "operating_cash_flow": financial_data.get("cash_flow_operations"),
                    "revenue_growth": "Positive" if financial_data.get("revenue", 0) > financial_data.get("prev_revenue", 0) else "Negative"
                }
                
                response = chain.invoke({"ticker": ticker, "data": json.dumps(simple_data)})
                
                # Check response type. It might be a string or AIMessage
                if hasattr(response, 'content'):
                    content = response.content
                else:
                    content = str(response)
                    
                if isinstance(content, list):
                     # Sometimes chain returns a list if not parsed correctly?
                     # Or maybe response.content is a list of objects?
                     # Let's assume it's a string for now, but handle this case
                     content = json.dumps(content)

                print(f"[RiskSignalAgent] LLM Response Type: {type(content)}")
                
                # Ensure content is string before strip
                if not isinstance(content, str):
                    content = str(content)
                    
                content = content.strip()
                print(f"[RiskSignalAgent] LLM Response: {content[:100]}...") # Log first 100 chars
                
                # Clean up markdown if present
                if content.startswith("```json"):
                    content = content[7:]
                elif content.startswith("```"):
                     content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                
                content = content.strip()
                
                try:
                    risks_data = json.loads(content)
                except json.JSONDecodeError as je:
                    print(f"[RiskSignalAgent] JSON Decode Error: {je}. Content: {content}")
                    raise je
                
                risks = []
                for r in risks_data:
                    risks.append(RiskFlag(
                        risk_category=r.get("risk_category", "General"),
                        description=r.get("description", "Potential risk detected"),
                        severity=r.get("severity", "medium").lower()
                    ))
                return risks

            except Exception as e:
                print(f"[RiskSignalAgent] LLM generation failed: {e}. Falling back to rules.")
        
        # 3. Fallback Rule-based Logic
        risks = []
        
        # Rule 1: Net Margin Check
        rev = financial_data.get("revenue", 0)
        ni = financial_data.get("net_income", 0)
        if rev > 0:
            margin = ni / rev
            if margin < 0.05:
                risks.append(RiskFlag(
                    risk_category="Profitability",
                    description=f"Net profit margin is low ({(margin*100):.1f}%), indicating potential efficiency issues.",
                    severity="medium" if margin > 0 else "high"
                ))
        
        # Rule 2: Cash Flow Check
        ocf = financial_data.get("cash_flow_operations", 0)
        if ocf < 0:
            risks.append(RiskFlag(
                risk_category="Liquidity",
                description="Operating cash flow is negative, which may indicate difficulty in generating cash from core operations.",
                severity="high"
            ))
            
        # Rule 3: Debt/Equity
        debt = financial_data.get("total_debt", 0)
        equity = financial_data.get("total_equity", 0)
        if equity > 0 and (debt / equity) > 2.0:
            risks.append(RiskFlag(
                risk_category="Solvency",
                description=f"High Debt-to-Equity ratio ({(debt/equity):.1f}), indicating high leverage.",
                severity="medium"
            ))

        if not risks:
             risks.append(RiskFlag(
                risk_category="Stability",
                description="No significant financial risks detected in the provided dataset.",
                severity="low"
            ))
            
        return risks
