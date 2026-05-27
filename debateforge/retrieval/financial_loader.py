import yfinance as yf
from debateforge.core.exceptions import RetrievalError


class FinancialLoader:
    def load(self, ticker: str) -> dict:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            financials = stock.financials
            balance_sheet = stock.balance_sheet

            # recent revenue and net income (last 3 years)
            revenue_trend = {}
            net_income_trend = {}

            if not financials.empty:
                for col in list(financials.columns)[:3]:
                    year = str(col.year)
                    if "Total Revenue" in financials.index:
                        revenue_trend[year] = financials.loc["Total Revenue", col]
                    if "Net Income" in financials.index:
                        net_income_trend[year] = financials.loc["Net Income", col]

            # recent debt (last 2 years)
            debt_trend = {}
            if not balance_sheet.empty:
                for col in list(balance_sheet.columns)[:2]:
                    year = str(col.year)
                    if "Total Debt" in balance_sheet.index:
                        debt_trend[year] = balance_sheet.loc["Total Debt", col]

            return {
                "ticker": ticker,
                "name": info.get("longName", ticker),
                "sector": info.get("sector", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "revenue_growth": info.get("revenueGrowth", "N/A"),
                "profit_margins": info.get("profitMargins", "N/A"),
                "debt_to_equity": info.get("debtToEquity", "N/A"),
                "return_on_equity": info.get("returnOnEquity", "N/A"),
                "current_ratio": info.get("currentRatio", "N/A"),
                "summary": info.get("longBusinessSummary", "N/A"),
                "revenue_trend": revenue_trend,
                "net_income_trend": net_income_trend,
                "debt_trend": debt_trend,
            }

        except Exception as e:
            raise RetrievalError(f"Failed to load data for {ticker}: {e}")

    def to_context(self, data: dict) -> str:
        revenue_str = ", ".join(
            f"{yr}: ${val:,.0f}" for yr, val in sorted(data["revenue_trend"].items(), reverse=True)
        ) if data["revenue_trend"] else "N/A"

        net_income_str = ", ".join(
            f"{yr}: ${val:,.0f}" for yr, val in sorted(data["net_income_trend"].items(), reverse=True)
        ) if data["net_income_trend"] else "N/A"

        debt_str = ", ".join(
            f"{yr}: ${val:,.0f}" for yr, val in sorted(data["debt_trend"].items(), reverse=True)
        ) if data["debt_trend"] else "N/A"

        return f"""
Company: {data['name']} ({data['ticker']})
Sector: {data['sector']}
Market Cap: {data['market_cap']}
P/E Ratio: {data['pe_ratio']}
Revenue Growth (YoY): {data['revenue_growth']}
Profit Margins: {data['profit_margins']}
Debt to Equity: {data['debt_to_equity']}
Return on Equity: {data['return_on_equity']}
Current Ratio: {data['current_ratio']}

Revenue Trend (last 3 years): {revenue_str}
Net Income Trend (last 3 years): {net_income_str}
Total Debt Trend (last 2 years): {debt_str}

Business Summary:
{data['summary']}
""".strip()