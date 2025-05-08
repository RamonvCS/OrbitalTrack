from flask import Flask, render_template
from services.api_client import get_upcoming_launches
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "your_phone_email@txt.att.net"  # or regular email
EMAIL_PASSWORD = "your_app_password"

def send_email(launch_name, pad_name, webcast_url=None):
    msg = MIMEText(f"🚀 Launch Alert!\n\n{launch_name} is launching from {pad_name}.\n{webcast_url or ''}")
    msg["Subject"] = f"Launch Now: {launch_name}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"✅ Email sent for {launch_name}")

def check_launches():
    print("⏱️ Checking launches...")
    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
    response = requests.get(url)
    data = response.json()["results"]

    now = datetime.utcnow()
    for launch in data:
        net = datetime.fromisoformat(launch["net"].replace("Z", "+00:00"))
        if abs((net - now).total_seconds()) < 60:
            send_email(launch["name"], launch["pad"]["name"], launch.get("webcast"))

scheduler = BackgroundScheduler()
scheduler.add_job(check_launches, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def index():
    launches = get_upcoming_launches()
    for launch in launches:
        net_raw = launch.get("net")
        try:
            net_datetime = datetime.strptime(net_raw, "%Y-%m-%dT%H:%M:%SZ")
            launch["formatted_net"] = net_datetime.strftime("%b %d, %Y at %H:%M UTC")
        except:
            launch["formatted_net"] = net_raw
    return render_template('index.html', launches=launches)

@app.route('/agencies')
def agencies():
    return render_template('agencies.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


if __name__ == '__main__':
    app.run(debug=True)
