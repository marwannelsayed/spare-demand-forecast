# Spare Parts Demand Visualizer + Forecast

This application allows you to visualize historical sales data for spare parts and generate demand forecasts using Prophet, all through an interactive Streamlit interface.

## Features
- Upload your sales CSV file (with columns: date, sku, quantity)
- Visualize raw data and historical demand for any SKU
- Forecast demand for the next 30 days using Prophet
- Download forecast results as CSV

## Requirements
- Python 3.7+
- See `requirements.txt` for dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

1. Upload your sales CSV file (must have columns: `date`, `sku`, `quantity`)
2. Select an SKU to visualize
3. View historical demand and forecast plot (shows 30 days before and after the last date)
4. Download the forecast as a CSV file

## Example CSV Format
```csv
date,sku,quantity
2023-01-01,A123,10
2023-01-02,A123,12
2023-01-01,B456,5
...
```

## Notes
- The forecast plot displays 30 days before and 30 days after the last date in your data.
- Make sure your CSV file uses ISO date format (YYYY-MM-DD).