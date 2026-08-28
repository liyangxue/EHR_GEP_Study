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
        0.809019, 0.802387, 0.827586,
        0.827320, 0.822165, 0.842784,
        0.789617, 0.781421, 0.811475,
    ],
    "Precision": [
        0.752336, 0.679443, 0.717857,
        0.690476, 0.629310, 0.643939,
        0.792308, 0.713450, 0.783784,
    ],
    "Recall": [
        0.638889, 0.773810, 0.797619,
        0.585859, 0.737374, 0.858586,
        0.673203, 0.797386, 0.758170,
    ],
    "F1-score": [
        0.690987, 0.723562, 0.755639,
        0.633880, 0.679070, 0.735931,
        0.727915, 0.753086, 0.770764,
    ],
    "AUC": [
        0.891260, 0.873016, 0.898968,
        0.891860, 0.876271, 0.917619,
        0.884347, 0.862684, 0.879959,
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
png_path = save_dir / "MSTL_GEP_Performance_no_misgender.png"
eps_path = save_dir / "MSTL_GEP_Performance_no_misgender.eps"

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
