"""
Main application module for the RealEstimate CLI interface.

This script demonstrates the mortgage vs. rent comparison functionality using 
the updated calculation modules with improved numerical precision and algorithms.
"""

from decimal import Decimal, getcontext
import uvicorn
from app import app
from calculations.mortgage_calculations import MortgageCalculator, MortgageParams
from calculations.comparison import MortgageComparison, ComparisonParams

# Set precision for financial calculations
getcontext().prec = 28

def format_currency(value):
    """Format a number with commas as IDR currency."""
    if isinstance(value, Decimal):
        return f"{value:,.2f} IDR"
    return f"{value:,.2f} IDR"

def run_cli_demo():
    """Run a demonstration of the mortgage calculation functionality from the CLI."""
    try:
        # Input data with Decimal for precision
        mortgage_params = MortgageParams(
            property_price=Decimal('750000000'),  # IDR
            down_payment_percentage=Decimal('0.20'),
            interest_rate_first_period=Decimal('0.0792'),
            interest_rate_subsequent_min=Decimal('0.12'),
            interest_rate_subsequent_max=Decimal('0.12'),
            mortgage_term_years=5,  # Longer term for more realistic analysis
            fixed_interest_duration_years=3  # Some fixed period followed by variable
        )
        monthly_rent = Decimal('5000000')  # IDR
        investment_return_rate = Decimal('0.06')  # 6% annual return on investments

        # Calculations
        mortgage_payments = MortgageCalculator.calculate_mortgage_payments(mortgage_params)

        comparison_params = ComparisonParams(
            monthly_rent=monthly_rent,
            mortgage_params=mortgage_params,
            mortgage_payments=mortgage_payments,
            investment_return_rate=investment_return_rate
        )

        comparison_result = MortgageComparison.month_by_month_comparison(comparison_params)

        # Output Summary
        print("\n===== MORTGAGE VS. RENT COMPARISON =====")
        print(f"Property Price: {format_currency(mortgage_params.property_price)}")
        print(f"Down Payment: {format_currency(mortgage_params.property_price * mortgage_params.down_payment_percentage)}")
        print(f"Monthly Rent: {format_currency(monthly_rent)}")
        print(f"Investment Return Rate: {investment_return_rate * 100}% annually")
        
        print("\n----- PAYMENT DETAILS -----")
        print(f"Monthly Payment (First {mortgage_params.fixed_interest_duration_years} years): {format_currency(mortgage_payments.monthly_payment_first_period)}")
        print(f"Monthly Payment (After fixed period): {format_currency(mortgage_payments.monthly_payment_subsequent_min)} to {format_currency(mortgage_payments.monthly_payment_subsequent_max)}")
        
        print("\n----- TOTAL COSTS -----")
        print(f"Total Principal Paid: {format_currency(comparison_result.total_principal_paid)}")
        print(f"Total Interest Paid: {format_currency(comparison_result.total_interest_paid_min)} to {format_currency(comparison_result.total_interest_paid_max)}")
        print(f"Total Mortgage Cost: {format_currency(comparison_result.total_mortgage_cost_min)} to {format_currency(comparison_result.total_mortgage_cost_max)}")
        print(f"Total Rent Cost: {format_currency(comparison_result.total_rent_cost)}")
        print(f"Investment Growth (if renting): {format_currency(comparison_result.total_investment_growth_min)} to {format_currency(comparison_result.total_investment_growth_max)}")
        
        print("\n----- BUYING VS. RENTING COMPARISON -----")
        print(f"Net Benefit of Buying: {format_currency(comparison_result.net_benefit_buying_min)} to {format_currency(comparison_result.net_benefit_buying_max)}")
        
        # Display results with recommendation
        if comparison_result.is_buying_cheaper_min and comparison_result.is_buying_cheaper_max:
            print("\nCONCLUSION: Buying is more economical in all scenarios.")
        elif not comparison_result.is_buying_cheaper_min and not comparison_result.is_buying_cheaper_max:
            print("\nCONCLUSION: Renting is more economical in all scenarios.")
        else:
            print("\nCONCLUSION: The outcome depends on future interest rates and investment returns.")
        
        # Optional detailed monthly output (only first few months)
        print_monthly_details = False
        if print_monthly_details:
            print("\n----- DETAILED MONTHLY DATA (First 3 months) -----")
            display_months = min(3, len(comparison_result.monthly_comparison))
            for i in range(display_months):
                mc = comparison_result.monthly_comparison[i]
                print(f"\nMonth {mc.month}:")
                print(f"  Monthly Mortgage Payment: {format_currency(mc.monthly_mortgage_payment_min)} to {format_currency(mc.monthly_mortgage_payment_max)}")
                print(f"  Principal: {format_currency(mc.principal_for_the_month_min)} to {format_currency(mc.principal_for_the_month_max)}")
                print(f"  Interest: {format_currency(mc.interest_for_the_month_min)} to {format_currency(mc.interest_for_the_month_max)}")
                print(f"  Monthly Rent: {format_currency(mc.monthly_rent)}")
                print(f"  Investment Growth: {format_currency(mc.cumulative_investment_min)} to {format_currency(mc.cumulative_investment_max)}")
    
    except ValueError as e:
        print(f"Error in calculation: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Determine if we should run the web app or CLI demo
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI demonstration
        run_cli_demo()
    else:
        # Start web application server
        uvicorn.run(app, host="0.0.0.0", port=8000)