import requests
API_KEY = 'DEMO_KEY'  
def fetch_apod(date=None):
    """
    Fetch APOD data from NASA API.
    If date is None, fetches today's image/video.
    """
    url = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'
    if date:
        url += f"&date={date}"  
    response = requests.get(url).json()
    return {
        'title': response.get('title'),
        'url': response.get('url'),
        'explanation': response.get('explanation'),
        'date': response.get('date'),
        'media_type': response.get('media_type')
    }
