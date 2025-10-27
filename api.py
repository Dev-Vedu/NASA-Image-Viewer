import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = "mQgZIgTFzRc9fFelcch7gpH7aIWbKMeggb2iVhDd"

def fetch_apod(date=None):
    """
    Fetch APOD (Astronomy Picture of the Day) data from NASA API.
    If date is None, fetch today's image.
    """
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
    if date:
        url += f"&date={date}"  # format of date

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    data = response.json()
    return {
        "title": data.get("title"),
        "url": data.get("url"),
        "explanation": data.get("explanation"),
        "date": data.get("date"),
        "media_type": data.get("media_type", "image"),
    }
