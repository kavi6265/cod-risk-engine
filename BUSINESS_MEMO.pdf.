# Business Memo: COD Risk Engine

**To:** Founder  
**Subject:** Reducing COD RTO risk through explainable decisions  
**Project:** COD Risk Engine

## Executive summary

The COD Risk Engine uses configurable, rule-based scoring to recommend different actions for orders with different risk profiles. The historical dataset indicates that RTO is a meaningful operational cost. The proposed engine should be treated as a decision-support tool until its rules and interventions are validated using real experiment data.

## Historical findings

The supplied dataset contains 2,018 orders: 1,444 marked DELIVERED, 573 marked RTO, and one marked IN_TRANSIT.

1. **Historical RTO rate:** Among the 2,017 finalized orders, 573 were RTO, giving an RTO rate of 28.41%.
2. **Delivery rate:** 1,444 of 2,017 finalized orders were delivered, a delivery rate of approximately 71.59%.
3. **Estimated RTO cost:** At the assumed cost of ₹169.40 per RTO, 573 RTO orders represent an estimated cost of ₹97,066.20.

These figures describe the supplied historical dataset. They do not establish that the risk engine or any intervention has reduced RTO.

## Recommended operating approach

Use configurable risk scores to separate orders into four actions: Ship as-is, Ship after confirmation, Nudge to prepaid, and Hold/cancel. Review high-risk recommendations before taking actions that could unnecessarily lose genuine customers.

Continue the existing COD confirmation process. To evaluate an additional standardized confirmation intervention, randomly assign eligible orders to a control group that continues the normal process and an intervention group that receives the additional step. Track assignments before intervention, record delivery outcomes consistently, and compare finalized RTO rates.

## Financial trade-offs

The estimated ₹169.40 cost per RTO provides a starting point for financial evaluation. The business should compare the cost of additional confirmation, prepaid discounts, and operational reviews against the value of avoided RTOs.

For example, the gross estimated savings from avoiding 10 RTOs would be ₹1,694 at the assumed cost per RTO, before accounting for intervention expenses, lost orders, discount costs, or other effects. This is an illustration, not a measured saving.

## Risks and limitations

- Historical associations do not demonstrate causation.
- Incorrect risk scores may inconvenience genuine customers or lead to lost sales.
- The assumed RTO cost may not capture every relevant cost or recovery.
- The current experiment-results file has no records, so intervention effectiveness remains unknown.

## Priorities for the next two weeks

1. Validate risk rules and thresholds with operations staff.
2. Add automated tests for scoring boundaries and invalid inputs.
3. Establish a randomized control/intervention process with consistent outcome tracking.
4. Collect finalized outcomes and assess RTO differences, sample size, and uncertainty.
5. Review customer complaints, lost orders, prepaid conversion, and intervention costs alongside RTO rate.

## Recommendation

Use the COD Risk Engine as an explainable decision-support tool while validating its rules. Run a properly controlled experiment before claiming that additional confirmation reduces RTO or produces financial savings.
