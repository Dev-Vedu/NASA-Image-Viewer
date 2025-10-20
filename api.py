import requests

API_KEY = "DEMO_KEY"

def fetch_apod(date=None):
    """
    Fetch APOD (Astronomy Picture of the Day) data from NASA API.
    If date is None, fetch today's image.
    """
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
    if date:
        url += f"&date={date}"#format of date

    try:
        response = requests.get(url, timeout=10)  #10-second timeout
        response.raise_for_status()  #raise error for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # returns None if there is a network error

    data = response.json()
    return {
        "title": data.get("title"),
        "url": data.get("url"),
        "explanation": data.get("explanation"),
        "date": data.get("date"),
        "media_type": data.get("media_type", "image"),
    }
