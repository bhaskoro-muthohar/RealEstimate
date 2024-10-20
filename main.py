from calculations.mortgage_calculations import MortgageCalculator, MortgageParams
from calculations.comparison import MortgageComparison, ComparisonParams


def main():
    # Input data
    mortgage_params = MortgageParams(
        property_price=750000000,  # IDR
        down_payment_percentage=0.20,
        interest_rate_first_period=0.0792,
        interest_rate_subsequent_min=0.12,
        interest_rate_subsequent_max=0.12,
        mortgage_term_years=1,
        fixed_interest_duration_years=1
    )
    monthly_rent = 5000000  # IDR

    # Calculations
    mortgage_payments = MortgageCalculator.calculate_mortgage_payments(mortgage_params)

    comparison_params = ComparisonParams(
        monthly_rent=monthly_rent,
        mortgage_params=mortgage_params,
        mortgage_payments=mortgage_payments
    )

    comparison_result = MortgageComparison.month_by_month_comparison(comparison_params)

    # Output Summary
    print(f"Total Principal Paid: {comparison_result.total_principal_paid:,.0f} IDR")
    print(
        f"Total Interest Paid: {comparison_result.total_interest_paid_min:,.0f} to "
        f"{comparison_result.total_interest_paid_max:,.0f} IDR"
    )
    print(f"Total Rent and Savings Paid: {comparison_result.total_rent_and_savings_paid:,.0f} IDR")

    total_mortgage_cost_min = comparison_result.total_principal_paid + comparison_result.total_interest_paid_min
    total_mortgage_cost_max = comparison_result.total_principal_paid + comparison_result.total_interest_paid_max

    difference_min = total_mortgage_cost_min - comparison_result.total_rent_and_savings_paid
    difference_max = total_mortgage_cost_max - comparison_result.total_rent_and_savings_paid

    percentage_difference_min = (difference_min / total_mortgage_cost_min) * 100
    percentage_difference_max = (difference_max / total_mortgage_cost_max) * 100

    if difference_min > 0:
        print(f"Renting and Saving is more economical by {difference_min:,.0f} to {difference_max:,.0f} IDR")
        print(f"This represents a {percentage_difference_min:.2f}% to {percentage_difference_max:.2f}% savings compared to buying")
    else:
        print(f"Buying is more economical by {-difference_max:,.0f} to {-difference_min:,.0f} IDR")
        print(f"This represents a {-percentage_difference_max:.2f}% to {-percentage_difference_min:.2f}% savings compared to renting")

    print(f"\nTotal Financial Difference Over {mortgage_params.mortgage_term_years} Years: "
          f"{difference_min:,.0f} to {difference_max:,.0f} IDR")
    # Detailed Monthly Output (optional)
    for month_data in comparison_result.monthly_comparison:
        print(f"Month {month_data.month}:")
        print(
            "  Monthly Mortgage Payment (min rate): "
            + f"{month_data.monthly_mortgage_payment_min} IDR"
        )
        print(
            "  Monthly Mortgage Payment (max rate): "
            + f"{month_data.monthly_mortgage_payment_max} IDR"
        )
        print(
            "  Principal for the Month: "
            + f"{month_data.principal_for_the_month} IDR"
        )
        print(
            "  Interest for the Month (min rate): "
            + f"{month_data.interest_for_the_month_min} IDR"
        )
        print(
            "  Interest for the Month (max rate): "
            + f"{month_data.interest_for_the_month_max} IDR"
        )
        print(
            "  Total Rent and Saving: " 
            + f"{month_data.total_rent_and_savings} IDR"
        )
        print(
            "  Financial Difference (min rate): "
            + f"{month_data.difference_min} IDR"
        )
        print(
            "  Financial Difference (max rate): "
            + f"{month_data.difference_max} IDR\n"
        )


if __name__ == "__main__":
    main()