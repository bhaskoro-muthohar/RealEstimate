from flask import Flask, request, jsonify, render_template
from calculations.mortgage_calculations import calculate_mortgage_payments
from calculations.comparison import month_by_month_comparison

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/calculate_mortgage_payments", methods=["POST"])
def mortgage_payments():
    data = request.form
    data = request.get_json()
    property_price = data.get("property_price")
    down_payment_percentage = data.get("down_payment_percentage")
    interest_rate_first_period = data.get("interest_rate_first_period")
    interest_rate_subsequent_min = data.get("interest_rate_subsequent_min")
    interest_rate_subsequent_max = data.get("interest_rate_subsequent_max")
    mortgage_term_years = data.get("mortgage_term_years")
    fixed_interest_duration_years = data.get("fixed_interest_duration_years")

    result = calculate_mortgage_payments(
        property_price,
        down_payment_percentage,
        interest_rate_first_period,
        interest_rate_subsequent_min,
        interest_rate_subsequent_max,
        mortgage_term_years,
        fixed_interest_duration_years,
    )

    return render_template('results.html', result=result)


@app.route("/month_by_month_comparison", methods=["POST"])
def comparison():
    data = request.get_json()
    monthly_payment_first_period = data.get("monthly_payment_first_period")
    monthly_payment_subsequent_min = data.get("monthly_payment_subsequent_min")
    monthly_payment_subsequent_max = data.get("monthly_payment_subsequent_max")
    monthly_rent = data.get("monthly_rent")
    mortgage_term_years = data.get("mortgage_term_years")
    loan_amount = data.get("loan_amount")
    interest_rate_first_period = data.get("interest_rate_first_period")
    interest_rate_subsequent_min = data.get("interest_rate_subsequent_min")
    interest_rate_subsequent_max = data.get("interest_rate_subsequent_max")
    fixed_interest_duration_years = data.get("fixed_interest_duration_years")

    result = month_by_month_comparison(
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

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
