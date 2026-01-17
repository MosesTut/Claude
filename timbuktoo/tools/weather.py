"""Weather API integration"""

import requests
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

from ..utils.logger import get_logger

logger = get_logger(__name__)


class WeatherTool:
    """Fetches real-time weather data and forecasts"""

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = {}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def get_forecast(
        self,
        city: str,
        country: str,
        start_date: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a city

        Returns:
        {
            "city": "Lisbon",
            "country": "Portugal",
            "forecast": [
                {
                    "date": "2024-06-01",
                    "temp_high_c": 25,
                    "temp_low_c": 18,
                    "conditions": "Sunny",
                    "precipitation_chance": 10,
                    "wind_speed_kmh": 15
                }
            ]
        }
        """

        cache_key = f"{city}_{country}_{start_date}_{days}"
        if cache_key in self.cache:
            logger.info(f"Weather cache hit for {city}")
            return self.cache[cache_key]

        try:
            if not self.api_key:
                logger.warning("No weather API key, returning mock data")
                return self._get_mock_forecast(city, country, start_date, days)

            # Call OpenWeatherMap API
            # Using 5-day forecast endpoint (free tier)
            params = {
                "q": f"{city},{country}",
                "appid": self.api_key,
                "units": "metric",
                "cnt": min(days * 8, 40)  # 3-hour intervals
            }

            response = requests.get(
                f"{self.base_url}/forecast",
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            # Process forecast
            forecast = self._process_forecast_data(data, days)

            result = {
                "city": city,
                "country": country,
                "forecast": forecast,
                "source": "OpenWeatherMap"
            }

            # Cache result
            self.cache[cache_key] = result

            logger.info(f"Fetched weather forecast for {city}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            return self._get_mock_forecast(city, country, start_date, days)

    def _process_forecast_data(self, data: Dict[str, Any], days: int) -> List[Dict[str, Any]]:
        """Process OpenWeatherMap response into daily forecasts"""

        daily_forecasts = {}

        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")

            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = {
                    "date": date_key,
                    "temps": [],
                    "conditions": [],
                    "precipitation": 0,
                    "wind_speeds": []
                }

            daily_forecasts[date_key]["temps"].append(item["main"]["temp"])
            daily_forecasts[date_key]["conditions"].append(
                item["weather"][0]["main"] if item.get("weather") else "Unknown"
            )
            daily_forecasts[date_key]["wind_speeds"].append(item["wind"]["speed"])

            if "rain" in item:
                daily_forecasts[date_key]["precipitation"] += item["rain"].get("3h", 0)

        # Aggregate to daily
        result = []
        for date_key in sorted(daily_forecasts.keys())[:days]:
            day_data = daily_forecasts[date_key]
            result.append({
                "date": date_key,
                "temp_high_c": int(max(day_data["temps"])),
                "temp_low_c": int(min(day_data["temps"])),
                "conditions": max(set(day_data["conditions"]), key=day_data["conditions"].count),
                "precipitation_mm": round(day_data["precipitation"], 1),
                "wind_speed_kmh": int(sum(day_data["wind_speeds"]) / len(day_data["wind_speeds"]) * 3.6)
            })

        return result

    def _get_mock_forecast(
        self,
        city: str,
        country: str,
        start_date: str,
        days: int
    ) -> Dict[str, Any]:
        """Generate mock weather data for testing"""

        logger.info(f"Generating mock weather for {city}")

        forecast = []
        start = datetime.strptime(start_date, "%Y-%m-%d")

        # Simple seasonal logic
        month = start.month
        if month in [6, 7, 8]:  # Summer
            base_high, base_low = 28, 20
            conditions = "Sunny"
        elif month in [12, 1, 2]:  # Winter
            base_high, base_low = 12, 5
            conditions = "Cloudy"
        elif month in [3, 4, 5]:  # Spring
            base_high, base_low = 18, 12
            conditions = "Partly Cloudy"
        else:  # Fall
            base_high, base_low = 20, 14
            conditions = "Partly Cloudy"

        for i in range(days):
            date = start + timedelta(days=i)
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "temp_high_c": base_high + (i % 3 - 1) * 2,
                "temp_low_c": base_low + (i % 3 - 1) * 2,
                "conditions": conditions,
                "precipitation_mm": 0 if conditions == "Sunny" else 5,
                "wind_speed_kmh": 15
            })

        return {
            "city": city,
            "country": country,
            "forecast": forecast,
            "source": "mock"
        }


# Singleton instance
_weather_tool = None

def get_weather_tool() -> WeatherTool:
    """Get or create weather tool instance"""
    global _weather_tool
    if _weather_tool is None:
        _weather_tool = WeatherTool()
    return _weather_tool
