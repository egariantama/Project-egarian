from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/time")
def time():
    now = datetime.now().strftime("%H:%M:%S")
    return now

if __name__ == "__main__":
    app.run(debug=True)
