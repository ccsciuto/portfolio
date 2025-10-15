from flask import Flask, render_template, request
import pandas as pd
import math
import os
from PIL import Image

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
    photo_root = os.path.join("static", "photos")
    albums = []
    for folder in os.listdir(photo_root):
        folder_path = os.path.join(photo_root, folder)
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path)
                      if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
            if images:
                cover_image = images[0]  # first image as preview
                albums.append({
                    "name": folder.capitalize(),
                    "folder": folder,
                    "cover": f"photos/{folder}/{cover_image}"
                })
    return render_template("photography.html", albums=albums)


@app.route("/photography/<album_name>")
def album(album_name):
    album_path = os.path.join("static", "photos", album_name)
    photos = [f for f in os.listdir(album_path)
              if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

    # Get dimensions and group by orientation
    portrait = []
    landscape = []
    square = []

    for photo in photos:
        try:
            img_path = os.path.join(album_path, photo)
            with Image.open(img_path) as img:
                width, height = img.size
                if height > width:
                    portrait.append(photo)
                elif width > height:
                    landscape.append(photo)
                else:
                    square.append(photo)
        except Exception as e:
            print(f"Error reading {photo}: {e}")

    # Combine groups — you can rearrange this order however you like
    sorted_photos = landscape + portrait + square

    return render_template(
        "album.html",
        album_name=album_name.capitalize(),
        photos=sorted_photos,
        album_folder=album_name
    )


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
