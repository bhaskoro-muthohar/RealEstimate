from flask import Flask, request, jsonify, render_template
from calculations.mortgage_calculations import calculate_mortgage_payments
from calculations.comparison import month_by_month_comparison

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/calculate_mortgage_payments', methods=['POST'])
def mortgage_payments():
    # Get form data
    property_price = float(request.form.get('property_price'))
    down_payment_percentage = float(request.form.get('down_payment_percentage'))
    interest_rate_first_period = float(request.form.get('interest_rate_first_period'))
    interest_rate_subsequent_min = float(request.form.get('interest_rate_subsequent_min'))
    interest_rate_subsequent_max = float(request.form.get('interest_rate_subsequent_max'))
    mortgage_term_years = int(request.form.get('mortgage_term_years'))
    fixed_interest_duration_years = int(request.form.get('fixed_interest_duration_years'))
    monthly_rent = float(request.form.get('monthly_rent'))

    # Call calculate_mortgage_payments
    (
        monthly_payment_first_period,
        monthly_payment_subsequent_min,
        monthly_payment_subsequent_max,
        loan_amount,
    ) = calculate_mortgage_payments(
        property_price,
        down_payment_percentage,
        interest_rate_first_period,
        interest_rate_subsequent_min,
        interest_rate_subsequent_max,
        mortgage_term_years,
        fixed_interest_duration_years,
    )

    # Call month_by_month_comparison
    (
        monthly_comparison,
        total_principal_paid,
        total_interest_paid_min,
        total_interest_paid_max,
        total_rent_and_savings_paid,
    ) = month_by_month_comparison(
        monthly_payment_first_period,
        monthly_payment_subsequent_min,
        monthly_payment_subsequent_max,
        monthly_rent,
        mortgage_term_years,
        loan_amount,
        interest_rate_first_period,
        interest_rate_subsequent_min,
        interest_rate_subsequent_max,
        fixed_interest_duration_years,
    )

    # Output Summary
    total_difference_min = (
        total_principal_paid + total_interest_paid_min 
        - total_rent_and_savings_paid
    )
    total_difference_max = (
        total_principal_paid + total_interest_paid_max 
        - total_rent_and_savings_paid
    )

    # Create result dictionary
    results = {
        'total_principal_paid': total_principal_paid,
        'total_interest_paid_min': total_interest_paid_min,
        'total_interest_paid_max': total_interest_paid_max,
        'total_rent_and_savings_paid': total_rent_and_savings_paid,
        'total_difference_min': total_difference_min,
        'total_difference_max': total_difference_max,
        'monthly_comparison': monthly_comparison
    }

    return render_template('results.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
