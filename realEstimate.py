import numpy_financial as npf
from decimal import Decimal, getcontext
from calculations.mortgage_calculations import MortgageCalculator, MortgageParams, MortgagePayments
from calculations.comparison import MortgageComparison, ComparisonParams

# Set precision for financial calculations
getcontext().prec = 28

def main():
    """
    Demonstration of mortgage vs. rent comparison functionality using the refactored calculation modules.
    This standalone script provides similar functionality to the web app but with direct console output.
    """
    # Input data (using reasonable defaults)
    try:
        # Input data with validation (max property price check)
        property_price = Decimal('1600000000')  # IDR
        down_payment_percentage = Decimal('0.20')
        interest_rate_first_period = Decimal('0.025')
        interest_rate_subsequent_min = Decimal('0.09')
        interest_rate_subsequent_max = Decimal('0.12')
        mortgage_term_years = 20
        fixed_interest_duration_years = 5
        monthly_rent = Decimal('3500000')  # IDR
        investment_return_rate = Decimal('0.07')  # 7% annual return

        # Validate inputs
        if property_price > Decimal('1000000000000'):  # 1 trillion limit
            raise ValueError("Property price exceeds maximum supported value")
        
        # Set up calculation parameters
        mortgage_params = MortgageParams(
            property_price=property_price,
            down_payment_percentage=down_payment_percentage,
            interest_rate_first_period=interest_rate_first_period,
            interest_rate_subsequent_min=interest_rate_subsequent_min,
            interest_rate_subsequent_max=interest_rate_subsequent_max,
            mortgage_term_years=mortgage_term_years,
            fixed_interest_duration_years=fixed_interest_duration_years
        )

        # Calculate mortgage payments
        mortgage_payments = MortgageCalculator.calculate_mortgage_payments(mortgage_params)
        
        # Set up comparison parameters
        comparison_params = ComparisonParams(
            monthly_rent=monthly_rent,
            mortgage_params=mortgage_params,
            mortgage_payments=mortgage_payments,
            investment_return_rate=investment_return_rate
        )

        # Perform month-by-month comparison
        comparison_result = MortgageComparison.month_by_month_comparison(comparison_params)
        
        # Output Summary
        print("\n===== MORTGAGE VS. RENT COMPARISON SUMMARY =====")
        print(f"Property Price: {format_currency(property_price)}")
        print(f"Down Payment: {format_currency(property_price * down_payment_percentage)} ({down_payment_percentage * 100}%)")
        print(f"Loan Amount: {format_currency(mortgage_payments.loan_amount)}")
        print(f"Monthly Rent: {format_currency(monthly_rent)}")
        print("\n----- PAYMENT DETAILS -----")
        print(f"Monthly Payment (Initial Fixed Period): {format_currency(mortgage_payments.monthly_payment_first_period)}")
        print(f"Monthly Payment After Fixed Period (Min): {format_currency(mortgage_payments.monthly_payment_subsequent_min)}")
        print(f"Monthly Payment After Fixed Period (Max): {format_currency(mortgage_payments.monthly_payment_subsequent_max)}")
        
        print("\n----- TOTAL COSTS OVER MORTGAGE TERM -----")
        print(f"Total Principal Paid: {format_currency(comparison_result.total_principal_paid)}")
        print(f"Total Interest Paid: {format_currency(comparison_result.total_interest_paid_min)} to {format_currency(comparison_result.total_interest_paid_max)}")
        print(f"Total Mortgage Cost: {format_currency(comparison_result.total_mortgage_cost_min)} to {format_currency(comparison_result.total_mortgage_cost_max)}")
        print(f"Total Rent Cost: {format_currency(comparison_result.total_rent_cost)}")
        
        print("\n----- INVESTMENT ANALYSIS -----")
        print(f"Investment Return Rate: {investment_return_rate * 100}% annually")
        print(f"Total Investment Growth (if renting): {format_currency(comparison_result.total_investment_growth_min)} to {format_currency(comparison_result.total_investment_growth_max)}")
        
        print("\n----- BUYING VS. RENTING COMPARISON -----")
        print(f"Net Benefit of Buying: {format_currency(comparison_result.net_benefit_buying_min)} to {format_currency(comparison_result.net_benefit_buying_max)}")
        print(f"Is Buying Cheaper? {get_yes_no(comparison_result.is_buying_cheaper_min)} to {get_yes_no(comparison_result.is_buying_cheaper_max)}")
        
        # Optional: Display month-by-month comparison for a specific range
        display_detailed_months = False
        if display_detailed_months:
            print("\n===== DETAILED MONTHLY COMPARISON (FIRST 12 MONTHS) =====")
            display_months = min(12, len(comparison_result.monthly_comparison))
            for i in range(display_months):
                mc = comparison_result.monthly_comparison[i]
                print(f"\nMonth {mc.month}:")
                print(f"  Monthly Mortgage Payment: {format_currency(mc.monthly_mortgage_payment_min)} to {format_currency(mc.monthly_mortgage_payment_max)}")
                print(f"  Principal Payment: {format_currency(mc.principal_for_the_month_min)} to {format_currency(mc.principal_for_the_month_max)}")
                print(f"  Interest Payment: {format_currency(mc.interest_for_the_month_min)} to {format_currency(mc.interest_for_the_month_max)}")
                print(f"  Monthly Rent: {format_currency(mc.monthly_rent)}")
                print(f"  Total Rent + Principal Savings: {format_currency(mc.total_rent_and_savings_min)} to {format_currency(mc.total_rent_and_savings_max)}")
                print(f"  Financial Difference: {format_currency(mc.difference_min)} to {format_currency(mc.difference_max)}")
                print(f"  Cumulative Investment (if renting): {format_currency(mc.cumulative_investment_min)} to {format_currency(mc.cumulative_investment_max)}")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

def format_currency(value: Decimal) -> str:
    """Format a Decimal value as currency with thousands separators."""
    return f"{value:,.2f} IDR"

def get_yes_no(value: bool) -> str:
    """Convert boolean to Yes/No string."""
    return "Yes" if value else "No"

if __name__ == "__main__":
    main()