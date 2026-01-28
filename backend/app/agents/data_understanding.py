import yfinance as yf
import pandas as pd
from typing import Dict, Any, List
from app.models.schemas import FinancialData, HistoricalDataPoint

class DataUnderstandingAgent:
    def run(self, ticker: str) -> FinancialData:
        print(f"[DataUnderstandingAgent] Fetching data for {ticker} using yfinance...")
        
        try:
            stock = yf.Ticker(ticker)
            # Fetch data
            financials = stock.financials
            cashflow = stock.cashflow
            balance_sheet = stock.balance_sheet
            
            # Check if data exists
            if financials.empty:
                print(f"No financials found for {ticker}")
                raise ValueError("No financial data found")

            # Ensure columns (dates) are sorted descending (newest first)
            # yfinance usually returns them sorted, but good to be safe
            financials = financials.T.sort_index(ascending=False).T
            cashflow = cashflow.T.sort_index(ascending=False).T
            balance_sheet = balance_sheet.T.sort_index(ascending=False).T
            
            years = financials.columns
            if len(years) == 0:
                raise ValueError("No time periods found")
                
            latest_date = years[0]
            latest_year = latest_date.year

            # Helper to get value safely
            def get_val(df, keys, col_idx=0):
                if df.empty or col_idx >= len(df.columns):
                    return 0.0
                
                # Try multiple possible keys
                for key in keys:
                    if key in df.index:
                        val = df.iloc[df.index.get_loc(key), col_idx]
                        # Handle NaN
                        if pd.isna(val):
                            return 0.0
                        return float(val)
                return 0.0

            # 1. Build History (last 5 years)
            history = []
            # Take up to 5 years
            history_dates = years[:5]
            
            # Iterate backwards (oldest to newest) for the chart, 
            # but we fetched descending. So let's iterate and then sort.
            for idx, date in enumerate(history_dates):
                rev = get_val(financials, ["Total Revenue", "Revenue"], idx)
                ni = get_val(financials, ["Net Income", "Net Income Common Stockholders"], idx)
                ocf = get_val(cashflow, ["Operating Cash Flow", "Total Cash From Operating Activities"], idx)
                
                history.append({
                    "year": date.year,
                    "revenue": rev,
                    "net_income": ni,
                    "operating_cash_flow": ocf
                })
            
            # Sort by year ascending for frontend charts
            history.sort(key=lambda x: x["year"])

            # 2. Current Year Metrics
            revenue = get_val(financials, ["Total Revenue", "Revenue"])
            cogs = get_val(financials, ["Cost Of Revenue", "Cost of Revenue"])
            
            # Operating Expenses
            op_exp = get_val(financials, ["Operating Expense", "Total Operating Expenses"])
            if op_exp == 0:
                # Try summing components if total is missing
                sgna = get_val(financials, ["Selling General And Administration"])
                rnd = get_val(financials, ["Research And Development"])
                op_exp = sgna + rnd

            net_income = get_val(financials, ["Net Income", "Net Income Common Stockholders"])
            ocf = get_val(cashflow, ["Operating Cash Flow", "Total Cash From Operating Activities"])
            
            total_debt = get_val(balance_sheet, ["Total Debt", "Long Term Debt"]) # Simplified
            total_equity = get_val(balance_sheet, ["Stockholders Equity", "Total Stockholder Equity"])
            
            # Previous Revenue (for trend calculation)
            prev_revenue = get_val(financials, ["Total Revenue", "Revenue"], 1)

            return FinancialData(
                ticker=ticker,
                period=f"FY{latest_year}",
                year=latest_year,
                structured_data={
                    "revenue": revenue,
                    "cogs": cogs,
                    "operating_expenses": op_exp,
                    "net_income": net_income,
                    "cash_flow_operations": ocf,
                    "total_debt": total_debt,
                    "total_equity": total_equity,
                    "prev_revenue": prev_revenue,
                    "history": history
                }
            )

        except Exception as e:
            print(f"Error in DataUnderstandingAgent: {e}")
            # Fallback to empty/zeros so the UI doesn't crash but shows "0"
            return FinancialData(
                ticker=ticker,
                period="N/A",
                year=0,
                structured_data={
                    "revenue": 0,
                    "cogs": 0,
                    "operating_expenses": 0,
                    "net_income": 0,
                    "cash_flow_operations": 0,
                    "total_debt": 0,
                    "total_equity": 0,
                    "prev_revenue": 0,
                    "history": []
                }
            )
