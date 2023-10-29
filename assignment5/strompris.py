#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
import datetime
from datetime import date, timedelta


from altair import Chart
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: date = date.today(), location: str = "NO1"):
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Make sure to document arguments and return value...
    ...
    """
    assert date >= datetime.date(2022, 10, 2) 

    # get the month and day from the date
    format_dt = date.strftime('%m-%d')
    # extract data from the url
    url = "https://www.hvakosterstrommen.no/api/v1/prices/{}/{}_{}.json".format(date.year, format_dt, location)
    r = requests.get(url)
    json = r.json()
    # transform into DataFrame with desired cols
    df = pd.DataFrame(json, columns=['NOK_per_kWh', 'time_start'])
    # format the date correctly
    df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")
    if format_dt == "10-30":
        df['time_start'][3:23] += timedelta(hours=1)
    return df

# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1" : "Oslo",
    "NO2" : "Kristiansand",
    "NO3" : "Trondheim",
    "NO4" : "Tromso",
    "NO5" : "Bergen",
}

# task 1:


def fetch_prices(
    end_date: date = date.today(),
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
):
    """Fetch prices for multiple days and locations into a single DataFrame

    Make sure to document arguments and return value...
    ...
    """
    # looping from start-date to end-date
    # extracting data day by day{}
    frames = []
    for i in range(days, 0, -1):
        dt = end_date - timedelta(days=i-1)     #start-date is days+1 before end-date
        # collect data for every location in a list
        date_prices = [fetch_day_prices(dt, loc).assign(location_code=loc, location=LOCATION_CODES.get(loc)) for loc in locations]
        # transform list of dfs into one df
        frames.append(pd.concat(date_prices))    
    df = pd.concat(frames)
    return df

# task 5.1:


def plot_prices(df: pd.DataFrame):
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value...
    """
    c = Chart(df).mark_line().encode(
        x='time_start', 
        y='NOK_per_kWh',
        color='location'
    )
    return c


# Task 5.4 (IN4110)


def plot_daily_prices(df: pd.DataFrame):
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    c = Chart(df).mark_line().encode(
        x='time_start', 
        y='NOK_per_kWh',
        color='location'
    )
    return c


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
):
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices(datetime.date(2022, 10, 30), days=2, locations=["NO1"]) #savings day
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
