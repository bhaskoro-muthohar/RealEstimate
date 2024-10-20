from typing import List, NamedTuple
from dataclasses import dataclass
from .mortgage_calculations import MortgageCalculator, MortgageParams, MortgagePayments

@dataclass
class ComparisonParams:
    monthly_rent: float
    mortgage_params: MortgageParams
    mortgage_payments: MortgagePayments
    investment_return_rate: float

class MonthlyComparison(NamedTuple):
    month: int
    monthly_mortgage_payment_min: float
    monthly_mortgage_payment_max: float
    monthly_rent: float
    investment_opportunity: float
    cumulative_investment: float
    principal_for_the_month: float
    interest_for_the_month_min: float
    interest_for_the_month_max: float
    total_rent_and_savings: float
    difference_min: float
    difference_max: float
class ComparisonResult(NamedTuple):
    monthly_comparison: List[MonthlyComparison]
    total_mortgage_cost: float
    total_rent_cost: float
    total_investment_growth: float
    net_benefit_buying: float
    total_difference_max: float
    is_renting_better: bool
    difference_min: float
    difference_max: float
    percentage_difference_min: float
    percentage_difference_max: float
class MortgageComparison:
    @classmethod
    def month_by_month_comparison(cls, params: ComparisonParams) -> ComparisonResult:
        monthly_comparison = []
        total_mortgage_cost = 0
        total_rent_cost = 0
        cumulative_investment = 0

        mortgage_term_months = MortgageCalculator.calculate_months(params.mortgage_params.mortgage_term_years)
        monthly_investment_rate = params.investment_return_rate / 12

        for month in range(1, mortgage_term_months + 1):
            monthly_payment_min = cls._get_monthly_mortgage_payment(month, params)
            monthly_payment_max = cls._get_monthly_mortgage_payment(month, params, use_max_rate=True)
            
            investment_opportunity = monthly_payment_max - params.monthly_rent
            cumulative_investment += investment_opportunity
            cumulative_investment *= (1 + monthly_investment_rate)

            total_mortgage_cost += monthly_payment_max
            total_rent_cost += params.monthly_rent

            principal_for_the_month = cls._calculate_principal_for_month(month, params)
            interest_for_the_month_min = monthly_payment_min - principal_for_the_month
            interest_for_the_month_max = monthly_payment_max - principal_for_the_month

            monthly_comparison.append(MonthlyComparison(
                month=month,
                monthly_mortgage_payment_min=monthly_payment_min,
                monthly_mortgage_payment_max=monthly_payment_max,
                monthly_rent=params.monthly_rent,
                investment_opportunity=investment_opportunity,
                cumulative_investment=cumulative_investment,
                principal_for_the_month=principal_for_the_month,
                interest_for_the_month_min=interest_for_the_month_min,
                interest_for_the_month_max=interest_for_the_month_max,
                total_rent_and_savings=params.monthly_rent + principal_for_the_month,
                difference_min=monthly_payment_min - (params.monthly_rent + principal_for_the_month),
                difference_max=monthly_payment_max - (params.monthly_rent + principal_for_the_month)
            ))

        total_investment_growth = cumulative_investment - sum(mc.investment_opportunity for mc in monthly_comparison)
        net_benefit_buying = total_rent_cost + total_investment_growth - total_mortgage_cost

        total_difference_max = max(abs(mc.cumulative_investment) for mc in monthly_comparison)
        is_renting_better = total_investment_growth > net_benefit_buying
        difference_min = min(total_investment_growth, net_benefit_buying)
        difference_max = max(total_investment_growth, net_benefit_buying)
        percentage_difference_min = (difference_min / total_mortgage_cost) * 100
        percentage_difference_max = (difference_max / total_mortgage_cost) * 100

        return ComparisonResult(
            monthly_comparison,
            total_mortgage_cost,
            total_rent_cost,
            total_investment_growth,
            net_benefit_buying,
            total_difference_max,
            is_renting_better,
            difference_min,
            difference_max,
            percentage_difference_min,
            percentage_difference_max
        )

    @staticmethod
    def _get_monthly_mortgage_payment(month: int, params: ComparisonParams, use_max_rate: bool = False) -> float:
        fixed_interest_duration_months = MortgageCalculator.calculate_months(params.mortgage_params.fixed_interest_duration_years)
        if month <= fixed_interest_duration_months:
            return params.mortgage_payments.monthly_payment_first_period
        else:
            return params.mortgage_payments.monthly_payment_subsequent_max if use_max_rate else params.mortgage_payments.monthly_payment_subsequent_min

    @staticmethod
    def _calculate_principal_for_month(month: int, params: ComparisonParams) -> float:
        # Implement the logic to calculate the principal for a given month
        # This is a placeholder and needs to be implemented based on your specific requirements
        return 0.0