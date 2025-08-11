from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Example external API 
EXTERNAL_API_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MBG.DEX&outputsize=compact&apikey=2TECT4A1BAPF8ILK"

@app.route("/fetch", methods=["GET"])
def fetch_data():
    try:
        # Call the external API
        response = requests.get(EXTERNAL_API_URL, timeout=5)
        response.raise_for_status()  # Raise error if request failed
        #response["success"] = "true"
        time_series = response.json()["Time Series (Daily)"]
        result = [
            {
                "date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            }
            for date, values in sorted(time_series.items())
        ]


        # Forward the data to the client
        return jsonify(response.json())
        # return jsonify(result)

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask development server
    app.run(host="0.0.0.0", port=6666, debug=True)
