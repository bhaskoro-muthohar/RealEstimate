from calculations.mortgage_calculations import calculate_mortgage_payments
from calculations.comparison import month_by_month_comparison


def main():
    # Input data
    property_price = 1600000000  # IDR
    down_payment_percentage = 0.20
    interest_rate_first_period = 0.0111
    interest_rate_subsequent_min = 0.12
    interest_rate_subsequent_max = 0.12
    mortgage_term_years = 4
    fixed_interest_duration_years = 3
    monthly_rent = 3500000  # IDR

    # Calculations
    (
        monthly_payment_first_period,
        monthly_payment_subsequent_min,
        monthly_payment_subsequent_max,
        loan_amount,
    ) = calculate_mortgage_payments(
        property_price,
        down_payment_percentage,
        interest_rate_first_period,
        interest_rate_subsequent_min,
        interest_rate_subsequent_max,
        mortgage_term_years,
        fixed_interest_duration_years,
    )

    (
        monthly_comparison,
        total_principal_paid,
        total_interest_paid_min,
        total_interest_paid_max,
        total_rent_and_savings_paid,
    ) = month_by_month_comparison(
        monthly_payment_first_period,
        monthly_payment_subsequent_min,
        monthly_payment_subsequent_max,
        monthly_rent,
        mortgage_term_years,
        loan_amount,
        interest_rate_first_period,
        interest_rate_subsequent_min,
        interest_rate_subsequent_max,
        fixed_interest_duration_years,
    )

    # Output Summary
    print(f"Total Principal Paid: {total_principal_paid} IDR")
    print(
        f"Total Interest Paid: {total_interest_paid_min} to "
        f"{total_interest_paid_max} IDR"
    )
    print(f"Total Rent and Savings Paid: {total_rent_and_savings_paid} IDR")
    total_difference_min = (
        total_principal_paid + total_interest_paid_min 
        - total_rent_and_savings_paid
    )
    total_difference_max = (
        total_principal_paid + total_interest_paid_max 
        - total_rent_and_savings_paid
    )
    print(
        f"Total Financial Difference Over {mortgage_term_years} Years: "
        + f"{total_difference_min} to "
        + f"{total_difference_max} IDR\n"
    )

    # Detailed Monthly Output (optional)
    for month_data in monthly_comparison:
        print(f"Month {month_data['month']}:")
        print(
            "  Monthly Mortgage Payment (min rate): "
            + f"{month_data['monthly_mortgage_payment_min']} IDR"
        )
        print(
            "  Monthly Mortgage Payment (max rate): "
            + f"{month_data['monthly_mortgage_payment_max']} IDR"
        )
        print(
            "  Principal for the Month: "
            + f"{month_data['principal_for_the_month']} IDR"
        )
        print(
            "  Interest for the Month (min rate): "
            + f"{month_data['interest_for_the_month_min']} IDR"
        )
        print(
            "  Interest for the Month (max rate): "
            + f"{month_data['interest_for_the_month_max']} IDR"
        )
        print(
            "  Total Rent and Saving: " 
            + f"{month_data['total_rent_and_savings']} IDR"
        )
        print(
            "  Financial Difference (min rate): "
            + f"{month_data['difference_min']} IDR"
        )
        print(
            "  Financial Difference (max rate): "
            + f"{month_data['difference_max']} IDR\n"
        )


if __name__ == "__main__":
    main()
