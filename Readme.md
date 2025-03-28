# RealEstimate: Real Estate Calculator

A FastAPI-based web application for real estate calculations, providing a user-friendly interface for mortgage payment calculations and rent vs. buy comparisons with investment return analysis.

## Table of Contents
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Running the Application](#running-the-application)
- [Features](#features)
- [Calculation Logic](#calculation-logic)
- [Recent Improvements](#recent-improvements)
- [API Endpoints](#api-endpoints)

## Project Structure
```
.
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── Readme.md
├── app.py
├── calculations
│   ├── __init__.py
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

### Local Setup

1. Clone the repository:
   ```
     git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
     cd <project-directory>
   ```

3. Create a virtual environment:
   ```
     python3 -m venv venv
   ```

4. Activate the virtual environment:
     - On Windows:
     ```
       venv\Scripts\activate
     ```
     - On Unix or MacOS:
     ```
       source venv/bin/activate
     ```

5. Install the required packages:
   ```
     pip install -r requirements.txt
   ```

### Docker Setup

1. Clone the repository:
   ```
     git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
     cd <project-directory>
   ```

3. Build and run using Docker Compose:
   ```
     docker-compose up --build
   ```
   
   This will build the Docker image and start the container, making the application available at `http://localhost:8000`.

4. Alternatively, you can build and run the Docker container manually:
   ```
     docker build -t realestimate .
     docker run -p 8000:8000 realestimate
   ```

## Running the Application

### Web Interface

To run the web application locally:

```bash
python main.py
```

This will start the FastAPI server on `http://localhost:8000`.

### CLI Mode

For a quick demonstration without the web interface:

```bash
python main.py --cli
```

### Docker Mode

Using Docker Compose:
```bash
docker-compose up
```

Or using Docker directly:
```bash
docker run -p 8000:8000 realestimate
```

To run in CLI mode with Docker:
```bash
docker run realestimate python main.py --cli
```

## Features

1. **User-friendly Web Interface**: Input mortgage parameters through a clean, responsive HTML form.
2. **Mortgage Payment Calculation**: Calculates monthly mortgage payments for both fixed and variable interest rate periods.
3. **Rent vs. Buy Comparison**: Provides a detailed month-by-month comparison of costs associated with renting versus buying.
4. **Investment Return Analysis**: Calculates potential investment returns on the difference between rent and mortgage payments.
5. **Comprehensive Results**: Displays total principal paid, total interest paid (min and max), investment growth, and overall financial outcomes.
6. **High-precision Calculations**: Uses Decimal for accurate financial calculations instead of floating-point.
7. **Containerized Deployment**: Easy deployment with Docker.

## Calculation Logic

This application uses the loan amortization formula to calculate monthly mortgage payments. The formula is as follows:

$$M = P[r(1+r)^n]/[(1+r)^n – 1]$$

Where:
- M is your monthly payment.
- P is the principal loan amount.
- r is your monthly interest rate, calculated by dividing your annual interest rate by 12.
- n is your number of payments (the number of months you will be paying the loan).

The application uses the following key calculations:

1. **Monthly Mortgage Payment**:
   Calculated using the standard amortization formula with provisions for zero or near-zero interest rates.

2. **Investment Growth**:
   If renting, the difference between mortgage and rent payments is invested with compound growth.

3. **Total Wealth Comparison**:
   Compares potential wealth accumulation between buying (property value minus interest) vs renting (investment returns).

4. **Net Benefit Analysis**:
   Calculates the net financial benefit of buying vs renting across best and worst case scenarios.

The results are presented in both summary and detailed formats, allowing users to make informed decisions about renting versus buying property.

## Recent Improvements

The latest version includes significant improvements to the calculation logic:

1. **Decimal-based Precision**: Replaced floating-point with Decimal for precise financial calculations
2. **Edge Case Handling**: Added proper handling for zero interest rates and other edge cases
3. **Input Validation**: Comprehensive input validation with meaningful error messages
4. **Overflow Protection**: Added upper limits to prevent numeric overflow in large calculations
5. **Fixed Wealth Calculations**: Corrected min/max wealth calculation logic for proper scenario analysis
6. **Efficient Algorithms**: Optimized calculation approaches to eliminate redundant operations
7. **Consistent Percentage Handling**: Standardized percentage conversions throughout the codebase
8. **Improved Investment Calculations**: Fixed compounding logic for more accurate investment growth projections
9. **Better Exception Handling**: Added comprehensive try/except blocks with appropriate error responses
10. **Containerization**: Added Docker support for easy deployment

For more detailed information about the calculations, please refer to the `calculations` directory in the source code.

## API Endpoints

### Calculate Mortgage Payments

Calculate monthly mortgage payments based on given parameters.

- **URL:** `/calculate_mortgage_payments`
- **Method:** `POST`
- **Data Params:**
  ```
    {
      "property_price": 300000,
      "down_payment_percentage": 20,
      "interest_rate_first_period": 3.5,
      "interest_rate_subsequent": 4.0,
      "mortgage_term_years": 30,
      "fixed_interest_duration_years": 5,
      "monthly_rent": 1200,
      "investment_return_rate": 6.0
    }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:** HTML page with detailed results

## Development

### Running Tests

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=.
```

### Docker Development Mode

For development with live reloading:

```bash
docker-compose up --build
```

The volume mapping in the `docker-compose.yml` file allows you to edit files locally and see changes reflected in the running container.

Inspired by: https://www.rumah123.com/kpr/simulasi-kpr/