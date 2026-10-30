
import pandas as pd

df = pd.read_csv("orders_sample.csv")
df.columns = df.columns.str.strip()

# Keep only orders with a finalized outcome
df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)

data = df[df["final_status"].isin(["DELIVERED", "RTO"])].copy()

print("TOTAL ORDERS:", len(df))
print("FINALIZED ORDERS:", len(data))
print("DELIVERED:", (data["final_status"] == "DELIVERED").sum())
print("RTO:", (data["final_status"] == "RTO").sum())
print("OVERALL RTO RATE:",
      round((data["final_status"] == "RTO").mean() * 100, 2), "%")


def show_rto_rates(column, minimum_orders=20):
    if column not in data.columns:
        print(f"\nMissing column: {column}")
        return

    summary = data.groupby(column, dropna=False).agg(
        orders=("final_status", "size"),
        rto_count=("final_status", lambda s: (s == "RTO").sum()),
        rto_rate=("final_status", lambda s: (s == "RTO").mean() * 100)
    )

    summary = summary[summary["orders"] >= minimum_orders]
    summary = summary.sort_values("rto_rate", ascending=False)

    print(f"\n--- RTO RATE BY {column.upper()} ---")
    print(summary.round(2).to_string())


show_rto_rates("customer_prior_rto")
show_rto_rates("customer_prior_orders")
show_rto_rates("state")
show_rto_rates("courier")
show_rto_rates("utm_source")

# Save a copy of the analysis results
data.to_csv("finalized_orders.csv", index=False)
print("\nSaved finalized orders to finalized_orders.csv")
