"""
OpenAI API example function: https://platform.openai.com/docs/guides/function-calling
This function returns the current weather in a given location as a 24-hour forecast.
The function is called by the OpenAI API and returns a JSON object.

Geocoding: Google Maps API
Documentation:
- https://developers.google.com/maps/documentation/geocoding/overview
- https://pypi.org/project/googlemaps/
- https://github.com/googlemaps/google-maps-services-python


Open-Meteo API:
Documentation:  https://open-meteo.com/en/docs
                https://pypi.org/project/openmeteo-requests/

The Open-Meteo API is used to get the weather data. The API is rate-limited to 1 request per second.
It is called with the openmeteo_requests Python package, which is a wrapper for the
requests package. It is used to cache the API responses to avoid repeated API calls, 
and to retry failed API calls.
"""

import os
import json
from logging import getLogger

import googlemaps
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


logger = getLogger(__name__)


# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_API_CACHE_SESSION = requests_cache.CachedSession(
    "/tmp/.cache", expire_after=3600
)  # nosec
WEATHER_API_RETRY_SESSION = retry(
    WEATHER_API_CACHE_SESSION, retries=5, backoff_factor=0.2
)


# Google Maps API key
gmaps = None
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
try:
    gmaps = googlemaps.Client(key=api_key)
# pylint: disable=broad-exception-caught
except ValueError as value_error:
    logger.error(
        "Could not initialize Google Maps API. Setup the Google Geolocation "
        "API service: https://developers.google.com/maps/documentation/geolocation/overview."
        "Add your GOOGLE_MAPS_API_KEY to .env: %s"
    )

openmeteo = openmeteo_requests.Client(session=WEATHER_API_RETRY_SESSION)


def weather_tool_factory() -> dict:
    """Return a list of tools that can be called by the OpenAI API"""
    tool = {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["METRIC", "USCS"]},
                },
                "required": ["location"],
            },
        },
    }
    return tool

def get_current_weather(location, unit="METRIC") -> str:
    """Get the current weather in a given location as a 24-hour forecast"""
    if gmaps is None:
        retval = {
            "error": "Google Maps Geolocation service is not initialized. "
            "Setup the Google Geolocation API service: "
            "https://developers.google.com/maps/documentation/geolocation/overview, "
            "and add your GOOGLE_MAPS_API_KEY to .env"
        }
        return json.dumps(retval)

    unit = unit or "METRIC"
    location = location or "Cambridge, MA, near Kendall Square"
    latitude: float = 0.0
    longitude: float = 0.0
    address: str = None

    # use Google Maps API to get the latitude and longitude of the location
    try:
        geocode_result = gmaps.geocode(location)
        latitude = geocode_result[0]["geometry"]["location"]["lat"] or 0
        longitude = geocode_result[0]["geometry"]["location"]["lng"] or 0
        address = geocode_result[0]["formatted_address"]
    except googlemaps.exceptions.ApiError as api_error:
        logger.error(
            "Google Maps API error getting geo coordinates for %s: %s",
            location,
            api_error,
        )
    # pylint: disable=broad-exception-caught
    except Exception as e:
        logger.error(
            "An unexpected error occurred while getting geo coordinates for %s: %s",
            location,
            e,
        )

    logger.info(
        "Using Google Maps API to get geo coordinates for %s: %s, %s, %s",
        location,
        latitude,
        longitude,
        address or "No address found",
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "precipitation"],
        "current": ["temperature_2m"],
    }
    responses = openmeteo.weather_api(WEATHER_API_URL, params=params)
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_2m = hourly.Variables(1).ValuesAsNumpy()
    if unit.upper() == "USCS":
        hourly_temperature_2m = hourly_temperature_2m * 9 / 5 + 32
        hourly_precipitation_2m = hourly_precipitation_2m / 2.54

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["temperature"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation_2m
    hourly_dataframe = pd.DataFrame(data=hourly_data).head(
        24
    )  # Only return the first 24 hours
    hourly_dataframe["date"] = hourly_dataframe["date"].dt.strftime("%Y-%m-%d %H:%M")
    hourly_json = hourly_dataframe.to_json(orient="records")
    return json.dumps(hourly_json)
