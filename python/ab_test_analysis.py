import math
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

control_sessions = 10044
control_purchases = 775
variant_sessions = 9956
variant_purchases = 978

control_rate = control_purchases / control_sessions
variant_rate = variant_purchases / variant_sessions

absolute_uplift = variant_rate - control_rate
relative_uplift = absolute_uplift / control_rate

standard_error = math.sqrt(
    (control_rate * (1 - control_rate) / control_sessions)
    + (variant_rate * (1 - variant_rate) / variant_sessions)
)

# Z-statistic
z_statistic = absolute_uplift / standard_error

# Two-sided p-value
p_value = 2 * (1 - norm.cdf(abs(z_statistic)))

# 95% confidence interval
margin_of_error = 1.96 * standard_error

ci_lower = absolute_uplift - margin_of_error
ci_upper = absolute_uplift + margin_of_error


print("ShopSphere A/B Test Analysis")
print("-----------------------------")

print(f"Control conversion rate: {control_rate:.4%}")
print(f"Variant conversion rate: {variant_rate:.4%}")

print(f"\nAbsolute uplift: {absolute_uplift:.4%}")
print(f"Relative uplift: {relative_uplift:.2%}")

print(f"\nZ-statistic: {z_statistic:.2f}")
print(f"P-value: {p_value:.10f}")

print(
    f"95% confidence interval: "
    f"{ci_lower:.4%} to {ci_upper:.4%}"
)

variants = ["Control", "Variant"]

conversion_rates = [7.7160, 9.8232]
revenue_per_session = [20.81, 25.29]

# Conversion rate chart
plt.figure(figsize=(8, 5))

plt.bar(variants, conversion_rates)

plt.title("Conversion Rate: Control vs Variant")
plt.xlabel("Experiment Variant")
plt.ylabel("Conversion Rate (%)")

plt.tight_layout()
plt.savefig("data/processed/ab_conversion_rate.png", dpi=150)

plt.show()

# Revenue per session chart
plt.figure(figsize=(8, 5))

plt.bar(variants, revenue_per_session)

plt.title("Revenue per Session: Control vs Variant")
plt.xlabel("Experiment Variant")
plt.ylabel("Revenue per Session (£)")

plt.tight_layout()
plt.savefig("data/processed/ab_revenue_per_session.png", dpi=150)

plt.show()

ab_results = pd.DataFrame({
    "experiment_variant": ["Control", "Variant"],
    "sessions": [10044, 9956],
    "purchases": [775, 978],
    "conversion_rate_pct": [7.7160, 9.8232],
    "revenue": [208997.09, 251790.56],
    "revenue_per_session": [20.81, 25.29],
    "average_order_value": [269.67, 257.45]
})

ab_results.to_csv(
    "data/processed/ab_test_results.csv",
    index=False
)

print("\nA/B results saved to data/processed/ab_test_results.csv")