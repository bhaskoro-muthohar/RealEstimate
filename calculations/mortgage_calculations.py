from typing import NamedTuple
from dataclasses import dataclass
import numpy_financial as npf

MONTHS_PER_YEAR = 12

@dataclass
class MortgageParams:
    property_price: float
    down_payment_percentage: float
    interest_rate_first_period: float
    interest_rate_subsequent_min: float
    interest_rate_subsequent_max: float
    mortgage_term_years: int
    fixed_interest_duration_years: int

class MortgagePayments(NamedTuple):
    monthly_payment_first_period: float
    monthly_payment_subsequent_min: float
    monthly_payment_subsequent_max: float
    loan_amount: float

class MortgageCalculator:
    @staticmethod
    def validate_input(params: MortgageParams) -> None:
        if (params.property_price <= 0 or
            not (0 <= params.down_payment_percentage <= 1) or
            params.interest_rate_first_period < 0 or
            params.interest_rate_subsequent_min < 0 or
            params.interest_rate_subsequent_max < 0 or
            params.mortgage_term_years <= 0 or
            params.fixed_interest_duration_years < 0):
            raise ValueError("Invalid input parameters")

    @staticmethod
    def calculate_loan_amount(property_price: float, down_payment_percentage: float) -> float:
        return property_price * (1 - down_payment_percentage)

    @staticmethod
    def calculate_months(years: int) -> int:
        return years * MONTHS_PER_YEAR

    @staticmethod
    def calculate_monthly_payment(loan_amount: float, annual_interest_rate: float, term_months: int) -> float:
        try:
            monthly_interest_rate = annual_interest_rate / MONTHS_PER_YEAR
            return npf.pmt(monthly_interest_rate, term_months, -loan_amount)
        except Exception as e:
            raise ValueError(f"Error calculating monthly payment: {str(e)}")

    @staticmethod
    def calculate_remaining_balance(loan_amount: float, annual_interest_rate: float, duration_months: int, monthly_payment: float) -> float:
        monthly_interest_rate = annual_interest_rate / MONTHS_PER_YEAR
        return npf.fv(monthly_interest_rate, duration_months, monthly_payment, -loan_amount)

    @classmethod
    def calculate_mortgage_payments(cls, params: MortgageParams) -> MortgagePayments:
        cls.validate_input(params)

        loan_amount = cls.calculate_loan_amount(params.property_price, params.down_payment_percentage)
        mortgage_term_months = cls.calculate_months(params.mortgage_term_years)
        fixed_interest_duration_months = cls.calculate_months(params.fixed_interest_duration_years)

        monthly_payment_first_period = cls.calculate_monthly_payment(loan_amount, params.interest_rate_first_period, mortgage_term_months)

        if params.fixed_interest_duration_years != params.mortgage_term_years:
            remaining_balance = cls.calculate_remaining_balance(loan_amount, params.interest_rate_first_period, fixed_interest_duration_months, monthly_payment_first_period)
            monthly_payment_subsequent_min = cls.calculate_monthly_payment(remaining_balance, params.interest_rate_subsequent_min, mortgage_term_months - fixed_interest_duration_months)
            monthly_payment_subsequent_max = cls.calculate_monthly_payment(remaining_balance, params.interest_rate_subsequent_max, mortgage_term_months - fixed_interest_duration_months)
        else:
            monthly_payment_subsequent_min = monthly_payment_subsequent_max = monthly_payment_first_period

        return MortgagePayments(
            monthly_payment_first_period,
            monthly_payment_subsequent_min,
            monthly_payment_subsequent_max,
            loan_amount
        )