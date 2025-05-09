import requests

def get_upcoming_launches():
    url = 'https://ll.thespacedevs.com/2.2.0/launch/upcoming/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si el status code es 4xx o 5xx
        data = response.json()
        return data.get('results', [])  # Devuelve [] si no hay 'results'
    except Exception as e:
        print(f"❌ Error al obtener datos de lanzamientos: {e}")
        return []
