# RealEstimate Quick Start Guide

This guide will help you get started with RealEstimate quickly.

## Running with Docker (Recommended)

The fastest way to get started:

1. Make sure you have Docker and Docker Compose installed
2. Clone the repository and navigate to the project directory
3. Run:
   ```bash
   docker-compose up
   ```
4. Open your browser to http://localhost:8000

That's it! The application is now running and ready to use.

## Local Installation

If you prefer to run the application without Docker:

1. Make sure you have Python 3.9+ installed
2. Clone the repository and navigate to the project directory
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python main.py
   ```
6. Open your browser to http://localhost:8000

## CLI Demo Mode

To try a quick demonstration with pre-set values:

```bash
# With Docker:
docker run realestimate --cli

# Without Docker:
python main.py --cli
```

## Basic Usage

1. Enter the property price
2. Specify the down payment percentage
3. Enter interest rates for different periods
4. Enter your current monthly rent
5. Specify expected investment return rate
6. Click "Calculate" to see the comparison between buying and renting

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [DOCKER.md](DOCKER.md) for advanced Docker configuration
- Explore the calculation logic in the `/calculations` directory