# SmartLoan 💳

**Embedded loan repayment for small merchants.**

Every customer payment automatically splits: 90% goes to the shopkeeper, 10% goes toward loan repayment — until the loan is fully paid off.

---

## Project Structure

```
smart_loan/
├── app.py                  # Flask backend (all routes + logic)
├── requirements.txt
├── loan_data.json          # Auto-created on first loan setup
├── templates/
│   ├── index.html          # Screen 1: Loan Setup
│   ├── merchant.html       # Screen 2: Merchant QR + Simulate Payment
│   └── dashboard.html      # Screen 3: Dashboard + Transaction History
└── static/
    ├── style.css           # All styles
    └── script.js           # Live previews & animations
```

---

## Setup & Run

```bash
# 1. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Screens / Flow

### Screen 1 – Loan Setup (`/`)
- Shopkeeper enters: Shop Name, Loan Amount (₹50,000), Interest Rate (12%), Deduction % (10%), Duration (12 months)
- Live preview shows total interest, total due, and per-₹1,000 deduction
- Click **Create Loan** → redirects to QR screen

### Screen 2 – Merchant QR (`/merchant`)
- Displays the shop name and a live QR code (UPI deep-link format)
- Shows remaining loan balance and deduction %
- **Simulate Customer Payment**: enter ₹1,000 → splits as ₹900 to shopkeeper + ₹100 to loan repayment
- Live split bar preview before submitting

### Screen 3 – Dashboard (`/dashboard`)
- Progress bar showing % of loan repaid
- 6 metric cards: Loan Amount, Remaining Loan, Amount Repaid, Deduction %, No. of Transactions, Estimated Completion Date
- Full transaction history table (newest first)

---

## Tech Stack

| Layer     | Choice              |
|-----------|---------------------|
| Backend   | Python + Flask      |
| Storage   | JSON file (loan_data.json) |
| Frontend  | HTML + CSS + Vanilla JS |
| QR Code   | qrcodejs (CDN)      |

No database required — keeps it simple and portable for a demo/prototype.

---

## Business Logic

```
Customer pays ₹1,000
├── Loan repayment = ₹1,000 × 10% = ₹100
└── Shopkeeper gets = ₹1,000 − ₹100 = ₹900

Total due = Loan Amount + (Loan × Rate × Duration/12)
e.g. ₹50,000 + (₹50,000 × 12% × 1yr) = ₹56,000
```

---

## To-Do / Extensions

- [ ] Add UPI/Razorpay real payment integration
- [ ] Multi-shopkeeper support with login
- [ ] SMS/WhatsApp notification on repayment milestones
- [ ] Export transaction history to CSV/PDF
- [ ] Replace JSON storage with SQLite/PostgreSQL
