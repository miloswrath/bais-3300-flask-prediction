from flask import Flask, render_template, request
from flask_cors import CORS
import requests as http
import os

app = Flask(__name__)
CORS(app)

# Change this to the Azure backend URL before deploying to Azure:
# api_url = "https://zjgilliam-flask-prediction.azurewebsites.net/predict"
api_url = "https://zjgilliam-flask-prediction-hghtdze8czd8hxcz.eastus-01.azurewebsites.net/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    payload = {
        "age":          request.form.get("age"),
        "gender":       request.form.get("gender"),
        "country":      request.form.get("country"),
        "highest_deg":  request.form.get("highest_deg"),
        "coding_exp":   request.form.get("coding_exp"),
        "title":        request.form.get("title"),
        "company_size": request.form.get("company_size"),
    }

    try:
        response = http.post(api_url, json=payload, timeout=10)
        data = response.json()

        if response.status_code == 200:
            raw = data.get("predicted_salary", 0)
            predicted_salary = f"${raw:,.0f}"
            return render_template("index.html", predicted_salary=predicted_salary)
        else:
            error = data.get("error", "An unexpected error occurred.")
            return render_template("index.html", error=error)

    except http.exceptions.ConnectionError:
        return render_template("index.html", error="Could not connect to the prediction API. Please try again later.")
    except http.exceptions.Timeout:
        return render_template("index.html", error="The prediction API took too long to respond. Please try again.")
    except Exception as e:
        return render_template("index.html", error=f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=port, debug=debug)
