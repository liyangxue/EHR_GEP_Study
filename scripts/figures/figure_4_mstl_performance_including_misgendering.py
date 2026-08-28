import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os


# ==== DataFrame setup ====
data = {
    "Model": [
        "Longformer: T", "Longformer: ST", "Longformer: SST",
        "Longformer: T", "Longformer: ST", "Longformer: SST",
        "Longformer: T", "Longformer: ST", "Longformer: SST",
    ],
    "Group": [
        "Overall", "Overall", "Overall",
        "GEP=0", "GEP=0", "GEP=0",
        "GEP=1", "GEP=1", "GEP=1",
    ],
    "Accuracy": [
        0.738727, 0.753316, 0.767905,
        0.827320, 0.822165, 0.842784,
        0.644809, 0.680328, 0.688525,
    ],
    "Precision": [
        0.803738, 0.745645, 0.771429,
        0.690476, 0.629310, 0.643939,
        0.876923, 0.824561, 0.885135,
    ],
    "Recall": [
        0.525994, 0.654434, 0.660550,
        0.585859, 0.737374, 0.858586,
        0.500000, 0.618421, 0.574561,
    ],
    "F1-score": [
        0.635860, 0.697068, 0.711697,
        0.633880, 0.679070, 0.735931,
        0.636872, 0.706767, 0.696809,
    ],
    "AUC": [
        0.835665, 0.798301, 0.829649,
        0.891860, 0.876271, 0.917619,
        0.775140, 0.743961, 0.776093,
    ],
}
df = pd.DataFrame(data)

# ==== Reshape for plotting ====
df_melted = df.melt(
    id_vars=["Model", "Group"],
    value_vars=["Accuracy", "Precision", "Recall", "F1-score", "AUC"],
    var_name="Metric",
    value_name="Score",
)

# ==== Plot setup ====
custom_params = {"axes.grid": False, "axes.facecolor": "white"}
sns.set_theme(style="white", rc=custom_params, font_scale=1.2)
palette_gnbu = ["#7bccc4", "#2b8cbe", "#0868ac"]

groups = ["Overall", "GEP=0", "GEP=1"]
fig, axes = plt.subplots(3, 1, figsize=(10, 13), sharey=True)

# ==== Create vertically stacked bar plots ====
for i, grp in enumerate(groups):
    ax = axes[i]
    sub_df = df_melted[df_melted["Group"] == grp]
    sns.barplot(
        data=sub_df,
        x="Metric",
        y="Score",
        hue="Model",
        palette=palette_gnbu,
        ax=ax,
    )
    ax.set_title(grp, fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("Performance" if i == 1 else "")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x")
    ax.grid(False)
    ax.set_facecolor("white")

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.2f",
            fontsize=10,
            label_type="edge",
            padding=2,
        )
    ax.get_legend().remove()

# ==== Shared legend below all subplots ====
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    title="Model",
    loc="lower center",
    ncol=3,
    frameon=True,
    bbox_to_anchor=(0.5, 0.01),
)

# The caption supplies the overall figure title.
plt.tight_layout(rect=[0, 0.08, 1, 1])

# ==== Save files ====
save_dir = Path(os.environ.get("GEP_FIGURES_DIR", Path.cwd() / "figures"))
save_dir.mkdir(parents=True, exist_ok=True)
png_path = save_dir / "MSTL_GEP_Performance.png"
eps_path = save_dir / "MSTL_GEP_Performance.eps"

max_png_dimension = 1200
png_dpi = min(600, max_png_dimension / max(fig.get_size_inches()))
fig.savefig(
    png_path,
    dpi=png_dpi,
    bbox_inches=None,
    pad_inches=0,
    facecolor="white",
    transparent=False,
)
fig.savefig(
    eps_path,
    format="eps",
    bbox_inches="tight",
    transparent=False,
)
plt.show()

print(f"Figures saved to:\n  PNG: {png_path}\n  EPS: {eps_path}")
