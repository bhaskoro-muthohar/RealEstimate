import numpy_financial as npf

def calculate_mortgage_payments(property_price, down_payment_percentage, interest_rate_first_period, interest_rate_subsequent_min, interest_rate_subsequent_max, mortgage_term_years, fixed_interest_duration_years):
    loan_amount = property_price * (1 - down_payment_percentage)
    mortgage_term_months = mortgage_term_years * 12
    fixed_interest_duration_months = fixed_interest_duration_years * 12

    monthly_interest_first_period = interest_rate_first_period / 12
    monthly_payment_first_period = npf.pmt(monthly_interest_first_period, mortgage_term_months, -loan_amount)

    if fixed_interest_duration_years != mortgage_term_years:
        remaining_balance_after_fixed_period = npf.fv(monthly_interest_first_period, fixed_interest_duration_months, monthly_payment_first_period, -loan_amount)
        monthly_interest_subsequent_min = interest_rate_subsequent_min / 12
        monthly_interest_subsequent_max = interest_rate_subsequent_max / 12
        monthly_payment_subsequent_min = npf.pmt(monthly_interest_subsequent_min, mortgage_term_months - fixed_interest_duration_months, -remaining_balance_after_fixed_period)
        monthly_payment_subsequent_max = npf.pmt(monthly_interest_subsequent_max, mortgage_term_months - fixed_interest_duration_months, -remaining_balance_after_fixed_period)
    else:
        monthly_payment_subsequent_min = monthly_payment_subsequent_max = monthly_payment_first_period

    return monthly_payment_first_period, monthly_payment_subsequent_min, monthly_payment_subsequent_max, loan_amount

def month_by_month_comparison(monthly_payment_first_period, monthly_payment_subsequent_min, monthly_payment_subsequent_max, monthly_rent, mortgage_term_years, loan_amount, interest_rate_first_period, interest_rate_subsequent_min, interest_rate_subsequent_max, fixed_interest_duration_years):
    monthly_comparison = []
    remaining_balance_min = remaining_balance_max = loan_amount

    total_principal_paid = 0
    total_interest_paid_min = total_interest_paid_max = 0
    total_rent_and_savings_paid = 0

    fixed_interest_duration_months = fixed_interest_duration_years * 12

    for month in range(1, mortgage_term_years * 12 + 1):
        if month <= fixed_interest_duration_months:
            monthly_payment = monthly_payment_first_period
            monthly_interest_min = monthly_interest_max = interest_rate_first_period / 12
        else:
            if fixed_interest_duration_years != mortgage_term_years:
                monthly_payment = monthly_payment_subsequent_min
                monthly_interest_min = interest_rate_subsequent_min / 12
                monthly_interest_max = interest_rate_subsequent_max / 12
            else:
                monthly_payment = monthly_payment_first_period
                monthly_interest_min = monthly_interest_max = interest_rate_first_period / 12

        interest_for_the_month_min = remaining_balance_min * monthly_interest_min
        interest_for_the_month_max = remaining_balance_max * monthly_interest_max
        principal_for_the_month_min = monthly_payment - interest_for_the_month_min
        principal_for_the_month_max = monthly_payment - interest_for_the_month_max

        remaining_balance_min -= principal_for_the_month_min
        remaining_balance_max -= principal_for_the_month_max

        total_principal_paid += principal_for_the_month_min
        total_interest_paid_min += interest_for_the_month_min
        total_interest_paid_max += interest_for_the_month_max
        total_rent_and_savings_paid += monthly_rent + principal_for_the_month_min

        monthly_comparison.append({
            'month': month,
            'monthly_mortgage_payment_min': monthly_payment,
            'monthly_mortgage_payment_max': monthly_payment,
            'principal_for_the_month': principal_for_the_month_min,
            'interest_for_the_month_min': interest_for_the_month_min,
            'interest_for_the_month_max': interest_for_the_month_max,
            'total_rent_and_savings': monthly_rent + principal_for_the_month_min,
            'difference_min': monthly_payment - (monthly_rent + principal_for_the_month_min),
            'difference_max': monthly_payment - (monthly_rent + principal_for_the_month_min)
        })

    return monthly_comparison, total_principal_paid, total_interest_paid_min, total_interest_paid_max, total_rent_and_savings_paid

def main():
    # Input data
    property_price = 1600000000  # IDR
    down_payment_percentage = 0.20
    interest_rate_first_period = 0.025
    interest_rate_subsequent_min = 0.12
    interest_rate_subsequent_max = 0.12
    mortgage_term_years = 13
    fixed_interest_duration_years = 13
    monthly_rent = 3500000  # IDR

    # Calculations
    monthly_payment_first_period, monthly_payment_subsequent_min, monthly_payment_subsequent_max, loan_amount = calculate_mortgage_payments(
        property_price, down_payment_percentage, interest_rate_first_period, interest_rate_subsequent_min, interest_rate_subsequent_max, mortgage_term_years, fixed_interest_duration_years)

    monthly_comparison, total_principal_paid, total_interest_paid_min, total_interest_paid_max, total_rent_and_savings_paid = month_by_month_comparison(
        monthly_payment_first_period, monthly_payment_subsequent_min, monthly_payment_subsequent_max, monthly_rent, mortgage_term_years, loan_amount, interest_rate_first_period, interest_rate_subsequent_min, interest_rate_subsequent_max, fixed_interest_duration_years)

    # Output Summary
    print(f"Total Principal Paid: {total_principal_paid} IDR")
    print(f"Total Interest Paid: {total_interest_paid_min} to {total_interest_paid_max} IDR")
    print(f"Total Rent and Savings Paid: {total_rent_and_savings_paid} IDR")
    print(f"Total Financial Difference Over 13 Years: {total_principal_paid + total_interest_paid_min - total_rent_and_savings_paid} to {total_principal_paid + total_interest_paid_max - total_rent_and_savings_paid} IDR\n")

    # Detailed Monthly Output (optional)
    for month_data in monthly_comparison:
        print(f"Month {month_data['month']}:")
        print(f"  Monthly Mortgage Payment (min rate): {month_data['monthly_mortgage_payment_min']} IDR")
        print(f"  Monthly Mortgage Payment (max rate): {month_data['monthly_mortgage_payment_max']} IDR")
        print(f"  Principal for the Month: {month_data['principal_for_the_month']} IDR")
        print(f"  Interest for the Month (min rate): {month_data['interest_for_the_month_min']} IDR")
        print(f"  Interest for the Month (max rate): {month_data['interest_for_the_month_max']} IDR")
        print(f"  Total Rent and Saving: {month_data['total_rent_and_savings']} IDR")
        print(f"  Financial Difference (min rate): {month_data['difference_min']} IDR")
        print(f"  Financial Difference (max rate): {month_data['difference_max']} IDR\n")

if __name__ == "__main__":
    main()