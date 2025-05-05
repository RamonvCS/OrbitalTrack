from flask import Flask, render_template
from services.api_client import get_upcoming_launches
from datetime import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
