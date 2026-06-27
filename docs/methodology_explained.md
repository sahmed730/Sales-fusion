# 🎓 Methodology Explained (For Non-Technical Audiences)

This document breaks down our complex algorithms into easy-to-understand analogies. Share this with stakeholders who want to know "how it works" without seeing the math.

## 1. How We Predict Revenue (Prophet)
**The Analogy**: Imagine running a coffee shop. You know Monday mornings are always busy, summers are slow, and you always get a huge rush on the day of the town parade. 

**How it Works**: Prophet does exactly this. It learns the "normal" patterns of our business (Mondays vs Sundays, Summer vs Winter) and then we explicitly tell it when our "parades" are happening (our Marketing Campaigns). It combines these two things to draw a highly accurate trendline of future sales.

## 2. How We Predict Product Demand (XGBoost)
**The Analogy**: Imagine a panel of 100 experts trying to guess how many laptops we will sell tomorrow. Expert 1 looks at the day of the week, Expert 2 looks at the region, and Expert 3 looks at what we sold yesterday. They all vote, and the consensus is usually incredibly accurate.

**How it Works**: XGBoost builds hundreds of small "decision trees" (our experts). Each tree learns from the mistakes of the previous one. When it's time to predict demand, the algorithm aggregates the knowledge of all these trees to give us the final number.

## 3. How We Find Problems (Isolation Forest)
**The Analogy**: If you have a bag of 100 identical red marbles and 1 blue marble, finding the blue marble is extremely fast because it's isolated by its differences. 

**How it Works**: The Isolation Forest algorithm randomly slices up our data. Normal data points require a lot of slicing to separate because they are clustered tightly together. Anomalous data points (like a sudden 50% drop in revenue) get separated almost instantly. We flag the data points that get isolated the fastest.
