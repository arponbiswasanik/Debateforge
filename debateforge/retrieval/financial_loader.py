import requests
from debateforge.core.exceptions import RetrievalError
from debateforge.config.settings import settings


class FinancialLoader:
    BASE_URL = "https://www.alphavantage.co/query"

    def load(self, ticker: str) -> dict:
        try:
            overview = self._get_overview(ticker)
            income = self._get_income_statement(ticker)

            revenue_trend = {}
            net_income_trend = {}

            if income.get("annualReports"):
                for report in income["annualReports"][:3]:
                    year = report["fiscalDateEnding"][:4]
                    revenue_trend[year] = int(report.get("totalRevenue", 0))
                    net_income_trend[year] = int(report.get("netIncome", 0))

            return {
                "ticker": ticker,
                "name": overview.get("Name", ticker),
                "sector": overview.get("Sector", "N/A"),
                "market_cap": overview.get("MarketCapitalization", "N/A"),
                "pe_ratio": overview.get("PERatio", "N/A"),
                "revenue_growth": overview.get("QuarterlyRevenueGrowthYOY", "N/A"),
                "profit_margins": overview.get("ProfitMargin", "N/A"),
                "debt_to_equity": overview.get("DebtToEquityRatio", "N/A"),
                "return_on_equity": overview.get("ReturnOnEquityTTM", "N/A"),
                "current_ratio": overview.get("CurrentRatio", "N/A"),
                "summary": overview.get("Description", "N/A"),
                "revenue_trend": revenue_trend,
                "net_income_trend": net_income_trend,
                "debt_trend": {},
            }

        except Exception as e:
            raise RetrievalError(f"Failed to load data for {ticker}: {e}")

    def _get_overview(self, ticker: str) -> dict:
        params = {
            "function": "OVERVIEW",
            "symbol": ticker,
            "apikey": settings.alpha_vantage_api_key,
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def _get_income_statement(self, ticker: str) -> dict:
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": ticker,
            "apikey": settings.alpha_vantage_api_key,
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def to_context(self, data: dict) -> str:
        revenue_str = ", ".join(
            f"{yr}: ${val:,.0f}" for yr, val in sorted(data["revenue_trend"].items(), reverse=True)
        ) if data["revenue_trend"] else "N/A"

        net_income_str = ", ".join(
            f"{yr}: ${val:,.0f}" for yr, val in sorted(data["net_income_trend"].items(), reverse=True)
        ) if data["net_income_trend"] else "N/A"

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

Business Summary:
{data['summary']}
""".strip()