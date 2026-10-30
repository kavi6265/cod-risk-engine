
import pandas as pd

df = pd.read_csv("orders_sample.csv")
df.columns = df.columns.str.strip()

df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)

df = df[df["final_status"].isin(["DELIVERED", "RTO"])].copy()

# Assignment-provided financial assumptions
FORWARD_SHIPPING = 65
RETURN_SHIPPING = 65
PACKAGING = 25
DAMAGE_RATE = 0.08
PRODUCT_COST = 180
ORDER_VALUE = 649
GROSS_MARGIN = 0.62

# Expected direct cost per RTO
rto_cost = (
    FORWARD_SHIPPING
    + RETURN_SHIPPING
    + PACKAGING
    + DAMAGE_RATE * PRODUCT_COST
)

delivered = (df["final_status"] == "DELIVERED").sum()
rto = (df["final_status"] == "RTO").sum()

# Approximate gross profit on a delivered order
gross_profit = ORDER_VALUE * GROSS_MARGIN

print("\n--- HISTORICAL FINANCIAL BASELINE ---")
print("Finalized orders:", len(df))
print("Delivered:", delivered)
print("RTO orders:", rto)
print("RTO rate:", round(rto / len(df) * 100, 2), "%")
print("Expected direct cost per RTO: Rs.", round(rto_cost, 2))
print("Estimated direct RTO costs: Rs.", round(rto * rto_cost, 2))
print("Gross profit per delivered order: Rs.", round(gross_profit, 2))

# Illustrative prepaid incentive
discount = 20
rto_rate_cod = 0.28
rto_rate_prepaid = 0.04

expected_rto_cost_reduction = (
    (rto_rate_cod - rto_rate_prepaid) * rto_cost
)

print("\n--- PREPAID INCENTIVE EXAMPLE ---")
print("Illustrative discount: Rs.", discount)
print(
    "Expected RTO cost reduction per converted order: Rs.",
    round(expected_rto_cost_reduction, 2)
)
print(
    "Difference before conversion effects: Rs.",
    round(expected_rto_cost_reduction - discount, 2)
)

print("\nNote: These are estimates based on assignment assumptions.")
print("They are not measured savings from the proposed engine.")
