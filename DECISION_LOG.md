# Decision Log — COD Risk Engine

## 1. Configurable risk thresholds
- **Decision:** Store risk thresholds and weights in `config.json`.
- **Alternative considered:** Hard-code thresholds in `app.py`.
- **Reason:** Non-technical team members can adjust the thresholds without changing Python code.

## 2. Four risk-based actions
- **Decision:** Use four actions: Ship as-is, Ship after confirmation, Nudge to prepaid, and Hold/cancel.
- **Alternative considered:** Automatically cancel every high-risk order.
- **Reason:** This balances reducing RTO costs with avoiding the loss of genuine customers.

## 3. Rule-based risk scoring
- **Decision:** Use Python rules for customer history, state, courier, address, and suspicious names.
- **Alternative considered:** Use an LLM for every risk calculation.
- **Reason:** Rules and calculations are predictable, easy to explain, and easier to test. An LLM could help with more complex address interpretation.

## 4. Explainable decisions
- **Decision:** Return a risk score, recommended action, and plain-English reasons.
- **Alternative considered:** Return only a risk score.
- **Reason:** Operations staff need to understand why an order received a particular recommendation.

## 5. Mock confirmation flow
- **Decision:** Build a chat simulator for confirmation and prepaid-offer scenarios.
- **Alternative considered:** Integrate a live WhatsApp API.
- **Reason:** A simulator demonstrates the workflow without requiring a real WhatsApp account or paid integration.

## 6. Historical dashboard
- **Decision:** Use the supplied historical order dataset to display delivery outcomes, RTO rates, and estimated RTO costs.
- **Alternative considered:** Show only total order counts.
- **Reason:** The business needs to understand both operational performance and financial impact.

## 7. Experiment measurement
- **Decision:** Add an experiment-results CSV to compare control and intervention groups.
- **Alternative considered:** Assume that historical risk-based decisions reduced RTO.
- **Reason:** Historical associations alone do not prove that an intervention caused a reduction. Real experiment results are needed to evaluate impact.

## 8. Current limitations
- The confirmation flow is a mock, not a live WhatsApp integration.
- The experiment-results file currently contains headers only; real-world intervention impact has not yet been measured.
- The risk thresholds and weights require further validation using appropriate test data and business outcomes.