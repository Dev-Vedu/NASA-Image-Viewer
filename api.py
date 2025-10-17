import os
import requests

API_KEY = os.getenv("NASA_API_KEY")

def fetch_apod(date=None):
    """
    Fetch APOD data from NASA API.
    If date is None, fetches today's image.
    """
    url = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'
    if date:
        url += f"&date={date}"  # format: 'YYYY-MM-DD'

    try:
        response = requests.get(url, timeout=10)  # 10-second timeout
        response.raise_for_status()  # raise error for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # returns None if there is a network error

    data = response.json()
    return {
        'title': data.get('title'),
        'url': data.get('url'),
        'explanation': data.get('explanation'),
        'date': data.get('date'),
        'media_type': data.get('media_type', 'image')
    }
