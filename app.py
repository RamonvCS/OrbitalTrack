from flask import Flask, render_template
from services.api_client import get_upcoming_launches

app = Flask(__name__)

@app.route('/')
def index():
    launches = get_upcoming_launches()
    return render_template('index.html', launches=launches)

if __name__ == '__main__':
    app.run(debug=True)