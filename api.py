import os
import requests


API_KEY = os.getenv("NASA_API_KEY")

if not API_KEY:
    raise ValueError("NASA_API_KEY not set. Please set it in your environment.")

def fetch_apod(date=None):
    """
    Fetch APOD data from NASA API.
    If date is None, fetches today's image.
    """
    url = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'
    if date:
        url += f"&date={date}" 
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        return {
            'title': data.get('title'),
            'url': data.get('url'),
            'explanation': data.get('explanation'),
            'date': data.get('date'),
            'media_type': data.get('media_type')
        }
    else:
        raise Exception(f"Error {response.status_code}: Unable to fetch data.")
