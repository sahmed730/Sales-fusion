# 🔄 Analysis Retrospective: Q2 Regional Anomaly Investigation

**Date**: June 2026
**Lead**: AI Agent & Umar

## 1. What Went Well?
- The automated `root_cause_analysis.py` script accurately identified the 18% drop in South India's revenue within seconds.
- The Isolation Forest algorithm successfully isolated the behavior from standard seasonality.

## 2. What Didn't Go Well?
- We initially lacked context on why the AOV dropped. The data showed the drop, but we had to manually cross-reference the promotional discount codes to realize it was due to a flawed marketing campaign.

## 3. Learnings & Action Items
- **Action Item**: Integrate `campaigns.csv` directly into the `root_cause_analysis.py` script so that it automatically correlates revenue drops with active discount codes.
- **Action Item**: Lower the sensitivity on the Isolation Forest (`contamination=0.05` to `0.03`) as it flagged a minor dip in North India that was actually just a public holiday.
