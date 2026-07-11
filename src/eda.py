"""Generate Phase 1 EDA plots for the cleaned Heart Disease dataset."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.data_processing import NUMERIC_FEATURES


DATA_PATH = Path("data/processed/heart_cleveland_clean.csv")
OUTPUT_DIR = Path("screenshots/phase1_eda")


def save_numeric_histograms(data: pd.DataFrame, output_dir: Path) -> Path:
    """Save histograms for the main continuous clinical features."""
    output_path = output_dir / "numeric_feature_histograms.png"
    axes = data[NUMERIC_FEATURES].hist(
        bins=20,
        figsize=(12, 8),
        color="#4c78a8",
        edgecolor="white",
    )

    for axis in axes.flatten():
        axis.set_ylabel("Patient count")
        axis.grid(False)

    title = "Heart Disease Dataset: Numeric Feature Distributions"
    plt.suptitle(title, y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()
    return output_path


def save_correlation_heatmap(data: pd.DataFrame, output_dir: Path) -> Path:
    """Save a correlation heatmap for numeric encoded features."""
    output_path = output_dir / "correlation_heatmap.png"
    plt.figure(figsize=(11, 9))
    sns.heatmap(
        data.corr(numeric_only=True),
        cmap="vlag",
        center=0,
        annot=False,
        linewidths=0.4,
        cbar_kws={"label": "Pearson correlation"},
    )
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()
    return output_path


def save_class_balance(data: pd.DataFrame, output_dir: Path) -> Path:
    """Save a bar chart showing the binary target class balance."""
    output_path = output_dir / "class_balance.png"
    class_counts = (
        data["target"]
        .map({0: "No disease", 1: "Disease"})
        .value_counts()
        .rename_axis("class")
        .reset_index(name="count")
    )

    plt.figure(figsize=(7, 5))
    sns.barplot(
        data=class_counts,
        x="class",
        y="count",
        hue="class",
        legend=False,
    )
    plt.title("Target Class Balance")
    plt.xlabel("Target class")
    plt.ylabel("Patient count")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()
    return output_path


def generate_eda_plots(
    data_path: Path = DATA_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> list[Path]:
    """Generate and save all Phase 1 EDA plots."""
    output_dir.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(data_path)

    plot_paths = [
        save_numeric_histograms(data, output_dir),
        save_correlation_heatmap(data, output_dir),
        save_class_balance(data, output_dir),
    ]
    return plot_paths


def main() -> None:
    """CLI entrypoint for EDA plot generation."""
    for plot_path in generate_eda_plots():
        print(f"Saved {plot_path}")


if __name__ == "__main__":
    main()
