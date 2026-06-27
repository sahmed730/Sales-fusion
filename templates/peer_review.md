# 🤝 Peer Review Template

**Reviewer Name:** 
**Author Name:** 
**Date:** 

## 1. Code Quality & Modularity
- [ ] Are there hardcoded paths? (Should use relative paths like `data/` instead of `c:/users/...`)
- [ ] Are functions modular and reusable?
- [ ] Is error handling implemented for missing files or bad data?

## 2. Statistical / Algorithmic Validity
- [ ] Is the correct model being used for the problem? (e.g. Prophet for time-series, XGBoost for feature-heavy demand prediction).
- [ ] Has data leakage been prevented? (e.g. testing data isn't leaking into training).
- [ ] Are hyperparameter choices logical or validated via GridSearch?

## 3. Documentation
- [ ] Has the `data_dictionary.md` been updated if new columns were engineered?
- [ ] Have the assumptions been logged in `assumptions.md`?

## 📝 Reviewer Comments
*Please provide constructive feedback below.*
