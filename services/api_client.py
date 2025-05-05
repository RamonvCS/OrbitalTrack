import requests

def get_upcoming_launches():
    url = 'https://ll.thespacedevs.com/2.2.0/launch/upcoming/'
    response = requests.get(url)
    data = response.json()
    return data['results']
