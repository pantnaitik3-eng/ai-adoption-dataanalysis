# AI Adoption in Everyday Business Work

An end-to-end data analytics project that explores how companies adopt AI in
regular workflows, which use cases appear first, and whether adoption is
associated with reported productivity gains.

## What this project demonstrates

- Reproducible analysis with Python, pandas, and matplotlib
- Data validation and derived KPI creation
- Year-over-year adoption trends
- Industry and company-size segmentation
- A simple relationship analysis between adoption and productivity
- Exported summary tables and presentation-ready charts

## Dataset note

`data/ai_adoption_survey.csv` is a small **illustrative survey-style dataset**
created for this portfolio project. It is not presented as a real survey or as
causal evidence. The dataset intentionally has a clear schema so the analysis
workflow can be replaced with a real survey export without changing the report
logic.

## Run it

```powershell
cd analytics/ai-adoption-analysis
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/analyze.py
```

The script writes files to `outputs/`:

- `executive_summary.csv`
- `industry_summary.csv`
- `size_summary.csv`
- `adoption_trend.png`
- `industry_adoption.png`
- `adoption_productivity.png`

## Questions answered

1. How did the share of companies using AI in regular workflows change from
   2022 to 2025?
2. Which industries and company sizes report the highest adoption?
3. Which everyday use cases are most common?
4. Is higher adoption associated with higher reported productivity?

## Key caveats

The analysis describes association, not causation. The data is illustrative,
self-reported, and intentionally small. A production analysis should add
sampling weights, confidence intervals, missing-data treatment, and controls
for company size, geography, industry, and pre-existing productivity trends.
