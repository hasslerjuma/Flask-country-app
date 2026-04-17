from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    country_data = None
    error = None

    if request.method == "POST":
        country_name = request.form.get("country")
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            country = data[0]
            country_data = {
                "name": country["name"]["common"],
                "capital": country["capital"][0],
                "population": country["population"],
                "region": country["region"],
                "flag": country["flags"]["png"]
            }
        else:
            error = "Country not found. Please try again."

    return render_template("index.html", country_data=country_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)