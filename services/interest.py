from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_months_diff(start_date: datetime, end_date: datetime) -> float:
    # Calculate difference in months (including fractional months if needed, but usually simple months)
    # Using relative delta for precise month calculation
    delta = relativedelta(end_date, start_date)
    months = delta.years * 12 + delta.months + (delta.days / 30.0) # Approx days
    return max(0, months)

def calculate_simple_interest(principal: float, rate_per_month: float, start_date: datetime, end_date: datetime) -> dict:
    months = calculate_months_diff(start_date, end_date)
    interest = principal * (rate_per_month / 100) * months
    return {
        "principal": principal,
        "rate": rate_per_month,
        "months": months,
        "interest": interest,
        "total_amount": principal + interest
    }

def calculate_compound_interest(principal: float, rate_per_month: float, start_date: datetime, end_date: datetime) -> dict:
    # A = P * (1 + r/100)^n
    months = calculate_months_diff(start_date, end_date)
    amount = principal * ((1 + rate_per_month / 100) ** months)
    interest = amount - principal
    return {
        "principal": principal,
        "rate": rate_per_month,
        "months": months,
        "interest": interest,
        "total_amount": amount
    }

def calculate_interest(principal: float, rate_per_month: float, start_date: datetime, end_date: datetime = None, interest_type: str = "Simple") -> dict:
    if end_date is None:
        end_date = datetime.utcnow()
    
    if interest_type.lower() == "compound":
        return calculate_compound_interest(principal, rate_per_month, start_date, end_date)
    else:
        return calculate_simple_interest(principal, rate_per_month, start_date, end_date)
