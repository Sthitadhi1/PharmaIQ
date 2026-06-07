from app.schemas import SalesForecastRequest, SalesForecastResponse


def forecast_sales(payload: SalesForecastRequest) -> SalesForecastResponse:
    growth = 18 if payload.marketing_spend > 25000 else 10
    stock = max(15000, int(payload.sales_units * (1 + growth / 100)))
    return SalesForecastResponse(expected_growth=f'+{growth}%', recommended_stock=stock)
