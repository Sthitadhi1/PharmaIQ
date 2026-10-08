from app.schemas import SalesForecastRequest, SalesForecastResponse

HIGH_SPEND_THRESHOLD = 25000


def forecast_sales(payload: SalesForecastRequest) -> SalesForecastResponse:
    growth = 18 if payload.marketing_spend > HIGH_SPEND_THRESHOLD else 10
    # Stock follows forecast demand (it used to be floored at 15,000 units, which
    # overstocked low-volume products). Integer ceiling division avoids float error:
    # math.ceil(100 * 1.1) == 111.
    stock = -(-payload.sales_units * (100 + growth) // 100)
    return SalesForecastResponse(
        expected_growth=f'+{growth}%',
        growth_percentage=growth,
        recommended_stock=stock
    )
