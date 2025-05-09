from flask import Flask, render_template
<<<<<<< HEAD
from services.api_client import get_upcoming_launches
from datetime import datetime

app = Flask(__name__)

=======
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import requests
import os

app = Flask(__name__)

# Opcional: configuración de correo si decides usar alertas después
EMAIL_FROM = os.environ.get("EMAIL_FROM", "your_email@gmail.com")
EMAIL_TO = os.environ.get("EMAIL_TO", "your_phone_email@txt.att.net")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "your_app_password")

# Función para obtener lanzamientos en tiempo real (solo al cargar la página)
def get_upcoming_launches():
    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"❌ Failed to fetch launches: {e}")
        return []

# RUTA PRINCIPAL - solo carga datos cuando el usuario hace refresh
>>>>>>> dev
@app.route('/')
def index():
    launches = get_upcoming_launches()
    for launch in launches:
        net_raw = launch.get("net")
        try:
            net_datetime = datetime.strptime(net_raw, "%Y-%m-%dT%H:%M:%SZ")
            launch["formatted_net"] = net_datetime.strftime("%b %d, %Y at %H:%M UTC")
<<<<<<< HEAD
        except:
=======
        except Exception:
>>>>>>> dev
            launch["formatted_net"] = net_raw
    return render_template('index.html', launches=launches)

@app.route('/agencies')
def agencies():
    return render_template('agencies.html')

<<<<<<< HEAD
=======
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/about')
def about():
    return render_template('about.html')
>>>>>>> dev

if __name__ == '__main__':
    app.run(debug=True)
