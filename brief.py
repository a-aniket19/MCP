import httpx
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("DailyBriefing")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_weather(city: str) -> str:
    response = httpx.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "imperial"
        }
    )
    if response.status_code != 200:
        return "Weather unavailable."

    data = response.json()
    return (
        f"Temperature: {data['main']['temp']}°F\n"
        f"Feels like: {data['main']['feels_like']}°F\n"
        f"Condition: {data['weather'][0]['description']}\n"
        f"Humidity: {data['main']['humidity']}%"
    )

def get_news(category: str) -> str:
    response = httpx.get(
        "https://newsapi.org/v2/top-headlines",
        params={
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 5,
            "category": category,
            "country": "us"
        }
    )
    if response.status_code != 200:
        return f"{category} news unavailable."

    articles = response.json().get("articles", [])
    if not articles:
        return f"No {category} news found."

    return "\n".join([f"- {a['title']}" for a in articles])

@mcp.tool()
def get_daily_briefing(city: str = "Cherry Hill, NJ", topic: str = "technology") -> str:
    """Generate a complete daily briefing including weather and news. Use this when the user asks for their daily briefing, morning update, or daily summary. Accepts a city for weather and a topic for news."""

    weather = get_weather(city)
    topic_news = get_news(topic)
    general_news = get_news("general")

    return f"""
🌤 WEATHER — {city}
{weather}

📰 {topic.upper()} NEWS
{topic_news}

🌍 GENERAL NEWS
{general_news}
"""

if __name__ == "__main__":
    mcp.run()
