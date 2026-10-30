# COD Risk Engine

## Overview
A Flask-based Cash on Delivery (COD) risk assessment application. It evaluates order risk using configurable rules and recommends an action to help operations teams manage potential Return to Origin (RTO) orders.

## Features
- Rule-based order risk scoring.
- Configurable thresholds and weights in `config.json`.
- Four recommended actions: Ship as-is, Ship after confirmation, Nudge to prepaid, and Hold/cancel.
- Dashboard for historical delivery outcomes and estimated RTO costs.
- Simulated customer confirmation and prepaid-offer flows.
- Experiment Impact dashboard section for comparing control and intervention groups when genuine experiment data becomes available.

## Requirements
- Python 3
- Flask
- pandas

## Setup

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```bash
   pip install flask pandas
   ```

5. Ensure the required configuration and dataset files are available locally. Keep private customer data out of public repositories.
6. Run the application:
   ```bash
   python app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## Main Routes
- `/` — Home page
- `/assess` — Order risk assessment endpoint
- `/dashboard` — Historical metrics and visualizations
- `/chat` — Simulated confirmation workflow

Check `app.py` for the expected request format for `/assess`.

## Data and limitations
Historical metrics describe observed outcomes and do not establish that the risk engine caused those outcomes. The experiment comparison requires genuine, correctly assigned control and intervention orders with finalized statuses.

The chat workflow is a simulator; it does not send real WhatsApp messages or process payments.

## Privacy
Do not commit confidential customer information, credentials, `.env` files, or private operational datasets. Supply authorized data locally when required.

## Future improvements
- Validate risk thresholds against business outcomes.
- Add automated tests and input validation.
- Integrate an authorized messaging provider.
- Run a properly randomized experiment and evaluate statistical uncertainty.
