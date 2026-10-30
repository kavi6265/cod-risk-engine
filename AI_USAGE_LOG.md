# AI Usage Log — COD Risk Engine

## Tools used
- **ChatGPT:** Used for implementation guidance, debugging support, dashboard improvements, documentation drafts, and Git/GitHub workflow guidance.
- **VS Code and Python:** Used to edit, run, and check the application.
- **Git and GitHub:** Used for source-code version control and repository submission.

## Examples of AI-assisted work and validation

### 1. Experiment-results file path
- **Initial issue:** The experiment-results function used a relative file path, which could depend on the working directory.
- **AI assistance:** Suggested using a path relative to the application directory.
- **Validation:** Checked the updated Python syntax and restarted the Flask application. The dashboard loaded successfully, but the empty experiment file still produced zero group counts, as expected.
- **Lesson:** Successful page loading does not prove that the experiment has produced results.

### 2. Interpreting historical RTO results
- **Potentially misleading conclusion:** A lower historical RTO rate for one category could be mistaken for proof that a risk-based intervention caused the reduction.
- **Correction:** Kept historical outcomes separate from experimental results and documented the need for randomized group assignment and finalized outcomes.
- **Lesson:** Observational associations should not be presented as causal effects.

### 3. Experiment dashboard with no data
- **Initial limitation:** The experiment CSV contained only column headers.
- **AI assistance:** Explained why the dashboard showed zero control and intervention orders and helped establish the expected data structure.
- **Validation:** Confirmed that no real experiment records had yet been entered.
- **Lesson:** Do not fabricate records to make a dashboard look complete. Report the experiment as not yet measured.

## Human review
I reviewed the AI-assisted suggestions, checked the application locally, and retained the distinction between implemented features, simulated workflows, historical findings, and unmeasured experiment results. The final submitted code and documentation should reflect what I actually tested and understood.
