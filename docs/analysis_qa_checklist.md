# ✅ Analysis QA Checklist

Before delivering any insights, models, or dashboards to stakeholders, the analyst (or AI Agent) MUST complete this checklist to guarantee data integrity and report quality.

### Section 1: Data Integrity
- [ ] Has the `data-quality-audit` been run on all source files?
- [ ] Did the metric reconciliation script (`reconcile_metrics.py`) pass without discrepancies?
- [ ] Have all missing values and anomalies been accounted for and documented in `assumptions.md`?

### Section 2: Model Validation
- [ ] Is the Forecast Error Rate (MAPE) below the acceptable threshold of 15%?
- [ ] Have the features driving the XGBoost model been reviewed for data leakage?
- [ ] Are the anomaly detection bounds reasonable? (i.e. we aren't flagging 50% of the dataset as anomalous).

### Section 3: Storytelling & Presentation
- [ ] Are all technical terms translated using the `business_translations.md` glossary?
- [ ] Does the Executive Summary start with a clear Bottom Line Up Front (BLUF)?
- [ ] Does every insight include an estimated ROI or business impact?
- [ ] Is the Streamlit dashboard rendering correctly without errors?

**Reviewed By**: 
**Date**: 
**Status**: [PASS / FAIL]
