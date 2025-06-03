# -*- coding: utf-8 -*-
"""
Created on Mon May 26 20:27:04 2025

@author: Rahul
"""

import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Get API key and email from environment variables
api_key = os.getenv("API_KEY")
email = os.getenv("EMAIL")

# Common Parameters for API call
base_url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
start_date = "20140101" # Start date for query params (format: YYYYMMDD)
end_date = "20201231" # End date for query params (format: YYYYMMDD)
state_code = '06' # State code for California
county_code = '037' # County code for LA
start_year = 2014
end_year = 2024

# Check if credentials are loaded
if not api_key or not email:
    raise ValueError("API_KEY or EMAIL not found in .env file. Please set them.")

# Define dictionary for data types and their parameter codes
data_types = {
    "pm25": "88101",        # PM2.5 FRM/FEM Mass
    "pm10": "81102",        # PM10 Mass
    "ozone": "44201",       # Ozone
    "temperature": "62101", # Temperature
    "wind_speed": "61103",  # Resultant Wind Speed
    "wind_direction": "61104", # Resultant Wind Direction
    "rh": "62201",          # Relative Humidity
}

# Output directory
output_dir = "raw_data/"
os.makedirs(output_dir, exist_ok=True)

# Function to generate 1-year date ranges
def generate_yearly_ranges(start_year, end_year):
    date_ranges = []
    for year in range(start_year, end_year + 1):
        bdate = f"{year}0101"  # January 1st
        edate = f"{year}1231"  # December 31st
        date_ranges.append((bdate, edate))
    return date_ranges

# Function to fetch data from the API for a given date range
def fetch_data(parameter_code, data_type, bdate, edate):
    params = {
        "email": email,
        "key": api_key,
        "param": parameter_code,
        "bdate": bdate,
        "edate": edate,
        "state": state_code,
        "county": county_code
    }
    
    try:
        print(f"Fetching {data_type} data for {bdate} to {edate}...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["Header"][0]["status"] != "Success":
            print(f"Failed to fetch {data_type}: {data['Header'][0]['error']}")
            return None
        
        records = data["Data"]
        if not records:
            print(f"No {data_type} data found for LA ({bdate} to {edate}).")
            return None
        
        df = pd.DataFrame(records)
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {data_type} data: {e}")
        return None

# Function to save DataFrame as CSV
def save_to_csv(df, data_type):
    if df is not None:
        filename = os.path.join(output_dir, f"la_{data_type}_2014_2024.csv")
        df.to_csv(filename, index=False)
        print(f"Saved {data_type} data to {filename}")
    else:
        print(f"No data to save for {data_type}")

# Main script to fetch and save all data
def main():
    
    # Generate 1-year date ranges (2014, 2015, ..., 2024)
    date_ranges = generate_yearly_ranges(start_year, end_year)
    
    # Fetch pollutants and meteorological data
    for data_type, param_code in data_types.items():
        dfs = []
        for bdate, edate in date_ranges:
            df = fetch_data(param_code, data_type, bdate, edate)
            if df is not None:
                dfs.append(df)
            time.sleep(1)  # Avoid rate limits
        # Combine data for this data type across all years
        combined_df = pd.concat(dfs) if dfs else None
        save_to_csv(combined_df, data_type)

main()
