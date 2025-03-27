from typing import NamedTuple
from dataclasses import dataclass
import numpy_financial as npf
from decimal import Decimal, getcontext

# Set decimal precision for financial calculations
getcontext().prec = 28

MONTHS_PER_YEAR = 12
MAX_PROPERTY_PRICE = 1000000000000  # 1 trillion (reasonable upper limit)

@dataclass
class MortgageParams:
    property_price: Decimal
    down_payment_percentage: Decimal
    interest_rate_first_period: Decimal
    interest_rate_subsequent: Decimal
    mortgage_term_years: int
    fixed_interest_duration_years: int

class MortgagePayments(NamedTuple):
    monthly_payment_first_period: Decimal
    monthly_payment_subsequent: Decimal
    loan_amount: Decimal
    fixed_interest_duration_months: int
    mortgage_term_months: int

class MortgageCalculator:
    @staticmethod
    def validate_input(params: MortgageParams) -> None:
        """Validate mortgage parameters with comprehensive error messages."""
        if params.property_price <= 0:
            raise ValueError("Property price must be greater than 0")
        if params.property_price > MAX_PROPERTY_PRICE:
            raise ValueError(f"Property price exceeds maximum allowed value of {MAX_PROPERTY_PRICE}")
        if not (0 <= params.down_payment_percentage <= 1):
            raise ValueError("Down payment percentage must be between 0 and 1")
        if params.interest_rate_first_period < 0:
            raise ValueError("First period interest rate cannot be negative")
        if params.interest_rate_subsequent < 0:
            raise ValueError("Subsequent interest rate cannot be negative")
        if params.mortgage_term_years <= 0:
            raise ValueError("Mortgage term must be greater than 0 years")
        if params.fixed_interest_duration_years < 0:
            raise ValueError("Fixed interest duration cannot be negative")
        if params.fixed_interest_duration_years > params.mortgage_term_years:
            raise ValueError("Fixed interest duration cannot exceed mortgage term")

    @staticmethod
    def calculate_loan_amount(property_price: Decimal, down_payment_percentage: Decimal) -> Decimal:
        """Calculate loan amount from property price and down payment percentage."""
        return property_price * (Decimal('1') - down_payment_percentage)

    @staticmethod
    def calculate_months(years: int) -> int:
        """Convert years to months."""
        return years * MONTHS_PER_YEAR

    @staticmethod
    def calculate_monthly_payment(loan_amount: Decimal, annual_interest_rate: Decimal, term_months: int) -> Decimal:
        """Calculate monthly mortgage payment with proper edge case handling."""
        try:
            # Handle zero or very small interest rates
            if annual_interest_rate <= Decimal('0.0000001'):  # Effectively zero
                return loan_amount / Decimal(term_months)
            
            # Convert to float for numpy_financial compatibility
            monthly_interest_rate = float(annual_interest_rate) / MONTHS_PER_YEAR
            loan_amount_float = float(loan_amount)
            
            # Calculate payment using numpy-financial
            payment = npf.pmt(monthly_interest_rate, term_months, -loan_amount_float)
            
            # Convert back to Decimal for precision
            return Decimal(str(payment))
        except Exception as e:
            raise ValueError(f"Error calculating monthly payment: {str(e)}")

    @staticmethod
    def calculate_remaining_balance(loan_amount: Decimal, annual_interest_rate: Decimal, 
                                    duration_months: int, monthly_payment: Decimal) -> Decimal:
        """Calculate remaining balance after fixed interest period."""
        try:
            # Handle zero or very small interest rates
            if annual_interest_rate <= Decimal('0.0000001'):  # Effectively zero
                return loan_amount - (monthly_payment * Decimal(duration_months))
            
            # Convert to float for numpy_financial compatibility
            monthly_interest_rate = float(annual_interest_rate) / MONTHS_PER_YEAR
            loan_amount_float = float(loan_amount)
            monthly_payment_float = float(monthly_payment)
            
            # Calculate future value using numpy-financial
            balance = npf.fv(monthly_interest_rate, duration_months, monthly_payment_float, -loan_amount_float)
            
            # Convert back to Decimal and ensure non-negative result
            return max(Decimal('0'), Decimal(str(balance)))
        except Exception as e:
            raise ValueError(f"Error calculating remaining balance: {str(e)}")

    @classmethod
    def calculate_mortgage_payments(cls, params: MortgageParams) -> MortgagePayments:
        """Calculate mortgage payments with all relevant parameters."""
        cls.validate_input(params)

        loan_amount = cls.calculate_loan_amount(params.property_price, params.down_payment_percentage)
        mortgage_term_months = cls.calculate_months(params.mortgage_term_years)
        fixed_interest_duration_months = cls.calculate_months(params.fixed_interest_duration_years)

        monthly_payment_first_period = cls.calculate_monthly_payment(
            loan_amount, params.interest_rate_first_period, mortgage_term_months)

        # Different calculation paths based on fixed interest duration
        if params.fixed_interest_duration_years != params.mortgage_term_years:
            remaining_balance = cls.calculate_remaining_balance(
                loan_amount, params.interest_rate_first_period, 
                fixed_interest_duration_months, monthly_payment_first_period
            )
            
            remaining_term_months = mortgage_term_months - fixed_interest_duration_months
            
            monthly_payment_subsequent = cls.calculate_monthly_payment(
                remaining_balance, params.interest_rate_subsequent, remaining_term_months)
        else:
            monthly_payment_subsequent = monthly_payment_first_period

        return MortgagePayments(
            monthly_payment_first_period,
            monthly_payment_subsequent,
            loan_amount,
            fixed_interest_duration_months,
            mortgage_term_months
        )