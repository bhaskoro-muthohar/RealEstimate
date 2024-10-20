from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from calculations.mortgage_calculations import MortgageCalculator, MortgageParams
from calculations.comparison import MortgageComparison, ComparisonParams

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate_mortgage_payments", response_class=HTMLResponse)
async def mortgage_payments(
    request: Request,
    property_price: float = Form(...),
    down_payment_percentage: float = Form(...),
    interest_rate_first_period: float = Form(...),
    interest_rate_subsequent_min: float = Form(...),
    interest_rate_subsequent_max: float = Form(...),
    mortgage_term_years: int = Form(...),
    fixed_interest_duration_years: int = Form(...),
    monthly_rent: float = Form(...)
):
    mortgage_params = MortgageParams(
        property_price=property_price,
        down_payment_percentage=down_payment_percentage,
        interest_rate_first_period=interest_rate_first_period,
        interest_rate_subsequent_min=interest_rate_subsequent_min,
        interest_rate_subsequent_max=interest_rate_subsequent_max,
        mortgage_term_years=mortgage_term_years,
        fixed_interest_duration_years=fixed_interest_duration_years
    )

    mortgage_payments = MortgageCalculator.calculate_mortgage_payments(mortgage_params)

    comparison_params = ComparisonParams(
        monthly_rent=monthly_rent,
        mortgage_params=mortgage_params,
        mortgage_payments=mortgage_payments
    )

    comparison_result = MortgageComparison.month_by_month_comparison(comparison_params)

    total_difference_min = (
        comparison_result.total_principal_paid + comparison_result.total_interest_paid_min 
        - comparison_result.total_rent_and_savings_paid
    )
    total_difference_max = (
        comparison_result.total_principal_paid + comparison_result.total_interest_paid_max 
        - comparison_result.total_rent_and_savings_paid
    )

    results = {
        'monthly_payment_first_period': mortgage_payments.monthly_payment_first_period,
        'monthly_payment_subsequent_min': mortgage_payments.monthly_payment_subsequent_min,
        'monthly_payment_subsequent_max': mortgage_payments.monthly_payment_subsequent_max,
        'total_principal_paid': comparison_result.total_principal_paid,
        'total_interest_paid_min': comparison_result.total_interest_paid_min,
        'total_interest_paid_max': comparison_result.total_interest_paid_max,
        'total_rent_and_savings_paid': comparison_result.total_rent_and_savings_paid,
        'total_difference_min': total_difference_min,
        'total_difference_max': total_difference_max,
        'monthly_comparison': comparison_result.monthly_comparison
    }

    return templates.TemplateResponse("results.html", {"request": request, "results": results})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)