from flask import Flask, render_template, request, jsonify, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json 
import os

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds_json = os.environ.get("GOOGLE_CREDS")

if not creds_json:
    raise Exception("GOOGLE_CREDS not found!")

creds_dict = json.loads(creds_json)


creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("NGO Donations").sheet1

app = Flask(__name__)

# Temporary storage (later DB)
donations = []

@app.route('/')
def home():
    return render_template('donate.html')


@app.route('/submit-donation', methods=['POST'])
def submit_donation():
    data = request.get_json()
    print("DATA:", data)

    # Save to Google Sheet
    sheet.append_row([
    str(data.get('full name', '')),
    str(data.get('mobile', '')),
    str(data.get('address', '')),
    str(data.get('city', '')),
    str(data.get('pin code', '')),
    str(data.get('state', '')),
    str(data.get('email', '')),
    str(data.get('donation_amount', ''))
])
    print("Saved to Google Sheets:", data)

    return jsonify({
        "success": True,
        "redirect": url_for('payment')
    })


@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))