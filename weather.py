import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

API_KEY = "f9698e47577fe4f4076ebc03507edbdf"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather condition for any given city.
    Use this tool when the user asks about the weather in a specific city."""
    response = httpx.get(BASE_URL, params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    })

    if response.status_code != 200:
        raise ValueError(f"Failed to get weather for {city}: {response.text}")

    data = response.json()

    return (
        f"City: {data['name']}\n"
        f"Temperature: {data['main']['temp']}°C\n"
        f"Feels like: {data['main']['feels_like']}°C\n"
        f"Condition: {data['weather'][0]['description']}\n"
        f"Humidity: {data['main']['humidity']}%\n"
        f"Wind speed: {data['wind']['speed']} m/s"
    )

if __name__ == "__main__":
    mcp.run()