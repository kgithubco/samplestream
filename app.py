import streamlit as st
import requests
import json

st.title("Stock1 Data")
# Get user input for stock symbol
stock_symbol = st.text_input("Enter a stock symbol", "AAPL")

# API endpoint and parameters
api_endpoint = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey=3MMA83Z4ZN91RLCN"

# Make the API request
response = requests.get(api_endpoint)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if "Global Quote" in data:
        data = data["Global Quote"]
        # Extract relevant data
        symbol = data["01. symbol"]
        price = float(data["05. price"])
        change = float(data["09. change"])
        change_percent = float(data["10. change percent"].rstrip("%"))

        # Construct the Slack message
        slack_webhook_url = "https://hooks.slack.com/services/YOUR_SLACK_WEBHOOK_URL"
        slack_message = f"{symbol} ({data['01. symbol']}) Current Price: ${price:.2f}, Change: ${change:.2f} ({change_percent:.2f}%)"

        payload = {
            "text": slack_message
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            st.write(f"Slack notification sent for {symbol}")
        else:
            st.write(f"Failed to send Slack notification. Error: {response.text}")

        # Display the stock data
        st.subheader(f"{symbol} ({data['01. symbol']})")
        st.write(f"Price: ${price:.2f}")
        st.write(f"Change: ${change:.2f} ({change_percent:.2f}%)")
    else:
        st.write("No data found for the given stock symbol.")
else:
    st.write(f"Error: {response.status_code} - {response.text}")
