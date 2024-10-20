from fastapi import FastAPI, Request, Form
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from calculations.mortgage_calculations import MortgageCalculator, MortgageParams
from calculations.comparison import MortgageComparison, ComparisonParams

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def format_number(value):
    return "{:,.2f}".format(value)

def parse_formatted_number(value: str) -> float:
    return float(value.replace(',', ''))

templates.env.filters["format_number"] = format_number

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate_mortgage_payments", response_class=HTMLResponse)
async def mortgage_payments(
    request: Request,
    property_price: str = Form(...),
    down_payment_percentage: float = Form(...),
    interest_rate_first_period: float = Form(...),
    interest_rate_subsequent_min: float = Form(...),
    interest_rate_subsequent_max: float = Form(...),
    mortgage_term_years: int = Form(...),
    fixed_interest_duration_years: int = Form(...),
    monthly_rent: str = Form(...),
    investment_return_rate: float = Form(...)
):
    mortgage_params = MortgageParams(
        property_price=parse_formatted_number(property_price),
        down_payment_percentage=down_payment_percentage / 100,
        interest_rate_first_period=interest_rate_first_period / 100,
        interest_rate_subsequent_min=interest_rate_subsequent_min / 100,
        interest_rate_subsequent_max=interest_rate_subsequent_max / 100,
        mortgage_term_years=mortgage_term_years,
        fixed_interest_duration_years=fixed_interest_duration_years
    )

    mortgage_payments = MortgageCalculator.calculate_mortgage_payments(mortgage_params)
    comparison_params = ComparisonParams(
        monthly_rent=parse_formatted_number(monthly_rent),
        mortgage_params=mortgage_params,
        mortgage_payments=mortgage_payments,
        investment_return_rate=investment_return_rate / 100
    )

    comparison_result = MortgageComparison.month_by_month_comparison(comparison_params)

    results = {
        'monthly_payment_first_period': mortgage_payments.monthly_payment_first_period,
        'monthly_payment_subsequent_min': mortgage_payments.monthly_payment_subsequent_min,
        'monthly_payment_subsequent_max': mortgage_payments.monthly_payment_subsequent_max,
        'total_mortgage_cost': comparison_result.total_mortgage_cost,
        'total_rent_cost': comparison_result.total_rent_cost,
        'total_investment_growth': comparison_result.total_investment_growth,
        'net_benefit_buying': comparison_result.net_benefit_buying,
        'monthly_comparison': comparison_result.monthly_comparison,
        'total_difference_max': comparison_result.total_difference_max,
        'is_renting_better': comparison_result.is_renting_better,
        'difference_min': comparison_result.difference_min,
        'difference_max': comparison_result.difference_max,
        'percentage_difference_min': comparison_result.percentage_difference_min,
        'percentage_difference_max': comparison_result.percentage_difference_max,
    }
    return templates.TemplateResponse("results.html", {"request": request, "results": results})
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)