from fastapi import FastAPI, Request, Form, HTTPException
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from calculations.mortgage_calculations import MortgageCalculator, MortgageParams
from calculations.comparison import MortgageComparison, ComparisonParams, ComparisonResult
from decimal import Decimal, InvalidOperation, getcontext

# Set precision for all calculations
getcontext().prec = 28

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def format_number(value):
    """Format a number with commas and 2 decimal places for display."""
    if isinstance(value, Decimal):
        # Convert Decimal to string with proper formatting
        return f"{value:,.2f}"
    return "{:,.2f}".format(value)

def parse_formatted_number(value: str) -> Decimal:
    """Parse a formatted number string into a Decimal.
    
    Args:
        value: A string containing a number with potential formatting like commas.
        
    Returns:
        The parsed decimal value.
        
    Raises:
        HTTPException: If the input value cannot be parsed as a valid number.
    """
    try:
        # Remove any commas and convert to Decimal
        cleaned = value.replace(',', '')
        return Decimal(cleaned)
    except InvalidOperation:
        raise HTTPException(status_code=400, detail=f"Invalid number format: '{value}'")

# Register the number formatter with Jinja
templates.env.filters["format_number"] = format_number

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main calculator form page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate_mortgage_payments", response_class=HTMLResponse)
async def mortgage_payments(
    request: Request,
    property_price: str = Form(...),
    down_payment_percentage: float = Form(...),
    interest_rate_first_period: float = Form(...),
    interest_rate_subsequent: float = Form(...),
    mortgage_term_years: int = Form(...),
    fixed_interest_duration_years: int = Form(...),
    monthly_rent: str = Form(...),
    investment_return_rate: float = Form(...)
):
    """Calculate and compare mortgage vs. renting scenarios based on form input.
    
    All percentage inputs from the form are converted from percentage to decimal
    form (e.g., 5.25% becomes 0.0525).
    """
    try:
        # Convert input parameters to Decimal for precise calculations
        mortgage_params = MortgageParams(
            property_price=parse_formatted_number(property_price),
            down_payment_percentage=Decimal(str(down_payment_percentage)) / Decimal('100'),
            interest_rate_first_period=Decimal(str(interest_rate_first_period)) / Decimal('100'),
            interest_rate_subsequent=Decimal(str(interest_rate_subsequent)) / Decimal('100'),
            mortgage_term_years=mortgage_term_years,
            fixed_interest_duration_years=fixed_interest_duration_years
        )

        # Calculate mortgage payments and comparison results
        mortgage_payments = MortgageCalculator.calculate_mortgage_payments(mortgage_params)
        comparison_params = ComparisonParams(
            monthly_rent=parse_formatted_number(monthly_rent),
            mortgage_params=mortgage_params,
            mortgage_payments=mortgage_payments,
            investment_return_rate=Decimal(str(investment_return_rate)) / Decimal('100')
        )

        comparison_result = MortgageComparison.month_by_month_comparison(comparison_params)

        # Prepare results for template rendering
        results = {
            'monthly_payment_first_period': mortgage_payments.monthly_payment_first_period,
            'monthly_payment_subsequent': mortgage_payments.monthly_payment_subsequent,
            'total_mortgage_cost': comparison_result.total_mortgage_cost,
            'total_rent_cost': comparison_result.total_rent_cost,
            'total_investment_growth': comparison_result.total_investment_growth,
            'net_benefit_buying': comparison_result.net_benefit_buying,
            'monthly_comparison': comparison_result.monthly_comparison,
            'yearly_summary': comparison_result.yearly_summary,
            'max_payment_difference': comparison_result.max_payment_difference,
            'is_buying_cheaper': comparison_result.is_buying_cheaper,
            'total_interest_paid': comparison_result.total_interest_paid,
            'total_principal_paid': comparison_result.total_principal_paid
        }
        
        # Convert yearly summary data to make it JSON serializable
        serializable_yearly_summary = []
        for year_data in results['yearly_summary']:
            serializable_yearly_summary.append({
                'year': year_data.year,
                'average_mortgage_payment': float(year_data.average_mortgage_payment),
                'average_rent': float(year_data.average_rent),
                'yearly_investment_growth': float(year_data.yearly_investment_growth),
                'total_principal_paid': float(year_data.total_principal_paid),
                'total_interest_paid': float(year_data.total_interest_paid)
            })
        
        # Replace the yearly_summary with the serializable version
        results_copy = results.copy()
        results_copy['yearly_summary'] = serializable_yearly_summary
        
        return templates.TemplateResponse("results.html", {
            "request": request, 
            "results": results_copy,
            "mortgage_params": mortgage_params,
            "mortgage_payments": mortgage_payments
        })
    except ValueError as e:
        # Return error message if validation fails
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log unexpected errors and return a generic error message
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing mortgage calculation: {str(e)}\n{error_details}")
        raise HTTPException(status_code=500, detail="An error occurred during calculation")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)