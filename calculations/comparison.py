from .mortgage_calculations import calculate_mortgage_payments

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