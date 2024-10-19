from typing import List, NamedTuple
from dataclasses import dataclass
from .mortgage_calculations import MortgageCalculator, MortgageParams, MortgagePayments

@dataclass
class ComparisonParams:
    monthly_rent: float
    mortgage_params: MortgageParams
    mortgage_payments: MortgagePayments

class MonthlyComparison(NamedTuple):
    month: int
    monthly_mortgage_payment_min: float
    monthly_mortgage_payment_max: float
    principal_for_the_month: float
    interest_for_the_month_min: float
    interest_for_the_month_max: float
    total_rent_and_savings: float
    difference_min: float
    difference_max: float

class ComparisonResult(NamedTuple):
    monthly_comparison: List[MonthlyComparison]
    total_principal_paid: float
    total_interest_paid_min: float
    total_interest_paid_max: float
    total_rent_and_savings_paid: float

class MortgageComparison:
    @classmethod
    def month_by_month_comparison(cls, params: ComparisonParams) -> ComparisonResult:
        monthly_comparison = []
        remaining_balance_min = remaining_balance_max = params.mortgage_payments.loan_amount

        total_principal_paid = 0
        total_interest_paid_min = total_interest_paid_max = 0
        total_rent_and_savings_paid = 0

        fixed_interest_duration_months = MortgageCalculator.calculate_months(params.mortgage_params.fixed_interest_duration_years)
        mortgage_term_months = MortgageCalculator.calculate_months(params.mortgage_params.mortgage_term_years)

        for month in range(1, mortgage_term_months + 1):
            monthly_payment, monthly_interest_min, monthly_interest_max = cls._get_monthly_values(
                month, fixed_interest_duration_months, params
            )

            interest_for_the_month_min = remaining_balance_min * monthly_interest_min
            interest_for_the_month_max = remaining_balance_max * monthly_interest_max
            principal_for_the_month_min = monthly_payment - interest_for_the_month_min
            principal_for_the_month_max = monthly_payment - interest_for_the_month_max

            remaining_balance_min -= principal_for_the_month_min
            remaining_balance_max -= principal_for_the_month_max

            total_principal_paid += principal_for_the_month_min
            total_interest_paid_min += interest_for_the_month_min
            total_interest_paid_max += interest_for_the_month_max
            total_rent_and_savings = params.monthly_rent + principal_for_the_month_min
            total_rent_and_savings_paid += total_rent_and_savings

            monthly_comparison.append(MonthlyComparison(
                month=month,
                monthly_mortgage_payment_min=monthly_payment,
                monthly_mortgage_payment_max=monthly_payment,
                principal_for_the_month=principal_for_the_month_min,
                interest_for_the_month_min=interest_for_the_month_min,
                interest_for_the_month_max=interest_for_the_month_max,
                total_rent_and_savings=total_rent_and_savings,
                difference_min=monthly_payment - total_rent_and_savings,
                difference_max=monthly_payment - total_rent_and_savings
            ))

        return ComparisonResult(
            monthly_comparison,
            total_principal_paid,
            total_interest_paid_min,
            total_interest_paid_max,
            total_rent_and_savings_paid
        )

    @staticmethod
    def _get_monthly_values(month: int, fixed_interest_duration_months: int, params: ComparisonParams) -> tuple:
        if month <= fixed_interest_duration_months:
            monthly_payment = params.mortgage_payments.monthly_payment_first_period
            monthly_interest_min = monthly_interest_max = params.mortgage_params.interest_rate_first_period / 12
        else:
            if params.mortgage_params.fixed_interest_duration_years != params.mortgage_params.mortgage_term_years:
                monthly_payment = params.mortgage_payments.monthly_payment_subsequent_min
                monthly_interest_min = params.mortgage_params.interest_rate_subsequent_min / 12
                monthly_interest_max = params.mortgage_params.interest_rate_subsequent_max / 12
            else:
                monthly_payment = params.mortgage_payments.monthly_payment_first_period
                monthly_interest_min = monthly_interest_max = params.mortgage_params.interest_rate_first_period / 12
        
        return monthly_payment, monthly_interest_min, monthly_interest_max