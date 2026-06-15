from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "smartloan_secret_2024"

DATA_FILE = "loan_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return None


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_loan():
    return load_data()


@app.route("/")
def index():
    loan = get_loan()
    return render_template("index.html", loan=loan)


@app.route("/setup", methods=["POST"])
def setup():
    loan_amount = float(request.form["loan_amount"])
    interest_rate = float(request.form["interest_rate"])
    deduction_pct = float(request.form["deduction_pct"])
    duration_months = int(request.form["duration_months"])
    shop_name = request.form.get("shop_name", "My Store")

    total_interest = loan_amount * (interest_rate / 100) * (duration_months / 12)
    total_due = loan_amount + total_interest

    data = {
        "shop_name": shop_name,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "deduction_pct": deduction_pct,
        "duration_months": duration_months,
        "total_due": round(total_due, 2),
        "remaining_loan": round(total_due, 2),
        "total_repaid": 0,
        "transactions": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_data(data)
    return redirect(url_for("merchant_qr"))


@app.route("/merchant")
def merchant_qr():
    loan = get_loan()
    if not loan:
        return redirect(url_for("index"))
    return render_template("merchant.html", loan=loan)


@app.route("/simulate", methods=["POST"])
def simulate():
    loan = get_loan()
    if not loan:
        return redirect(url_for("index"))

    payment = float(request.form["payment_amount"])
    deduction_pct = loan["deduction_pct"]

    loan_deduction = round(payment * (deduction_pct / 100), 2)
    shopkeeper_gets = round(payment - loan_deduction, 2)

    if loan_deduction > loan["remaining_loan"]:
        loan_deduction = round(loan["remaining_loan"], 2)
        shopkeeper_gets = round(payment - loan_deduction, 2)

    loan["remaining_loan"] = round(loan["remaining_loan"] - loan_deduction, 2)
    loan["total_repaid"] = round(loan["total_repaid"] + loan_deduction, 2)

    txn = {
        "id": len(loan["transactions"]) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payment": payment,
        "loan_deduction": loan_deduction,
        "shopkeeper_gets": shopkeeper_gets,
    }
    loan["transactions"].append(txn)
    save_data(loan)

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    loan = get_loan()
    if not loan:
        return redirect(url_for("index"))

    progress = 0
    if loan["total_due"] > 0:
        progress = round((loan["total_repaid"] / loan["total_due"]) * 100, 1)

    # Estimated completion
    avg_daily = 0
    est_completion = "N/A"
    if loan["transactions"]:
        total_days = 1
        if len(loan["transactions"]) > 1:
            first = datetime.strptime(loan["transactions"][0]["timestamp"], "%Y-%m-%d %H:%M:%S")
            last = datetime.strptime(loan["transactions"][-1]["timestamp"], "%Y-%m-%d %H:%M:%S")
            total_days = max((last - first).days, 1)
        avg_daily = loan["total_repaid"] / total_days
        if avg_daily > 0:
            days_left = loan["remaining_loan"] / avg_daily
            est_date = datetime.now() + timedelta(days=days_left)
            est_completion = est_date.strftime("%d %b %Y")

    return render_template(
        "dashboard.html",
        loan=loan,
        progress=progress,
        est_completion=est_completion,
    )


@app.route("/reset", methods=["POST"])
def reset():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    return redirect(url_for("index"))


@app.route("/api/loan")
def api_loan():
    loan = get_loan()
    return jsonify(loan or {})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
