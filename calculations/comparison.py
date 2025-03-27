from typing import List, NamedTuple, Dict
from dataclasses import dataclass
from decimal import Decimal
from .mortgage_calculations import MortgageCalculator, MortgageParams, MortgagePayments

@dataclass
class ComparisonParams:
    monthly_rent: Decimal
    mortgage_params: MortgageParams
    mortgage_payments: MortgagePayments
    investment_return_rate: Decimal

class MonthlyComparison(NamedTuple):
    month: int
    year: int  # Added year for filtering
    month_of_year: int  # Added month within year (1-12)
    monthly_mortgage_payment: Decimal
    monthly_rent: Decimal
    investment_opportunity: Decimal
    cumulative_investment: Decimal
    principal_for_the_month: Decimal
    interest_for_the_month: Decimal
    total_rent_and_savings: Decimal
    difference: Decimal

class YearSummary(NamedTuple):
    year: int
    average_mortgage_payment: Decimal
    average_rent: Decimal
    yearly_investment_growth: Decimal
    total_principal_paid: Decimal
    total_interest_paid: Decimal

class ComparisonResult(NamedTuple):
    monthly_comparison: List[MonthlyComparison]
    yearly_summary: List[YearSummary]
    total_mortgage_cost: Decimal
    total_rent_cost: Decimal
    total_investment_growth: Decimal
    net_benefit_buying: Decimal
    max_payment_difference: Decimal
    is_buying_cheaper: bool
    payment_difference_fixed: Decimal
    payment_difference_variable: Decimal
    savings_percent_fixed: Decimal
    savings_percent_variable: Decimal
    total_interest_paid: Decimal
    total_principal_paid: Decimal

class MortgageComparison:
    @classmethod
    def month_by_month_comparison(cls, params: ComparisonParams) -> ComparisonResult:
        monthly_comparison = []
        yearly_summary = []
        total_mortgage_cost = Decimal('0')
        total_rent_cost = Decimal('0')
        
        # Use pre-calculated values from mortgage_payments when available
        fixed_interest_duration_months = params.mortgage_payments.fixed_interest_duration_months
        mortgage_term_months = params.mortgage_payments.mortgage_term_months
        
        # Calculate monthly investment rate (with high precision)
        monthly_investment_rate = params.investment_return_rate / Decimal('12')
        
        # Initialize tracking variables for amortization calculations
        remaining_balance = params.mortgage_payments.loan_amount
        
        # Initialize counters for direct incremental tracking (avoiding later sums)
        cumulative_investment = Decimal('0')
        total_investment_amount = Decimal('0')
        total_principal_paid = Decimal('0')
        total_interest_paid = Decimal('0')
        
        # Variables for tracking yearly data
        current_year = 1
        year_mortgage_payment_sum = Decimal('0')
        year_rent_sum = Decimal('0')
        year_investment_growth = Decimal('0')
        year_principal_paid = Decimal('0')
        year_interest_paid = Decimal('0')
        prev_cumulative_investment = Decimal('0')
        months_in_current_year = 0

        # Calculate both scenarios month-by-month
        for month in range(1, mortgage_term_months + 1):
            # Calculate year and month_of_year
            year = ((month - 1) // 12) + 1  # 1-based year (1, 2, 3, etc.)
            month_of_year = ((month - 1) % 12) + 1  # 1-based month within year (1-12)
            
            # Check if we need to create a yearly summary
            if year > current_year:
                # Create yearly summary for the completed year
                yearly_summary.append(YearSummary(
                    year=current_year,
                    average_mortgage_payment=year_mortgage_payment_sum / months_in_current_year,
                    average_rent=year_rent_sum / months_in_current_year,
                    yearly_investment_growth=year_investment_growth,
                    total_principal_paid=year_principal_paid,
                    total_interest_paid=year_interest_paid
                ))
                
                # Reset tracking variables for new year
                current_year = year
                year_mortgage_payment_sum = Decimal('0')
                year_rent_sum = Decimal('0')
                year_investment_growth = Decimal('0')
                year_principal_paid = Decimal('0')
                year_interest_paid = Decimal('0')
                prev_cumulative_investment = cumulative_investment
                months_in_current_year = 0
            
            # Get monthly values based on the period
            monthly_payment, monthly_interest = cls._get_monthly_values(
                month, params, fixed_interest_duration_months)
            
            # Calculate monthly payment components
            interest = remaining_balance * monthly_interest
            principal = monthly_payment - interest
            remaining_balance -= principal
            
            # Track totals
            total_mortgage_cost += monthly_payment
            total_interest_paid += interest
            total_principal_paid += principal
            
            # Calculate investment opportunity (difference between mortgage payment and rent)
            investment_opportunity = monthly_payment - params.monthly_rent
            
            # Track total amount invested (before growth)
            total_investment_amount += investment_opportunity
            
            # Apply investment growth (based on previous cumulative amount + new investment)
            if month == 1:
                # First month, just set the initial investment
                cumulative_investment = investment_opportunity
            else:
                # Add new investment to current balance and then apply growth
                cumulative_investment = (cumulative_investment + investment_opportunity) * (Decimal('1') + monthly_investment_rate)
            
            # Track rent costs
            total_rent_cost += params.monthly_rent
            
            # Update yearly tracking
            year_mortgage_payment_sum += monthly_payment
            year_rent_sum += params.monthly_rent
            year_principal_paid += principal
            year_interest_paid += interest
            months_in_current_year += 1
            
            # Create monthly comparison record
            monthly_comparison.append(MonthlyComparison(
                month=month,
                year=year,
                month_of_year=month_of_year,
                monthly_mortgage_payment=monthly_payment,
                monthly_rent=params.monthly_rent,
                investment_opportunity=investment_opportunity,
                cumulative_investment=cumulative_investment,
                principal_for_the_month=principal,
                interest_for_the_month=interest,
                total_rent_and_savings=params.monthly_rent + principal,
                difference=monthly_payment - (params.monthly_rent + principal)
            ))
            
            # Calculate yearly investment growth for tracking - update whenever the last month of a year is processed
            if month_of_year == 12 or month == mortgage_term_months:
                year_investment_growth = cumulative_investment - prev_cumulative_investment - investment_opportunity
        
        # Add the final year summary if not already added
        if months_in_current_year > 0:
            yearly_summary.append(YearSummary(
                year=current_year,
                average_mortgage_payment=year_mortgage_payment_sum / months_in_current_year,
                average_rent=year_rent_sum / months_in_current_year,
                yearly_investment_growth=year_investment_growth,
                total_principal_paid=year_principal_paid,
                total_interest_paid=year_interest_paid
            ))
        
        # Calculate investment growth (final amount minus amount invested)
        total_investment_growth = cumulative_investment - total_investment_amount
        
        # Calculate wealth scenarios
        total_wealth_if_renting = total_investment_growth
        total_wealth_if_buying = params.mortgage_params.property_price - total_interest_paid
        
        # Calculate net benefits
        net_benefit_buying = total_wealth_if_buying - total_wealth_if_renting
        
        # Calculate fixed and variable period costs more efficiently
        total_mortgage_cost_fixed_period = Decimal('0')
        total_rent_cost_fixed_period = Decimal('0')
        total_mortgage_cost_variable = Decimal('0')
        total_rent_cost_variable = Decimal('0')
        
        # More efficient iteration with direct access to month value
        for mc in monthly_comparison:
            if mc.month <= fixed_interest_duration_months:
                total_mortgage_cost_fixed_period += mc.monthly_mortgage_payment
                total_rent_cost_fixed_period += params.monthly_rent
            else:
                total_mortgage_cost_variable += mc.monthly_mortgage_payment
                total_rent_cost_variable += params.monthly_rent
        
        # Calculate payment differences with protection against division by zero
        payment_difference_fixed = total_rent_cost_fixed_period - total_mortgage_cost_fixed_period
        payment_difference_variable = total_rent_cost_variable - total_mortgage_cost_variable
        
        # Calculate savings percentages with proper protection against division by zero and negative values
        savings_percent_fixed = Decimal('0')
        if total_rent_cost_fixed_period > Decimal('0'):
            savings_percent_fixed = (payment_difference_fixed / total_rent_cost_fixed_period * Decimal('100'))
            if savings_percent_fixed < Decimal('0'):
                savings_percent_fixed = Decimal('0')
        
        savings_percent_variable = Decimal('0')
        if total_rent_cost_variable > Decimal('0'):
            savings_percent_variable = (payment_difference_variable / total_rent_cost_variable * Decimal('100'))
            if savings_percent_variable < Decimal('0'):
                savings_percent_variable = Decimal('0')
        
        # Get max payment difference
        max_payment_difference = max((abs(mc.cumulative_investment) for mc in monthly_comparison), default=Decimal('0'))
        
        return ComparisonResult(
            monthly_comparison=monthly_comparison,
            yearly_summary=yearly_summary,
            total_mortgage_cost=total_mortgage_cost,
            total_rent_cost=total_rent_cost,
            total_investment_growth=total_investment_growth,
            net_benefit_buying=net_benefit_buying,
            max_payment_difference=max_payment_difference,
            is_buying_cheaper=net_benefit_buying > Decimal('0'),
            payment_difference_fixed=payment_difference_fixed,
            payment_difference_variable=payment_difference_variable,
            savings_percent_fixed=savings_percent_fixed,
            savings_percent_variable=savings_percent_variable,
            total_interest_paid=total_interest_paid,
            total_principal_paid=total_principal_paid
        )

    @staticmethod
    def _get_monthly_values(month: int, params: ComparisonParams, fixed_interest_duration_months: int) -> tuple:
        """Get monthly payment and interest rate values based on the month."""
        if month <= fixed_interest_duration_months:
            # First period (fixed rate)
            monthly_payment = params.mortgage_payments.monthly_payment_first_period
            monthly_interest = params.mortgage_params.interest_rate_first_period / Decimal('12')
        else:
            # Subsequent period (variable rate)
            if params.mortgage_params.fixed_interest_duration_years != params.mortgage_params.mortgage_term_years:
                monthly_payment = params.mortgage_payments.monthly_payment_subsequent
                monthly_interest = params.mortgage_params.interest_rate_subsequent / Decimal('12')
            else:
                # Both periods use the same rate
                monthly_payment = params.mortgage_payments.monthly_payment_first_period
                monthly_interest = params.mortgage_params.interest_rate_first_period / Decimal('12')

        return monthly_payment, monthly_interest