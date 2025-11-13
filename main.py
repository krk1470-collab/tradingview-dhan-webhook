from flask import Flask, request
import time, requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Alert received:", data)

    # Secret check
    if data.get("secret") != "qXsya":
        return "Invalid secret", 403

    delay = data.get("delay", 0)
    print(f"Waiting for {delay} seconds before placing order...")
    time.sleep(delay)

    order = data["order_legs"][0]

    # Example Dhan order payload
    order_payload = {
        "transactionType": order["transactionType"],
        "exchangeSegment": "NSE_EQ",
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "instrument": order["symbol"],
        "quantity": order["quantity"]
    }

    # Dhan API endpoint
    response = requests.post(
        "https://api.dhan.co/orders",
        json=order_payload,
        headers={
            "access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzYzMTA0MjQ5LCJpYXQiOjE3NjMwMTc4NDksInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAyNjUyMjMyIn0.AGv0_oxQDb1mTilq_egd43mu_BJAmjxPfrtLBoUxKicEMBhhhLYYiSVtwa-lXV2kwtfLbu5Ena-NIDPKxBUtNA"
        }
    )

    print("Order response:", response.text)
    return "Order executed after delay", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
