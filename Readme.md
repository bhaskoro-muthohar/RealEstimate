# Real Estate Calculator API

This is a Flask-based web API for real estate calculations. It provides endpoints for calculating mortgage payments and performing a month-by-month comparison of costs.

## Project Structure

.
├── .gitignore  
├── app.py  
├── calculations  
│   ├── __init__.py  
│   ├── comparison.py  
│   └── mortgage_calculations.py  
├── main.py  
└── realEstimate.py  

## Setup

1. Clone the repository:

```sh
git clone <repository-url>
```
2. Navigate to the project directory:
```cd <project-directory>```

3. Create a virtual environment:
```python3 -m venv venv```

4. Activate the virtual environment:
On Windows:
```venv\Scripts\activate```

On Unix or MacOS:
```source venv/bin/activate```

5. Install the required packages:
```pip install -r requirements.txt```

### Running the Application
To run the application, use the following command:

```python app.py```

This will start a development server on http://localhost:5000.

### API Endpoints
*Calculate Mortgage Payments*
URL: `/calculate_mortgage_payments`

Method: `POST`

Data Params:
```
{
    "property_price": <property_price>,
    "down_payment_percentage": <down_payment_percentage>,
    "interest_rate_first_period": <interest_rate_first_period>,
    "interest_rate_subsequent_min": <interest_rate_subsequent_min>,
    "interest_rate_subsequent_max": <interest_rate_subsequent_max>,
    "mortgage_term_years": <mortgage_term_years>,
    "fixed_interest_duration_years": <fixed_interest_duration_years>
}
```

*Month by Month Comparison*
URL: `/month_by_month_comparison`

Method: `POST`

Data Params:
```
{
    "monthly_payment_first_period": <monthly_payment_first_period>,
    "monthly_payment_subsequent_min": <monthly_payment_subsequent_min>,
    "monthly_payment_subsequent_max": <monthly_payment_subsequent_max>,
    "monthly_rent": <monthly_rent>,
    "mortgage_term_years": <mortgage_term_years>,
    "loan_amount": <loan_amount>,
    "interest_rate_first_period": <interest_rate_first_period>,
    "interest_rate_subsequent_min": <interest_rate_subsequent_min>,
    "interest_rate_subsequent_max": <interest_rate_subsequent_max>,
    "fixed_interest_duration_years": <fixed_interest_duration_years>
}
```
