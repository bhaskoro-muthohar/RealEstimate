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