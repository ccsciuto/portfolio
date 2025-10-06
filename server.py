from flask import Flask, render_template, request
import pandas as pd
import math
import os

app = Flask(__name__)

# Load your CSV and prepare dictionary
changes = pd.read_csv("changes.csv")
dict_change = {row.Total: row.Change for (_, row) in changes.iterrows()}


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/paceadjcalc')
def paceadjcalc():
    return render_template("paceadjcalc.html")


@app.route('/budget')
def budget():
    return render_template("test.html")


@app.route("/photography")
def photography():
    photo_folder = os.path.join('static', 'photos')
    photo_files = [
        f for f in os.listdir(photo_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    return render_template("photography.html", photo_files=photo_files)


@app.route('/garmincharts')
def garmincharts():
    return render_template("garmincharts.html")


@app.route('/warmer', methods=['GET', 'POST'])
def warmer():
    pace = request.form["pace"]
    dp = request.form["dewpoint"]
    temp = request.form["temp"]

    min_part, sec_part = pace.split(":")
    total_seconds = float(min_part) * 60 + float(sec_part)
    t_dp = float(dp) + float(temp)
    percent = dict_change[t_dp]
    amount_change = (percent + 100) / 100
    new_pace_seconds = total_seconds * amount_change

    new_min = math.floor(new_pace_seconds / 60)
    new_sec = int(new_pace_seconds % 60)
    if new_sec < 10:
        new_sec = f"0{new_sec}"

    return f"The adjusted pace is: {new_min}:{new_sec}/mile"


@app.route('/cooler', methods=['GET', 'POST'])
def cooler():
    pace = request.form["pace"]
    dp = request.form["dewpoint"]
    temp = request.form["temp"]

    min_part, sec_part = pace.split(":")
    total_seconds = float(min_part) * 60 + float(sec_part)
    t_dp = float(dp) + float(temp)
    percent = dict_change[t_dp]
    amount_change = (percent + 100) / 100
    new_pace_seconds = total_seconds / amount_change

    new_min = math.floor(new_pace_seconds / 60)
    new_sec = int(new_pace_seconds % 60)
    if new_sec < 10:
        new_sec = f"0{new_sec}"

    return f"The adjusted pace is: {new_min}:{new_sec}/mile"


@app.route("/marathon_prediction")
def marathon_prediction():
    return render_template("marathon_prediction.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns this automatically
    app.run(host="0.0.0.0", port=port, debug=True)
