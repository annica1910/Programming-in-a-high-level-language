from datetime import date
from typing import List, Optional

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date

@app.get("/")
def get_html(
        request: Request, 
        location_codes : dict = LOCATION_CODES, 
        today : date = date.today()
    ):
    return templates.TemplateResponse(name="strompris.html", 
        context={   
            "request" : request, 
            "location_codes" : location_codes,
            "today" : today
        })


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

@app.get("/plot_prices.json")
def plot_prices_json(
        locations: List[str] = Query(default=list(LOCATION_CODES.keys())),
        end : date = date.today(), 
        days : int = 7
    ):
    df = fetch_prices(end, days, locations)
    return plot_prices(df).to_dict()

# mount your docs directory as static files at `/help`

app.mount("/help", StaticFiles(directory="build/html", html=True), name="help") # mounting all html files in build

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000
    uvicorn.run(app, host="127.0.0.1", port=5000)

