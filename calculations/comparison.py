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
    investment_opportunity_min: float
    investment_opportunity_max: float
    cumulative_investment_min: float
    cumulative_investment_max: float
    principal_for_the_month_min: float
    principal_for_the_month_max: float
    interest_for_the_month_min: float
    interest_for_the_month_max: float
    total_rent_and_savings_min: float
    total_rent_and_savings_max: float
    difference_min: float
    difference_max: float

class ComparisonResult(NamedTuple):
    monthly_comparison: List[MonthlyComparison]
    total_mortgage_cost_min: float
    total_mortgage_cost_max: float
    total_rent_cost: float
    total_investment_growth_min: float
    total_investment_growth_max: float
    net_benefit_buying_min: float
    net_benefit_buying_max: float
    max_payment_difference: float
    is_buying_cheaper_min: bool
    is_buying_cheaper_max: bool
    payment_difference_fixed: float
    payment_difference_variable_min: float
    payment_difference_variable_max: float
    savings_percent_fixed: float
    savings_percent_variable_min: float
    savings_percent_variable_max: float

class MortgageComparison:
    @classmethod
    def month_by_month_comparison(cls, params: ComparisonParams) -> ComparisonResult:
        monthly_comparison = []
        total_mortgage_cost_min = total_mortgage_cost_max = 0
        total_rent_cost = 0
        cumulative_investment_min = cumulative_investment_max = 0
        
        # Initialize tracking variables for both scenarios
        remaining_balance_min = remaining_balance_max = params.mortgage_payments.loan_amount
        fixed_interest_duration_months = MortgageCalculator.calculate_months(params.mortgage_params.fixed_interest_duration_years)
        mortgage_term_months = MortgageCalculator.calculate_months(params.mortgage_params.mortgage_term_years)
        monthly_investment_rate = params.investment_return_rate / 12

        # Calculate both scenarios
        for month in range(1, mortgage_term_months + 1):
            monthly_payment_min, monthly_payment_max, monthly_interest_min, monthly_interest_max = cls._get_monthly_values(month, params)
            
            # Calculate for min scenario
            interest_min = remaining_balance_min * monthly_interest_min
            principal_min = monthly_payment_min - interest_min
            remaining_balance_min -= principal_min
            total_mortgage_cost_min += monthly_payment_min

            # Calculate for max scenario
            interest_max = remaining_balance_max * monthly_interest_max
            principal_max = monthly_payment_max - interest_max
            remaining_balance_max -= principal_max
            total_mortgage_cost_max += monthly_payment_max

            # Investment calculations
            investment_opportunity_min = monthly_payment_min - params.monthly_rent
            investment_opportunity_max = monthly_payment_max - params.monthly_rent
            cumulative_investment_min += investment_opportunity_min
            cumulative_investment_max += investment_opportunity_max
            cumulative_investment_min *= (1 + monthly_investment_rate)
            cumulative_investment_max *= (1 + monthly_investment_rate)

            total_rent_cost += params.monthly_rent

            # Add monthly comparison data
            monthly_comparison.append(MonthlyComparison(
                month=month,
                monthly_mortgage_payment_min=monthly_payment_min,
                monthly_mortgage_payment_max=monthly_payment_max,
                monthly_rent=params.monthly_rent,
                investment_opportunity_min=investment_opportunity_min,
                investment_opportunity_max=investment_opportunity_max,
                cumulative_investment_min=cumulative_investment_min,
                cumulative_investment_max=cumulative_investment_max,
                principal_for_the_month_min=principal_min,
                principal_for_the_month_max=principal_max,
                interest_for_the_month_min=interest_min,
                interest_for_the_month_max=interest_max,
                total_rent_and_savings_min=params.monthly_rent + principal_min,
                total_rent_and_savings_max=params.monthly_rent + principal_max,
                difference_min=monthly_payment_min - (params.monthly_rent + principal_min),
                difference_max=monthly_payment_max - (params.monthly_rent + principal_max)
            ))

        # Calculate final results
        total_investment_growth_min = cumulative_investment_min - sum(mc.investment_opportunity_min for mc in monthly_comparison)
        total_investment_growth_max = cumulative_investment_max - sum(mc.investment_opportunity_max for mc in monthly_comparison)

        # Calculate wealth scenarios
        total_wealth_if_renting_min = total_investment_growth_min
        total_wealth_if_renting_max = total_investment_growth_max
        
        total_interest_paid_min = total_mortgage_cost_min - params.mortgage_payments.loan_amount
        total_interest_paid_max = total_mortgage_cost_max - params.mortgage_payments.loan_amount
        
        total_wealth_if_buying_min = params.mortgage_params.property_price - total_interest_paid_max
        total_wealth_if_buying_max = params.mortgage_params.property_price - total_interest_paid_min

        net_benefit_buying_min = total_wealth_if_buying_min - total_wealth_if_renting_max
        net_benefit_buying_max = total_wealth_if_buying_max - total_wealth_if_renting_min
        
        # Calculate payment differences for fixed and variable periods
        total_mortgage_cost_fixed_period = 0
        total_rent_cost_fixed_period = 0
        total_mortgage_cost_variable_min = 0
        total_mortgage_cost_variable_max = 0
        total_rent_cost_variable = 0

        fixed_months = MortgageCalculator.calculate_months(params.mortgage_params.fixed_interest_duration_years)
        
        for month, data in enumerate(monthly_comparison, 1):
            if month <= fixed_months:
                total_mortgage_cost_fixed_period += data.monthly_mortgage_payment_min
                total_rent_cost_fixed_period += params.monthly_rent
            else:
                total_mortgage_cost_variable_min += data.monthly_mortgage_payment_min
                total_mortgage_cost_variable_max += data.monthly_mortgage_payment_max
                total_rent_cost_variable += params.monthly_rent

        # Calculate differences and percentages
        payment_difference_fixed = total_rent_cost_fixed_period - total_mortgage_cost_fixed_period
        payment_difference_variable_min = total_rent_cost_variable - total_mortgage_cost_variable_min
        payment_difference_variable_max = total_rent_cost_variable - total_mortgage_cost_variable_max

        savings_percent_fixed = (payment_difference_fixed / total_rent_cost_fixed_period * 100) if total_rent_cost_fixed_period > 0 else 0
        savings_percent_variable_min = (payment_difference_variable_min / total_rent_cost_variable * 100) if total_rent_cost_variable > 0 else 0
        savings_percent_variable_max = (payment_difference_variable_max / total_rent_cost_variable * 100) if total_rent_cost_variable > 0 else 0

        return ComparisonResult(
            monthly_comparison=monthly_comparison,
            total_mortgage_cost_min=total_mortgage_cost_min,
            total_mortgage_cost_max=total_mortgage_cost_max,
            total_rent_cost=total_rent_cost,
            total_investment_growth_min=total_investment_growth_min,
            total_investment_growth_max=total_investment_growth_max,
            net_benefit_buying_min=net_benefit_buying_min,
            net_benefit_buying_max=net_benefit_buying_max,
            max_payment_difference=max(abs(mc.cumulative_investment_max) for mc in monthly_comparison),
            is_buying_cheaper_min=net_benefit_buying_min > 0,
            is_buying_cheaper_max=net_benefit_buying_max > 0,
            payment_difference_fixed=payment_difference_fixed,
            payment_difference_variable_min=payment_difference_variable_min,
            payment_difference_variable_max=payment_difference_variable_max,
            savings_percent_fixed=savings_percent_fixed,
            savings_percent_variable_min=savings_percent_variable_min,
            savings_percent_variable_max=savings_percent_variable_max
        )

    @staticmethod
    def _get_monthly_values(month: int, params: ComparisonParams) -> tuple:
        fixed_interest_duration_months = MortgageCalculator.calculate_months(params.mortgage_params.fixed_interest_duration_years)

        if month <= fixed_interest_duration_months:
            monthly_payment_min = monthly_payment_max = params.mortgage_payments.monthly_payment_first_period
            monthly_interest_min = monthly_interest_max = params.mortgage_params.interest_rate_first_period / 12
        else:
            if params.mortgage_params.fixed_interest_duration_years != params.mortgage_params.mortgage_term_years:
                monthly_payment_min = params.mortgage_payments.monthly_payment_subsequent_min
                monthly_payment_max = params.mortgage_payments.monthly_payment_subsequent_max
                monthly_interest_min = params.mortgage_params.interest_rate_subsequent_min / 12
                monthly_interest_max = params.mortgage_params.interest_rate_subsequent_max / 12
            else:
                monthly_payment_min = monthly_payment_max = params.mortgage_payments.monthly_payment_first_period
                monthly_interest_min = monthly_interest_max = params.mortgage_params.interest_rate_first_period / 12

        return monthly_payment_min, monthly_payment_max, monthly_interest_min, monthly_interest_max