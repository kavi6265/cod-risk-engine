
from flask import Flask, request, jsonify, render_template
import json
from pathlib import Path
import pandas as pd
import os
app = Flask(__name__)

# File paths
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
CSV_PATH = BASE_DIR / "orders_sample.csv"


# Load risk configuration
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Load and clean finalized orders
def load_finalized_orders():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    # Remove spaces around column names
    df.columns = df.columns.str.strip()

    # Validate required column
    if "final_status" not in df.columns:
        raise ValueError(
            "Column 'final_status' is missing. "
            f"Available columns: {df.columns.tolist()}"
        )

    # Normalize order status
    df["final_status"] = (
        df["final_status"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Keep only finalized orders
    df = df[
        df["final_status"].isin(["DELIVERED", "RTO"])
    ].copy()

    return df


# Assess COD order risk
def assess_order(order):
    config = load_config()
    weights = config["weights"]
    thresholds = config["thresholds"]

    risk = 0
    reasons = []

    # Customer history
    previous_rto = int(
        order.get(
            "customer_prior_rto",
            order.get("previous_rto", 0)
        ) or 0
    )

    if previous_rto >= 2:
        risk += weights["previous_rto_2_plus"]
        reasons.append("Multiple previous RTOs")
    elif previous_rto == 1:
        risk += weights["previous_rto_1"]
        reasons.append("One previous RTO")

    # State-level historical risk
    state = str(order.get("state", "") or "").strip().title()

    high_risk_states = [
        x.title() for x in config["high_risk_states"]
    ]
    medium_risk_states = [
        x.title() for x in config["medium_risk_states"]
    ]

    if state in high_risk_states:
        risk += weights["high_risk_state"]
        reasons.append(
            "Historical state-level RTO rate is elevated"
        )
    elif state in medium_risk_states:
        risk += weights["medium_risk_state"]
        reasons.append(
            "State has an elevated historical RTO rate"
        )

    # Courier history
    courier = str(order.get("courier", "") or "").strip().lower()

    high_couriers = [
        name.lower() for name in config["high_risk_couriers"]
    ]

    if courier in high_couriers:
        risk += weights["high_risk_courier"]
        reasons.append(
            "Courier has a higher observed RTO rate"
        )

    # Marketing source
    source = str(
        order.get("utm_source", "") or ""
    ).strip().lower()

    if source == "meta_ads":
        risk += weights["meta_ads"]
        reasons.append(
            "Acquisition channel has elevated observed RTO"
        )

    # Basic address check
    address = str(order.get("address", "") or "").strip()

    if len(address) < 15:
        risk += weights["incomplete_address"]
        reasons.append("Address may be incomplete")

    # Basic placeholder-name check
    name = str(
        order.get("customer_name", "") or ""
    ).strip().lower()

    if name in {"asdf", "test", "abc", "unknown", "qwerty"}:
        risk += weights["suspicious_name"]
        reasons.append(
            "Customer name looks like a placeholder"
        )

    # Keep score within 0–100
    risk = max(0, min(int(risk), 100))

    # Determine recommended action
    if risk <= thresholds["ship_max"]:
        action = "Ship as-is"
    elif risk <= thresholds["confirm_max"]:
        action = "Ship after confirmation"
    elif risk <= thresholds["prepaid_max"]:
        action = "Nudge to prepaid"
    else:
        action = "Hold / cancel"

    if not reasons:
        reasons.append(
            "No configured risk indicators detected"
        )

    return {
        "risk_score": risk,
        "action": action,
        "reason": "; ".join(reasons)
    }

def get_experiment_impact():
    file_path = BASE_DIR / "experiment_results.csv"

    empty_result = {
        "available": False,
        "control_count": 0,
        "intervention_count": 0,
        "control_rto_rate": 0,
        "intervention_rto_rate": 0,
        "absolute_reduction": 0,
        "relative_reduction": 0
    }

    if not file_path.exists():
        return empty_result

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()

    required = {"experiment_group", "final_status"}
    if not required.issubset(df.columns):
        return empty_result

    df["experiment_group"] = (
        df["experiment_group"].astype(str).str.strip().str.lower()
    )
    df["final_status"] = (
        df["final_status"].astype(str).str.strip().str.upper()
    )

    # Only compare finalized orders in the two experiment groups.
    df = df[
        df["experiment_group"].isin(["control", "intervention"])
        & df["final_status"].isin(["DELIVERED", "RTO"])
    ].copy()

    # Each order should appear only once.
    df = df.drop_duplicates(subset=["order_id"]) if "order_id" in df.columns else df

    control = df[df["experiment_group"] == "control"]
    intervention = df[df["experiment_group"] == "intervention"]

    if control.empty or intervention.empty:
        return {
            **empty_result,
            "control_count": len(control),
            "intervention_count": len(intervention)
        }

    control_rate = (control["final_status"].eq("RTO").mean()) * 100
    intervention_rate = (intervention["final_status"].eq("RTO").mean()) * 100

    absolute_reduction = control_rate - intervention_rate
    relative_reduction = (
        absolute_reduction / control_rate * 100
        if control_rate > 0 else 0
    )

    return {
        "available": True,
        "control_count": len(control),
        "intervention_count": len(intervention),
        "control_rto_rate": round(control_rate, 2),
        "intervention_rto_rate": round(intervention_rate, 2),
        "absolute_reduction": round(absolute_reduction, 2),
        "relative_reduction": round(relative_reduction, 2)
    }
# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Order assessment API
@app.route("/assess", methods=["POST"])
def assess():
    order = request.get_json(silent=True)

    if not isinstance(order, dict):
        return jsonify({
            "error": "Send a valid JSON object"
        }), 400

    try:
        result = assess_order(order)
        return jsonify(result)

    except (ValueError, TypeError, KeyError, OSError) as error:
        return jsonify({
            "error": str(error)
        }), 400


# Founder dashboard

@app.route("/dashboard")
def dashboard():
    try:
        # 1. Load finalized order data
        df = load_finalized_orders()

        if df.empty:
            return "No finalized orders found.", 404

        # 2. Validate required columns
        required_columns = [
            "final_status",
            "state",
            "courier"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            return (
                f"Missing required CSV columns: {missing_columns}",
                500
            )

        # 3. Clean status values
        df["final_status"] = (
            df["final_status"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # 4. Calculate risk decisions for each order
        results = df.apply(
            lambda row: assess_order(row.to_dict()),
            axis=1
        )

        df["decision"] = [
            result["action"] for result in results
        ]

        # 5. Overall metrics
        total = len(df)

        delivered = int(
            (df["final_status"] == "DELIVERED").sum()
        )

        rto = int(
            (df["final_status"] == "RTO").sum()
        )

        rto_rate = round(
            (rto / total) * 100, 2
        ) if total else 0

        # Estimated direct RTO costs
        cost_per_rto = 169.40
        rto_cost = f"{rto * cost_per_rto:,.2f}"

        # 6. Historical outcomes by decision
        decision_names = [
            "Ship as-is",
            "Ship after confirmation",
            "Nudge to prepaid",
            "Hold / cancel"
        ]

        decisions = []

        for action in decision_names:
            group = df[df["decision"] == action]

            order_count = len(group)

            rto_count = int(
                (group["final_status"] == "RTO").sum()
            )

            rate = round(
                (rto_count / order_count) * 100, 2
            ) if order_count else 0

            decisions.append({
                "decision": action,
                "orders": order_count,
                "rto_count": rto_count,
                "rto_rate": rate
            })

        # 7. Overall order outcomes for doughnut chart
        outcome_counts = {
            "Delivered": delivered,
            "RTO": rto
        }

        # 8. Helper function for category-level RTO rates
        def calculate_rto_rates(column):
            grouped = df.groupby(
                column,
                dropna=False
            ).agg(
                orders=("final_status", "size"),
                rto_count=(
                    "final_status",
                    lambda values: (
                        values == "RTO"
                    ).sum()
                )
            )

            grouped["rto_rate"] = (
                grouped["rto_count"]
                / grouped["orders"]
                * 100
            )

            # Avoid ranking categories with very few orders
            grouped = grouped[
                grouped["orders"] >= 10
            ]

            return grouped.sort_values(
                "rto_rate",
                ascending=False
            )

        # 9. RTO rate by state
        state_data = calculate_rto_rates("state").head(10)

        state_labels = [
            "(Missing)" if pd.isna(value) else str(value)
            for value in state_data.index
        ]

        state_rates = [
            round(float(value), 2)
            for value in state_data["rto_rate"]
        ]

        # 10. RTO rate by courier
        courier_data = calculate_rto_rates("courier")

        courier_labels = [
            "(Missing)" if pd.isna(value) else str(value)
            for value in courier_data.index
        ]

        courier_rates = [
            round(float(value), 2)
            for value in courier_data["rto_rate"]
        ]

        # 11. Render dashboard with all required variables
        return render_template(
            "dashboard.html",
            total_orders=total,
            delivered=delivered,
            rto=rto,
            rto_rate=rto_rate,
            rto_cost=rto_cost,
            decisions=decisions,
            outcome_counts=outcome_counts,
            state_labels=state_labels,
            state_rates=state_rates,
            courier_labels=courier_labels,
            courier_rates=courier_rates,
            experiment_impact=get_experiment_impact(),
        )

    except Exception as e:
        app.logger.exception(
            "Error while loading COD Risk Engine dashboard"
        )
        return f"Dashboard error: {e}", 500

@app.route("/chat")
def chat():
    return render_template("chat.html")


print("REGISTERED ROUTES:")
print(app.url_map)
# Run application
if __name__ == "__main__":
    app.run(debug=True)
