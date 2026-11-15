# Ross vs TJ Maxx — Fiscal Year 2024 Comparison

*Source: `calvinw/BusMgmtBenchmarks` Dolt database. Both companies are in the
**Off Price** segment and both report in **USD, in thousands**. All figures are
for fiscal year **2024** (TJ Maxx's year ended 2025-02-01, Ross's ended
2025-02-01). All ratios come from the `financial_metrics` table; raw dollars
come from `financials`.*

## The two companies

| | TJ Maxx | Ross |
|---|---|---|
| Segment / subsegment | Off Price | Off Price |
| What they sell | Off-price apparel and home fashions | Off-price apparel, accessories and footwear |
| Ticker | TJX | ROST |
| Currency / units | USD, thousands | USD, thousands |

Because both report in USD, their dollar amounts can be compared directly.

## Key numbers, fiscal year 2024

SQL used:

```sql
SELECT fm.company_name,
       f.`Net Revenue` AS net_revenue,
       fm.Gross_Margin_Percentage AS gross_margin_pct,
       fm.Operating_Profit_Margin_Percentage AS op_margin_pct,
       fm.Net_Profit_Margin_Percentage AS net_margin_pct,
       fm.SGA_Percentage AS sga_pct,
       fm.Inventory_Turnover AS inventory_turnover,
       fm.Current_Ratio AS current_ratio,
       fm.Asset_Turnover AS asset_turnover,
       fm.Return_on_Assets AS return_on_assets,
       fm.Debt_to_Equity AS debt_to_equity
FROM financial_metrics fm
JOIN financials f
  ON f.company_name = fm.company_name AND f.year = fm.year
WHERE fm.year = 2024 AND fm.company_name IN ('TJ Maxx', 'Ross');
```

| Measure | Ross | TJ Maxx | Edge |
|---|---|---|---|
| Net revenue (US$ thousands) | 21,129,219 | 56,360,000 | TJ Maxx |
| Gross margin (US$ thousands) | 5,868,713 | 17,248,000 | TJ Maxx |
| Operating profit (US$ thousands) | 2,585,586 | 6,483,000 | TJ Maxx |
| Net profit (US$ thousands) | 2,090,730 | 4,864,000 | TJ Maxx |
| Gross margin % | 27.78% | 30.60% | TJ Maxx |
| Operating profit margin % | 12.24% | 11.50% | Ross |
| Net profit margin % | 9.90% | 8.63% | Ross |
| SG&A % of revenue | 15.54% | 19.42% | Ross (lower is better) |
| Inventory turnover | 6.24 | 6.09 | Ross |
| Current ratio | 1.62 | 1.18 | Ross |
| Asset turnover | 1.42 | 1.78 | TJ Maxx |
| Return on assets | 14.03% | 15.32% | TJ Maxx |
| Debt to equity | 1.71 | 2.78 | Ross (lower is safer) |

## Findings

1. **TJ Maxx is far larger.** Net revenue of about **$56.4 billion** vs Ross's
   **$21.1 billion** — roughly 2.7 times bigger. It also earns more profit in
   total: net profit of **$4.86 billion** vs Ross's **$2.09 billion**.

2. **But Ross is more profitable per dollar of sales.** Ross keeps **9.90%**
   of every sales dollar as net profit, versus **8.63%** for TJ Maxx. The
   operating margin tells the same story (12.24% vs 11.50%).

3. **The reason is overhead.** TJ Maxx starts ahead: its gross margin is
   **30.60%** vs Ross's **27.78%**, so it buys (or prices) better at the top
   of the income statement. But SG&A — the cost of running stores and head
   office — is **15.54%** of sales at Ross but **19.42%** at TJ Maxx, almost
   4 points higher. Ross is the leaner operation, so its higher overhead-free
   portion carries all the way to the bottom line and it ends up the more
   profitable company per dollar of sales.

4. **Inventory management is a near tie, with Ross a whisker ahead.** Ross
   turns its inventory **6.24** times a year vs **6.09** for TJ Maxx. In
   off-price fashion, faster turns mean less stock has to be marked down.

5. **TJ Maxx wins on return on assets, and the reason is asset turnover.**
   ROA is **15.32%** at TJ Maxx vs **14.03%** at Ross. Using the standard
   breakdown, **ROA = net profit margin × asset turnover**:

   | | Net margin | Asset turnover | = ROA | Reported ROA |
   |---|---|---|---|---|
   | Ross | 9.90% | 1.42 | 14.03% | 14.03% |
   | TJ Maxx | 8.63% | 1.78 | 15.32% | 15.32% |

   Ross wins the first half (better margin), but TJ Maxx wins the second half
   by more: it generates about **25% more sales for each dollar of assets**
   (turnover 1.78 vs 1.42). So TJ Maxx's assets work harder, and that outweighs
   its thinner margin.

6. **Ross is in the stronger financial position.** Its current ratio is
   **1.62** vs **1.18**, meaning a bigger cushion to pay short-term bills. Its
   debt to equity is **1.71** vs **2.78**, meaning it relies less on borrowed
   money. TJ Maxx carries more debt for its size.

## Conclusion

TJ Maxx is the **bigger** and **more asset-efficient** business; Ross is the
**leaner**, **more profitable-per-sale** and **financially safer** one. The
cleanest way to say it: TJ Maxx makes more money in total by being large and
turning its assets hard, while Ross makes more money on each sale by keeping
overhead low and running a stronger balance sheet.
