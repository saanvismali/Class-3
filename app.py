from flask import flask, render_template, request
import json
import urllib.request
import urllib.parse

app = flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def details():
    if request.method == 'GET':
        return render_template("index.html")
    location = request.form.get("location", "").strip()
    if not location:
        return render_template("index.html", error="Please enter a location.")
    try:
        q = urllib.parse.quote(location)

        url = f"https://photon.komoot.io/api/?q={q}&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'FlaskGEocoder/1.0'})
        source = urllib.request.urlopen(req).read()
        responseData = json.loads(source)

    features = responseData.get("Features", [])
    if not features:
        return render_template("index.html", error="Location not found.")

    lon, lat = features[0]["geometry"]["coordinates"]

    data={
        "latitude": str(lat),
        "longitude": str(lon)
    }

    return render_template("index.html", data=data)

except Exception:
    return render_template("index.html", error="An error occurred while fetching location data.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)