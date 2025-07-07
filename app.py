import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet
import numpy as np

st.title("Spare Parts Demand Visualizer + Forecast")

uploaded_file = st.file_uploader("Upload sales CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    
    # Show raw data
    st.subheader("Raw Data")
    st.dataframe(df)
    
    # SKU selector
    sku_list = df["sku"].unique()
    sku = st.selectbox("Select SKU to visualize", sku_list)
    
    # Filter by SKU
    sku_df = df[df["sku"] == sku]
    daily_sales = sku_df.groupby("date")["quantity"].sum().reset_index()
    
    # Plot historical demand
    st.subheader("Historical Demand")
    plt.figure(figsize=(10,4))
    plt.plot(daily_sales["date"], daily_sales["quantity"])
    plt.xlabel("Date")
    plt.ylabel("Quantity Sold")
    plt.title(f"{sku} Demand")
    st.pyplot(plt)
    
    # Prepare data for Prophet
    prophet_df = daily_sales.rename(columns={"date": "ds", "quantity": "y"})
    
    # Fit and forecast
    model = Prophet(growth="linear")
    model.fit(prophet_df.assign(y = prophet_df["y"].clip(lower=1)).assign(y = np.log(prophet_df["y"].clip(lower=1))))
    
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    forecast['yhat'] = np.exp(forecast['yhat'])
    forecast['yhat_lower'] = np.exp(forecast['yhat_lower'])
    forecast['yhat_upper'] = np.exp(forecast['yhat_upper'])
    
    # Filter to 30 days before + after last date
    last_date = pd.to_datetime(df['date'].max())
    start = last_date - pd.Timedelta(days=30)
    end = last_date + pd.Timedelta(days=30)
    
    forecast_filtered = forecast[(forecast['ds'] >= start) & (forecast['ds'] <= end)]
    actual_filtered = prophet_df[(prophet_df['ds'] >= start)]
    
    # Plot manually with matplotlib
    st.subheader("Forecast (Zoomed View)")
    plt.figure(figsize=(10, 5))
    plt.plot(forecast_filtered['ds'], forecast_filtered['yhat'], label='Forecast', color='blue')
    plt.fill_between(forecast_filtered['ds'],
                     forecast_filtered['yhat_lower'],
                     forecast_filtered['yhat_upper'],
                     color='lightblue', alpha=0.5, label='Confidence Interval')
    plt.scatter(actual_filtered['ds'], actual_filtered['y'], color='black', s=20, label='Actual')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xlabel("Date (MM-DD)")
    plt.ylabel("Quantity")
    plt.title(f"{sku} Forecast: 30 Days Before and After")
    plt.legend()
    plt.grid(True)
    
    st.pyplot(plt)
    
    # Download forecast data
    st.subheader("Download forecast data")
    forecast_out = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    st.write(forecast_out.tail(30))
    csv = forecast_out.to_csv(index=False)
    st.download_button("Download CSV", csv, "forecast.csv", "text/csv")
