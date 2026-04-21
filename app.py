from flask import Flask, render_template, request, jsonify, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
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

    # Save to Google Sheet
    sheet.append_row([
    data.get('donor_name'),
    data.get('mobile'),
    data.get('address'),
    data.get('city'),
    data.get('pin_code'),
    data.get('state'),
    data.get('email'),
    data.get('donation_amount')
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