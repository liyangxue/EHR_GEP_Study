import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import os
from pathlib import Path


# =========================
# Save directory
# =========================
save_dir = Path(os.environ.get("GEP_FIGURES_DIR", Path.cwd() / "figures"))
os.makedirs(save_dir, exist_ok=True)
MAX_PNG_DIMENSION = 1200

# =========================
# Models and order
# =========================
models = ["BERT", "ClinicalBERT", "Longformer\n(GEP base)", "MSTL\nLongformer"]
n_models = len(models)
x = np.arange(n_models)


# =========================
# Formatter for labels
# =========================
def format_val(val):
    if abs(val) < 0.01:
        return "<0.01"
    return f"{val:.2f}"


# =========================
# Including misgendering
# =========================
acc_overall_baseline = np.array([77.48, 74.17, 72.85, 82.78])
acc_gep0_baseline = np.array([84.81, 77.22, 77.22, 88.61])
acc_gep1_baseline = np.array([69.44, 70.83, 68.06, 76.39])

delta_fpr_baseline = np.array([43.38, 15.00, 31.51, 15.76])
delta_tpr_baseline = np.array([17.22, 0.56, 10.00, 7.22])

acc_overall_best = np.array([80.13, 77.48, 76.82, 84.77])
acc_gep0_best = np.array([84.81, 84.81, 78.48, 86.08])
acc_gep1_best = np.array([75.00, 69.44, 75.00, 83.33])

delta_fpr_best = np.array([45.07, 74.07, 32.27, 21.16])
delta_tpr_best = np.array([31.11, 55.56, 44.44, 21.11])

acc_overall_fair = np.array([74.17, 71.52, 78.15, 83.44])
acc_gep0_fair = np.array([72.15, 74.68, 75.95, 86.08])
acc_gep1_fair = np.array([76.39, 68.06, 80.56, 80.56])

delta_fpr_fair = np.array([4.83, 7.60, 11.61, 6.65])
delta_tpr_fair = np.array([0.56, 1.67, 11.11, 0.00])

# =========================
# Excluding misgendering
# =========================
acc_overall_baseline_excl = np.array([80.79, 78.15, 80.13, 88.08])
acc_gep0_baseline_excl = np.array([84.81, 79.75, 83.54, 89.87])
acc_gep1_baseline_excl = np.array([76.39, 76.39, 76.39, 86.11])

delta_fpr_baseline_excl = np.array([14.63, 13.48, 5.00, 3.72])
delta_tpr_baseline_excl = np.array([24.52, 29.19, 10.81, 1.13])

acc_overall_best_excl = np.array([83.44, 83.44, 86.75, 89.40])
acc_gep0_best_excl = np.array([84.81, 83.54, 87.34, 92.41])
acc_gep1_best_excl = np.array([81.94, 83.33, 86.11, 86.11])

delta_fpr_best_excl = np.array([25.88, 11.78, 9.34, 11.24])
delta_tpr_best_excl = np.array([46.77, 25.32, 13.55, 7.10])

acc_overall_fair_excl = np.array([82.12, 82.78, 84.77, 88.08])
acc_gep0_fair_excl = np.array([82.28, 84.81, 87.34, 89.87])
acc_gep1_fair_excl = np.array([81.94, 80.56, 81.94, 86.11])

delta_fpr_fair_excl = np.array([2.03, 2.03, 0.41, 2.98])
delta_tpr_fair_excl = np.array([14.19, 0.97, 9.03, 0.65])

# =========================
# Colors
# =========================
strategy_colors = {
    "Baseline": "#d9e3d0",
    "Best accuracy": "#9cc9a3",
    "Best fair": "#4b9ec4",
}


# =========================
# Helper plotting function
# =========================
def plot_metric_three_variants(
    ax,
    baseline_vals,
    best_vals,
    fair_vals,
    ylabel,
    title,
    ylim=None,
    show_xticklabels=True,
):
    width = 0.23
    off1 = x - width
    off2 = x
    off3 = x + width

    bars_b = ax.bar(
        off1,
        baseline_vals,
        width,
        color=strategy_colors["Baseline"],
        edgecolor="black",
        label="Baseline",
    )
    bars_o = ax.bar(
        off2,
        best_vals,
        width,
        color=strategy_colors["Best accuracy"],
        edgecolor="black",
        label="Best accuracy",
    )
    bars_f = ax.bar(
        off3,
        fair_vals,
        width,
        color=strategy_colors["Best fair"],
        edgecolor="black",
        label="Best fair",
    )

    label_offset = 1 if ylim is None else max((ylim[1] - ylim[0]) * 0.015, 0.5)

    for bars in (bars_b, bars_o, bars_f):
        for rect in bars:
            h = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                h + label_offset,
                format_val(h),
                ha="center",
                va="bottom",
                fontsize=8,
            )

    ax.set_title(title, fontsize=12)
    ax.set_ylabel(ylabel)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_xticks(x)
    if show_xticklabels:
        ax.set_xticklabels(models, fontsize=10)
    else:
        ax.set_xticklabels([])


# =========================
# Shared legend handles
# =========================
handles_variants = [
    Rectangle(
        (0, 0),
        1,
        1,
        facecolor=strategy_colors["Baseline"],
        edgecolor="black",
    ),
    Rectangle(
        (0, 0),
        1,
        1,
        facecolor=strategy_colors["Best accuracy"],
        edgecolor="black",
    ),
    Rectangle(
        (0, 0),
        1,
        1,
        facecolor=strategy_colors["Best fair"],
        edgecolor="black",
    ),
]
labels_variants = ["Baseline", "Best accuracy", "Best fair"]

# =========================
# Figure 6: including misgendering
# =========================
fig6, axes6 = plt.subplots(3, 2, figsize=(14, 14))
axes6 = axes6.flatten()

plot_metric_three_variants(
    axes6[0],
    acc_overall_baseline,
    acc_overall_best,
    acc_overall_fair,
    "Accuracy (%)",
    "Overall accuracy including misgendering",
    ylim=(0, 100),
    show_xticklabels=False,
)

plot_metric_three_variants(
    axes6[1],
    delta_fpr_baseline,
    delta_fpr_best,
    delta_fpr_fair,
    "Gap (pp)",
    "ΔFPR including misgendering",
    ylim=(0, 80),
    show_xticklabels=False,
)

plot_metric_three_variants(
    axes6[2],
    acc_gep0_baseline,
    acc_gep0_best,
    acc_gep0_fair,
    "Accuracy (%)",
    "NGEP (GEP=0) accuracy including misgendering",
    ylim=(0, 100),
    show_xticklabels=False,
)

plot_metric_three_variants(
    axes6[3],
    delta_tpr_baseline,
    delta_tpr_best,
    delta_tpr_fair,
    "Gap (pp)",
    "ΔTPR including misgendering",
    ylim=(0, 60),
    show_xticklabels=True,
)

plot_metric_three_variants(
    axes6[4],
    acc_gep1_baseline,
    acc_gep1_best,
    acc_gep1_fair,
    "Accuracy (%)",
    "GEP (GEP=1) accuracy including misgendering",
    ylim=(0, 100),
    show_xticklabels=True,
)

axes6[5].axis("off")
axes6[5].legend(
    handles_variants,
    labels_variants,
    loc="center",
    frameon=True,
    fontsize=12,
    ncol=1,
)

fig6.tight_layout(rect=[0.02, 0.05, 0.98, 0.98])
png_dpi_6 = min(600, MAX_PNG_DIMENSION / max(fig6.get_size_inches()))
fig6.savefig(
    os.path.join(
        save_dir,
        "Accuracy and subgroup fairness under baseline and threshold-optimized configurations including misgendering.png",
    ),
    dpi=png_dpi_6,
    bbox_inches=None,
    pad_inches=0,
    facecolor="white",
    transparent=False,
)
fig6.savefig(
    os.path.join(
        save_dir,
        "Accuracy and subgroup fairness under baseline and threshold-optimized configurations including misgendering.eps",
    ),
    format="eps",
    bbox_inches="tight",
    transparent=False,
)

# =========================
# Figure 7: excluding misgendering
# =========================
fig7, axes7 = plt.subplots(3, 2, figsize=(14, 14))
axes7 = axes7.flatten()

plot_metric_three_variants(
    axes7[0],
    acc_overall_baseline_excl,
    acc_overall_best_excl,
    acc_overall_fair_excl,
    "Accuracy (%)",
    "Overall accuracy excluding misgendering",
    ylim=(0, 100),
    show_xticklabels=False,
)

plot_metric_three_variants(
    axes7[1],
    delta_fpr_baseline_excl,
    delta_fpr_best_excl,
    delta_fpr_fair_excl,
    "Gap (pp)",
    "ΔFPR excluding misgendering",
    ylim=(0, 80),
    show_xticklabels=False,
)

plot_metric_three_variants(
    axes7[2],
    acc_gep0_baseline_excl,
    acc_gep0_best_excl,
    acc_gep0_fair_excl,
    "Accuracy (%)",
    "NGEP (GEP=0) accuracy excluding misgendering",
    ylim=(0, 100),
    show_xticklabels=False,
)

plot_metric_three_variants(
    axes7[3],
    delta_tpr_baseline_excl,
    delta_tpr_best_excl,
    delta_tpr_fair_excl,
    "Gap (pp)",
    "ΔTPR excluding misgendering",
    ylim=(0, 60),
    show_xticklabels=True,
)

plot_metric_three_variants(
    axes7[4],
    acc_gep1_baseline_excl,
    acc_gep1_best_excl,
    acc_gep1_fair_excl,
    "Accuracy (%)",
    "GEP (GEP=1) accuracy excluding misgendering",
    ylim=(0, 100),
    show_xticklabels=True,
)

axes7[5].axis("off")
axes7[5].legend(
    handles_variants,
    labels_variants,
    loc="center",
    frameon=True,
    fontsize=12,
    ncol=1,
)

fig7.tight_layout(rect=[0.02, 0.05, 0.98, 0.98])
png_dpi_7 = min(600, MAX_PNG_DIMENSION / max(fig7.get_size_inches()))
fig7.savefig(
    os.path.join(
        save_dir,
        "Accuracy and subgroup fairness under baseline and threshold-optimized configurations excluding misgendering.png",
    ),
    dpi=png_dpi_7,
    bbox_inches=None,
    pad_inches=0,
    facecolor="white",
    transparent=False,
)
fig7.savefig(
    os.path.join(
        save_dir,
        "Accuracy and subgroup fairness under baseline and threshold-optimized configurations excluding misgendering.eps",
    ),
    format="eps",
    bbox_inches="tight",
    transparent=False,
)

plt.show()
print("Saved Figures 6 and 7 to:", save_dir)
