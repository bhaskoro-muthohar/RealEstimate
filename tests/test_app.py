from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_index_renders_calculator():
    response = client.get("/")

    assert response.status_code == 200
    assert "Mortgage Calculator" in response.text


def test_mortgage_calculation_renders_results():
    response = client.post(
        "/calculate_mortgage_payments",
        data={
            "property_price": "300000000",
            "down_payment_percentage": "20",
            "interest_rate_first_period": "3.5",
            "interest_rate_subsequent": "4",
            "mortgage_term_years": "30",
            "fixed_interest_duration_years": "5",
            "monthly_rent": "1200000",
            "investment_return_rate": "6",
        },
    )

    assert response.status_code == 200
    assert "Results" in response.text
