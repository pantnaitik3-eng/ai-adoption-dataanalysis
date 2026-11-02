"""Generate reproducible summaries and charts for the AI adoption analysis."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ai_adoption_survey.csv"
OUTPUT_PATH = ROOT / "outputs"


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    required = {
        "year",
        "industry",
        "company_size",
        "ai_use_rate",
        "workflow_automation_rate",
        "training_hours",
        "productivity_change_pct",
        "primary_use_case",
        "governance_score",
        "adoption_stage",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if data.empty:
        raise ValueError("The input dataset is empty.")
    if not data["ai_use_rate"].between(0, 100).all():
        raise ValueError("ai_use_rate must be between 0 and 100.")
    if not data["workflow_automation_rate"].between(0, 100).all():
        raise ValueError("workflow_automation_rate must be between 0 and 100.")
    data["adoption_gap"] = (
        data["ai_use_rate"] - data["workflow_automation_rate"]
    )
    return data


def save_summaries(data: pd.DataFrame) -> None:
    yearly = (
        data.groupby("year", as_index=False)
        .agg(
            companies=("industry", "size"),
            avg_ai_use_rate=("ai_use_rate", "mean"),
            avg_automation_rate=("workflow_automation_rate", "mean"),
            avg_productivity_change_pct=("productivity_change_pct", "mean"),
            avg_governance_score=("governance_score", "mean"),
        )
        .round(2)
    )
    industry = (
        data.groupby("industry", as_index=False)
        .agg(
            companies=("year", "size"),
            avg_ai_use_rate=("ai_use_rate", "mean"),
            avg_automation_rate=("workflow_automation_rate", "mean"),
            avg_productivity_change_pct=("productivity_change_pct", "mean"),
        )
        .sort_values("avg_ai_use_rate", ascending=False)
        .round(2)
    )
    size = (
        data.groupby("company_size", as_index=False)
        .agg(
            companies=("year", "size"),
            avg_ai_use_rate=("ai_use_rate", "mean"),
            avg_training_hours=("training_hours", "mean"),
            avg_productivity_change_pct=("productivity_change_pct", "mean"),
        )
        .sort_values("avg_ai_use_rate", ascending=False)
        .round(2)
    )
    yearly.to_csv(OUTPUT_PATH / "executive_summary.csv", index=False)
    industry.to_csv(OUTPUT_PATH / "industry_summary.csv", index=False)
    size.to_csv(OUTPUT_PATH / "size_summary.csv", index=False)


def save_charts(data: pd.DataFrame) -> None:
    yearly = data.groupby("year", as_index=False)["ai_use_rate"].mean()
    plt.figure(figsize=(8, 4.5))
    plt.plot(yearly["year"], yearly["ai_use_rate"], marker="o", linewidth=2.5)
    plt.title("Average AI use in regular workflows")
    plt.xlabel("Year")
    plt.ylabel("Companies reporting regular AI use (%)")
    plt.ylim(0, 100)
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / "adoption_trend.png", dpi=160)
    plt.close()

    industry = data.groupby("industry", as_index=False)["ai_use_rate"].mean()
    industry = industry.sort_values("ai_use_rate")
    plt.figure(figsize=(8, 4.5))
    plt.barh(industry["industry"], industry["ai_use_rate"], color="#2563eb")
    plt.title("Average AI adoption by industry")
    plt.xlabel("Regular AI use (%)")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / "industry_adoption.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.scatter(
        data["ai_use_rate"],
        data["productivity_change_pct"],
        s=65,
        alpha=0.8,
        color="#0f766e",
    )
    correlation = data["ai_use_rate"].corr(data["productivity_change_pct"])
    plt.title(f"Adoption and reported productivity (r = {correlation:.2f})")
    plt.xlabel("Regular AI use (%)")
    plt.ylabel("Reported productivity change (%)")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / "adoption_productivity.png", dpi=160)
    plt.close()


def main() -> None:
    OUTPUT_PATH.mkdir(exist_ok=True)
    data = load_data()
    save_summaries(data)
    save_charts(data)
    correlation = data["ai_use_rate"].corr(data["productivity_change_pct"])
    print(f"Analyzed {len(data)} company-year observations.")
    print(f"Adoption grew from {data.loc[data.year == data.year.min(), 'ai_use_rate'].mean():.1f}% "
          f"to {data.loc[data.year == data.year.max(), 'ai_use_rate'].mean():.1f}%.")
    print(f"Adoption/productivity correlation: {correlation:.2f}")
    print(f"Outputs written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
