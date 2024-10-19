# Real Estate Calculator API

A Flask-based web API for real estate calculations, providing endpoints for mortgage payment calculations and month-by-month cost comparisons.

## Table of Contents
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
    - [Calculate Mortgage Payments](#calculate-mortgage-payments)
    - [Month by Month Comparison](#month-by-month-comparison)
- [Mortgage Calculation Logic](#mortgage-calculation-logic)

## Project Structure
```
.
├── LICENSE
├── Readme.md
├── app.py
├── calculations
│   ├── comparison.py
│   └── mortgage_calculations.py
├── main.py
├── realEstimate.py
├── requirements.txt
└── templates
   ├── index.html
   └── results.html
```


## Setup

1. Clone the repository:
   
     git clone <repository-url>
   

2. Navigate to the project directory:
   
     cd <project-directory>
   

3. Create a virtual environment:
   
     python3 -m venv venv
   

4. Activate the virtual environment:
     - On Windows:
     
       venv\Scripts\activate
     
     - On Unix or MacOS:
     
       source venv/bin/activate
     

5. Install the required packages:
   
     pip install -r requirements.txt
   

## Running the Application

To run the application, use the following command:


python app.py


This will start a development server on `http://localhost:5000`.

## API Endpoints

### Calculate Mortgage Payments

Calculate monthly mortgage payments based on given parameters.

- **URL:** `/calculate_mortgage_payments`
- **Method:** `POST`
- **Data Params:**
  
    {
      "property_price": 300000,
      "down_payment_percentage": 20,
      "interest_rate_first_period": 3.5,
      "interest_rate_subsequent_min": 3.0,
      "interest_rate_subsequent_max": 4.0,
      "mortgage_term_years": 30,
      "fixed_interest_duration_years": 5
    }
  
- **Success Response:**
    - **Code:** 200
    - **Content:**
    
      {
        "monthly_payment_first_period": 1077.71,
        "monthly_payment_subsequent_min": 1010.92,
        "monthly_payment_subsequent_max": 1145.80
      }
    

### Month by Month Comparison

Perform a month-by-month comparison of mortgage costs versus renting.

- **URL:** `/month_by_month_comparison`
- **Method:** `POST`
- **Data Params:**
  
    {
      "monthly_payment_first_period": 1077.71,
      "monthly_payment_subsequent_min": 1010.92,
      "monthly_payment_subsequent_max": 1145.80,
      "monthly_rent": 1200,
      "mortgage_term_years": 30,
      "loan_amount": 240000,
      "interest_rate_first_period": 3.5,
      "interest_rate_subsequent_min": 3.0,
      "interest_rate_subsequent_max": 4.0,
      "fixed_interest_duration_years": 5
    }
  
- **Success Response:**
    - **Code:** 200
    - **Content:**
    
      {
        "comparison": [
          {
            "month": 1,
            "mortgage_payment": 1077.71,
            "rent_payment": 1200,
            "principal_paid": 352.71,
            "interest_paid": 725.00,
            "cumulative_principal_paid": 352.71,
            "cumulative_interest_paid": 725.00,
            "remaining_loan_balance": 239647.29
          },
          // ... (data for subsequent months)
        ]
      }
    

## Mortgage Calculation Logic

This API uses the loan amortization formula to calculate monthly mortgage payments. The formula is as follows:


M = P[r(1+r)^n]/[(1+r)^n – 1]


Where:
- M is your monthly payment.
- P is the principal loan amount.
- r is your monthly interest rate, calculated by dividing your annual interest rate by 12.
- n is your number of payments (the number of months you will be paying the loan).

Inspired by: https://www.rumah123.com/kpr/simulasi-kpr/