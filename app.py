from flask import Flask, render_template, request, session
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = "nairobi254"

@app.route("/", methods=["GET", "POST"])
def index():
    country_data = None
    error = None

    if "favourites" not in session:
        session["favourites"] = []

    if request.method == "POST":
        print("Form data:", request.form)

        if "add_favourite" in request.form:
            country_name = request.form.get("add_favourite")
            if country_name not in session["favourites"]:
                session["favourites"].append(country_name)
                session.modified = True

        elif "country" in request.form:
            country_name = request.form.get("country")
            url = f"https://restcountries.com/v3.1/name/{country_name}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, verify=False)
            print("Status:", response.status_code)

            if response.status_code == 200:
                data = response.json()
                country = data[0]
                country_data = {
                    "name": country["name"]["common"],
                    "capital": country["capital"][0],
                    "population": country["population"],
                    "region": country["region"],
                    "flag": country["flags"]["svg"]
                }
            else:
                error = "Country not found. Please try again."

    print("country_data:", country_data)
    return render_template("index.html", country_data=country_data, error=error, favourites=session["favourites"])

if __name__ == "__main__":
    app.run(debug=True)