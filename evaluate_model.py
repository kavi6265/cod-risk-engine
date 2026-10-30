
import pandas as pd

df = pd.read_csv("orders_sample.csv")
df.columns = df.columns.str.strip()

df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)

df = df[df["final_status"].isin(["DELIVERED", "RTO"])].copy()


def decide(row):
    risk = 0

    previous_rto = int(row["customer_prior_rto"] or 0)

    if previous_rto >= 2:
        risk += 40
    elif previous_rto == 1:
        risk += 15

    state = str(row["state"]).strip().title()

    if state in ["Bihar", "Uttar Pradesh"]:
        risk += 15
    elif state in ["Madhya Pradesh", "Assam"]:
        risk += 8

    courier = str(row["courier"]).strip().lower()
    if courier == "xpressbees":
        risk += 5

    source = str(row["utm_source"]).strip().lower()
    if source == "meta_ads":
        risk += 3

    address = str(row["address"]).strip()
    if len(address) < 15:
        risk += 20

    name = str(row["customer_name"]).strip().lower()
    if name in {"asdf", "test", "abc", "unknown"}:
        risk += 35

    risk = min(risk, 100)

    if risk <= 24:
        return "Ship as-is"
    elif risk <= 44:
        return "Ship after confirmation"
    elif risk <= 69:
        return "Nudge to prepaid"
    else:
        return "Hold / cancel"


df["decision"] = df.apply(decide, axis=1)

print("\n--- DECISION COUNTS ---")
print(df["decision"].value_counts())

print("\n--- OUTCOME RATE BY DECISION ---")
summary = df.groupby("decision").agg(
    orders=("final_status", "size"),
    rto_count=("final_status", lambda s: (s == "RTO").sum()),
    rto_rate=("final_status", lambda s: (s == "RTO").mean() * 100)
)

print(summary.round(2))

print("\n--- RTO RATE BY DECISION ---")
print(
    df.groupby("decision")["final_status"]
    .apply(lambda s: round((s == "RTO").mean() * 100, 2))
)

print("\nNote: These are historical associations, not proof")
print("that the proposed actions would have prevented RTOs.")
