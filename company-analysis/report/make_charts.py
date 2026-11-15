"""Make comparison charts for Ross vs TJ Maxx (fiscal year 2024).

Data comes from report/data_2024.csv, which was exported from the
BusMgmtBenchmarks Dolt database with:
  dolt sql -r csv -q "SELECT ... WHERE year = 2024 AND company_name IN ('TJ Maxx','Ross')"
Run from the report folder:  python3 make_charts.py
"""

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- data ---------------------------------------------------------------
df = pd.read_csv("data_2024.csv").set_index("company_name")
COMPANIES = ["TJ Maxx", "Ross"]
COLORS = {"TJ Maxx": "#1f4e79", "Ross": "#c00000"}
YEAR = 2024
OUT = "charts"


def style_axes(ax, ylabel, title):
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)


def grouped_bar(filename, title, ylabel, series, fmt="{:.1f}", ymax_pad=1.25):
    """series: dict of label -> (value_column, extra_scale)"""
    labels = list(series.keys())
    x = range(len(labels))
    panel_w = 5.2 if len(labels) == 1 else 4.2
    fig, axes = plt.subplots(1, len(labels), figsize=(panel_w * len(labels), 5))
    if len(labels) == 1:
        axes = [axes]
    for ax, label in zip(axes, labels):
        col = series[label]
        vals = [df.loc[c, col] for c in COMPANIES]
        bars = ax.bar(COMPANIES, vals, color=[COLORS[c] for c in COMPANIES], width=0.6)
        ax.bar_label(bars, labels=[fmt.format(v) for v in vals], fontsize=11, padding=3)
        style_axes(ax, ylabel, label)
        ax.set_ylim(0, max(vals) * ymax_pad)
    fig.suptitle(title, fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUT}/{filename}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", f"{OUT}/{filename}")


# 1. Net revenue ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 5))
vals = df.loc[COMPANIES, "net_revenue"] / 1_000_000  # thousands -> billions
bars = ax.bar(COMPANIES, vals, color=[COLORS[c] for c in COMPANIES], width=0.6)
ax.bar_label(bars, labels=[f"${v:,.1f}B" for v in vals], fontsize=12, padding=3)
style_axes(ax, "Net revenue (US$ billions)", f"Net revenue, fiscal year {YEAR}")
ax.set_ylim(0, max(vals) * 1.2)
fig.tight_layout()
fig.savefig(f"{OUT}/net_revenue.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("wrote charts/net_revenue.png")

# 2. Profit margins (gross, operating, net) ------------------------------
grouped_bar(
    "profit_margins.png",
    f"Profit margins, fiscal year {YEAR}",
    "Percent of revenue (%)",
    {
        "Gross margin": "gross_margin_pct",
        "Operating margin": "operating_margin_pct",
        "Net margin": "net_margin_pct",
    },
    fmt="{:.1f}%",
)

# 3. SG&A % --------------------------------------------------------------
grouped_bar(
    "sga_pct.png",
    f"SG&A (overhead) as % of revenue, {YEAR}",
    "Percent of revenue (%)",
    {"SG&A %": "sga_pct"},
    fmt="{:.1f}%",
)

# 4. Inventory turnover --------------------------------------------------
grouped_bar(
    "inventory_turnover.png",
    f"Inventory turnover, {YEAR}",
    "Times per year",
    {"Inventory turnover": "inventory_turnover"},
    fmt="{:.2f}",
    ymax_pad=1.2,
)

# 5. Return on assets ----------------------------------------------------
grouped_bar(
    "return_on_assets.png",
    f"Return on assets, {YEAR}",
    "Percent (%)",
    {"Return on assets": "return_on_assets"},
    fmt="{:.1f}%",
)

# 6. ROA decomposition: net margin x asset turnover ----------------------
fig, ax1 = plt.subplots(figsize=(7.5, 5))
labels = ["Net margin\n(%)", "Asset turnover\n(x)"]
x = range(len(labels))
width = 0.35
for i, c in enumerate(COMPANIES):
    vals = [df.loc[c, "net_margin_pct"], df.loc[c, "asset_turnover"]]
    bars = ax1.bar([xx + (i - 0.5) * width for xx in x], vals, width,
                   label=c, color=COLORS[c])
    ax1.bar_label(bars, labels=[f"{v:.2f}" for v in vals], fontsize=10, padding=3)
ax1.set_xticks(list(x))
ax1.set_xticklabels(labels)
style_axes(ax1, "Value", f"Return on assets = net margin x asset turnover ({YEAR})")
ax1.legend(title="Company")
ax1.set_ylim(0, 2.4)
fig.tight_layout()
fig.savefig(f"{OUT}/roa_decomposition.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("wrote charts/roa_decomposition.png")

# 7. Liquidity and leverage ---------------------------------------------
grouped_bar(
    "financial_health.png",
    f"Financial health, {YEAR}",
    "Ratio",
    {"Current ratio": "current_ratio", "Debt to equity": "debt_to_equity"},
    fmt="{:.2f}",
    ymax_pad=1.25,
)

print("done")
