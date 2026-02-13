# F1 Driver Standings CLI

This is a command-line application built with Python that retrieves Formula 1 driver standings for a select season using the Jolpica API.

I built this project to practice working with external APIs, data processing, and structuring a Python app. It helped me strengthen my understanding of HTTP requests, JSON parsing, error handling, and presenting structured data using pandas.

## Features
- Retrieve real F1 season data from a public API
- Input validation for season year (1950–2025)
- Basic API error handling
- Cleanly formatted standings output using pandas

## What I Learned
- How to make HTTP requests with `requests`
- How to handle JSON API responses
- Structuring code using classes and helper functions
- Basic retry handling for API calls
- Organizing a Python project with virtual environments and dependencies

## Tech Stack
- Python
- pandas
- requests

## Running the App

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python app.py
