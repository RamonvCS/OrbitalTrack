from flask import Flask, render_template
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import requests
import os

app = Flask(__name__)

# Configuración de correo (opcional)
EMAIL_FROM = os.environ.get("EMAIL_FROM", "your_email@gmail.com")
EMAIL_TO = os.environ.get("EMAIL_TO", "your_phone_email@txt.att.net")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "your_app_password")

# Obtener lanzamientos desde SpaceDevs API
def get_upcoming_launches():
    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"❌ Failed to fetch launches: {e}")
        return []

@app.route('/')
def index():
    launches = get_upcoming_launches()
    for launch in launches:
        net_raw = launch.get("net")
        try:
            net_datetime = datetime.strptime(net_raw, "%Y-%m-%dT%H:%M:%SZ")
            launch["formatted_net"] = net_datetime.strftime("%b %d, %Y at %H:%M UTC")
        except Exception:
            launch["formatted_net"] = net_raw
    return render_template('index.html', launches=launches)

@app.route('/agencies')
def agencies():
    return render_template('agencies.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
