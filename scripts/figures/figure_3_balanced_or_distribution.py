import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
import os


data_dir = Path(os.environ.get("GEP_DATA_DIR", Path.cwd() / "data"))
save_dir = Path(os.environ.get("GEP_FIGURES_DIR", Path.cwd() / "figures"))
save_dir.mkdir(parents=True, exist_ok=True)
MAX_PNG_DIMENSION = 1200

rep_inc = pd.read_csv(
    data_dir / "balanced_runs_including_misgendering.csv"
)
rep_exc = pd.read_csv(
    data_dir / "balanced_runs_excluding_misgendering.csv"
)

sns.set(style="white", font_scale=1.0)

plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

plot_df = pd.concat(
    [
        rep_inc[["OR_GEP"]].assign(Analysis="Including misgendering"),
        rep_exc[["OR_GEP"]].assign(Analysis="Excluding misgendering"),
    ],
    ignore_index=True,
)

palette = {
    "Including misgendering": "#2b8cbe",
    "Excluding misgendering": "#7bccc4",
}

median_inc = rep_inc["OR_GEP"].median()
median_exc = rep_exc["OR_GEP"].median()

fig, ax = plt.subplots(figsize=(8, 6))

sns.kdeplot(
    data=plot_df,
    x="OR_GEP",
    hue="Analysis",
    palette=palette,
    fill=True,
    common_norm=False,
    alpha=0.45,
    linewidth=2,
    ax=ax,
)

# Median lines
ax.axvline(median_inc, color="#2b8cbe", linestyle="--", linewidth=2)
ax.axvline(median_exc, color="#7bccc4", linestyle="--", linewidth=2)

# Get y-axis maximum
ymax = ax.get_ylim()[1]

# Place labels inside the plot near the top
ax.text(
    median_exc,
    ymax * 0.98,
    f"Median OR={median_exc:.2f}",
    color="#7bccc4",
    ha="center",
    va="bottom",
    fontsize=10,
    fontweight="bold",
    bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=2),
)

ax.text(
    median_inc,
    ymax * 0.98,
    f"Median OR={median_inc:.2f}",
    color="#2b8cbe",
    ha="center",
    va="bottom",
    fontsize=10,
    fontweight="bold",
    bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=2),
)

ax.set_xlabel("OR for GEP status")
ax.set_ylabel("Density")
ax.set_title(
    "Distribution of GEP ORs across 100 balanced subsamples",
    pad=20,
)

# Access and modify the existing legend
legend = ax.get_legend()
if legend:
    for text in legend.get_texts():
        text.set_fontsize(8)
    legend.set_title("")
    legend.set_bbox_to_anchor((0.5, 1.0))
    if hasattr(legend, "set_loc"):
        legend.set_loc("upper center")
    else:
        legend._loc = 9  # Matplotlib location code for "upper center"

plt.tight_layout()

# Preserve the original 8 x 6 inch layout while limiting the PNG to
# 1200 pixels on its longest side, as required by JMIR.
png_dpi = min(600, MAX_PNG_DIMENSION / max(fig.get_size_inches()))
fig.savefig(
    save_dir / "balanced_OR_distribution.png",
    dpi=png_dpi,
    bbox_inches=None,
    pad_inches=0,
    facecolor="white",
    transparent=False,
)

fig.savefig(
    save_dir / "balanced_OR_distribution.pdf",
    bbox_inches="tight",
)

plt.show()
