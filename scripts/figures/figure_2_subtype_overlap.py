# ======================================================================
# FIGURE: STIGMA SUBTYPE OVERLAP VENN-STYLE SUMMARY
# Compact 2+1 layout
# Use this AFTER df has already been created.
# ======================================================================

from pathlib import Path
import os
import re
import textwrap

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle


# ======================================================================
# OUTPUT PATHS — file names unchanged
# ======================================================================

OUTPUT_DIR = Path(os.environ.get("GEP_FIGURES_DIR", Path.cwd() / "figures"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PNG = OUTPUT_DIR / "stigma_subtype_overlap_venn_summary.png"
OUTPUT_PDF = OUTPUT_DIR / "stigma_subtype_overlap_venn_summary.pdf"
OUTPUT_XLSX = OUTPUT_DIR / "stigma_subtype_overlap_venn_counts.xlsx"

MAX_PNG_DIMENSION = 1200

# Article-standard figure display labels.
PANEL_LABEL_COLOR = "#1F4E79"
CREDIBILITY_DISPLAY_LABEL = "Credibility and obstinacy"


# ======================================================================
# COLUMN FINDING
# ======================================================================

def normalize_colname(x):
    return re.sub(r"[^a-z0-9]+", "", str(x).lower())


def find_col(dataframe, candidates, required=True):
    normalized_lookup = {
        normalize_colname(col): col for col in dataframe.columns
    }

    for cand in candidates:
        key = normalize_colname(cand)
        if key in normalized_lookup:
            return normalized_lookup[key]

    if required:
        raise ValueError(
            f"Could not find any column matching: {candidates}\n"
            f"Available columns:\n{list(dataframe.columns)}"
        )

    return None


# ======================================================================
# LOAD INPUT DATA IF df IS NOT ALREADY DEFINED
# ======================================================================

DATA_DIR = Path(os.environ.get("GEP_DATA_DIR", Path.cwd() / "data"))


def load_figure2_dataframe(data_dir):
    required_column_groups = [
        ["GEP"],
        ["label", "stigma_label", "stigmatizing_label"],
        [
            "label_exclude_misgendering",
            "label excluding misgendering",
            "label_excluding_misgendering",
            "stigma_exclude_misgendering",
            "stigma excluding misgendering",
        ],
        ["Compliance", "compliance"],
        ["Descriptors", "Descriptor", "descriptors", "descriptor"],
        [
            "Descriptors_exclude_misgendering",
            "Descriptors excluding misgendering",
            "Descriptors_excluding_misgendering",
            "Descriptor_exclude_misgendering",
            "Descriptor excluding misgendering",
        ],
        [
            # Legacy internal files used "Obstinance"; the public release uses
            # the article terminology, "Obstinacy."
            "Credibility and Obstinance",
            "Credibility & Obstinance",
            "Credibility and Obstinacy",
            "Credibility & Obstinacy",
            "Credibility_Obstinance",
            "Credibility_Obstinacy",
        ],
        ["Misgendering", "misgendering"],
    ]

    matching_files = []
    for csv_path in sorted(data_dir.glob("*.csv")):
        try:
            columns = pd.read_csv(csv_path, nrows=0).columns
        except Exception:
            continue

        normalized_columns = {normalize_colname(col) for col in columns}
        has_all_required_columns = all(
            any(
                normalize_colname(candidate) in normalized_columns
                for candidate in candidate_group
            )
            for candidate_group in required_column_groups
        )
        if has_all_required_columns:
            matching_files.append(csv_path)

    if not matching_files:
        raise FileNotFoundError(
            "Could not find a CSV containing all Figure 2 columns in "
            f"{data_dir}. Confirm that the annotated note-level CSV is "
            "stored in this folder."
        )

    if len(matching_files) > 1:
        file_list = "\n".join(str(path) for path in matching_files)
        raise RuntimeError(
            "More than one CSV contains the required Figure 2 columns. "
            "Please retain only the intended input in the DATA folder or "
            f"set df manually before running this script:\n{file_list}"
        )

    input_csv = matching_files[0]
    print(f"Loading Figure 2 data from: {input_csv}")
    return pd.read_csv(input_csv)


if "df" not in globals():
    df = load_figure2_dataframe(DATA_DIR)


COL_GEP = find_col(df, ["GEP"])

COL_LABEL = find_col(
    df,
    ["label", "stigma_label", "stigmatizing_label"],
)

COL_LABEL_EXCL = find_col(
    df,
    [
        "label_exclude_misgendering",
        "label excluding misgendering",
        "label_excluding_misgendering",
        "stigma_exclude_misgendering",
        "stigma excluding misgendering",
    ],
)

COL_COMPLIANCE = find_col(df, ["Compliance", "compliance"])

COL_DESCRIPTOR = find_col(
    df,
    ["Descriptors", "Descriptor", "descriptors", "descriptor"],
)

COL_DESCRIPTOR_EXCL = find_col(
    df,
    [
        "Descriptors_exclude_misgendering",
        "Descriptors excluding misgendering",
        "Descriptors_excluding_misgendering",
        "Descriptor_exclude_misgendering",
        "Descriptor excluding misgendering",
    ],
)

COL_CREDIBILITY = find_col(
    df,
    [
        "Credibility and Obstinance",
        "Credibility & Obstinance",
        "Credibility and Obstinacy",
        "Credibility & Obstinacy",
        "Credibility_Obstinance",
        "Credibility_Obstinacy",
    ],
)

COL_MISGENDERING = find_col(df, ["Misgendering", "misgendering"])


# ======================================================================
# CLEAN BINARY COLUMNS
# ======================================================================

binary_cols = [
    COL_GEP,
    COL_LABEL,
    COL_LABEL_EXCL,
    COL_COMPLIANCE,
    COL_DESCRIPTOR,
    COL_DESCRIPTOR_EXCL,
    COL_CREDIBILITY,
    COL_MISGENDERING,
]

for col in binary_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)


# ======================================================================
# BASIC MASKS
# ======================================================================

is_gep = df[COL_GEP] == 1
is_ngep = df[COL_GEP] == 0

df_gep = df.loc[is_gep].copy()
df_ngep = df.loc[is_ngep].copy()

n_total = len(df)
n_gep = len(df_gep)
n_ngep = len(df_ngep)

if n_total == 0:
    raise ValueError("df has zero rows.")

if n_gep == 0:
    raise ValueError("No GEP rows found.")

if n_ngep == 0:
    raise ValueError("No NGEP rows found.")


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================

def pct(count, denominator):
    if denominator == 0:
        return 0.0
    return round(100 * int(count) / int(denominator), 2)


def count_mask(mask):
    return int(mask.sum())


def compute_venn_regions(data, descriptor_col):
    """
    C = Compliance
    D = Descriptor
    R = Credibility & Obstinacy
    """
    C = data[COL_COMPLIANCE].astype(bool)
    D = data[descriptor_col].astype(bool)
    R = data[COL_CREDIBILITY].astype(bool)

    regions = {
        "Only Compliance": count_mask(C & ~D & ~R),
        "Only Descriptor": count_mask(~C & D & ~R),
        "Only Credibility & Obstinacy": count_mask(~C & ~D & R),
        "Compliance + Descriptor only": count_mask(C & D & ~R),
        "Compliance + Credibility only": count_mask(C & ~D & R),
        "Descriptor + Credibility only": count_mask(~C & D & R),
        "All three": count_mask(C & D & R),
    }

    regions["Union"] = sum(regions.values())

    totals = {
        "Compliance total": count_mask(C),
        "Descriptor total": count_mask(D),
        "Credibility & Obstinacy total": count_mask(R),
        "Compliance ∩ Descriptor total": count_mask(C & D),
        "Compliance ∩ Credibility total": count_mask(C & R),
        "Descriptor ∩ Credibility total": count_mask(D & R),
    }

    return regions, totals


def build_panel(
    panel_label,
    title,
    group_label,
    data,
    denominator,
    label_col,
    descriptor_col,
    descriptor_legend_label,
    descriptor_circle_label,
    note,
):
    regions, totals = compute_venn_regions(data, descriptor_col)
    label_count = int(data[label_col].sum())
    label_percent = pct(label_count, denominator)

    return {
        "panel_label": panel_label,
        "title": title,
        "group_label": group_label,
        "data": data,
        "denominator": denominator,
        "label_col": label_col,
        "descriptor_col": descriptor_col,
        "descriptor_legend_label": descriptor_legend_label,
        "descriptor_circle_label": descriptor_circle_label,
        "note": note,
        "regions": regions,
        "totals": totals,
        "label_count": label_count,
        "label_percent": label_percent,
        "union_count": regions["Union"],
        "union_matches_label": regions["Union"] == label_count,
    }


# ======================================================================
# BUILD PANELS
# ======================================================================

gep_with_panel = build_panel(
    panel_label="A",
    title="GEP (including misgendering)",
    group_label="GEP",
    data=df_gep,
    denominator=n_gep,
    label_col=COL_LABEL,
    descriptor_col=COL_DESCRIPTOR,
    descriptor_legend_label="Descriptor (including misgendering)",
    descriptor_circle_label="Descriptor",
    note=(
        "Includes misgendering within the descriptor subtype. "
        "Dashed box represents the union of compliance, descriptor, "
        "and credibility and obstinacy."
    ),
)

gep_without_panel = build_panel(
    panel_label="B",
    title="GEP (excluding misgendering)",
    group_label="GEP",
    data=df_gep,
    denominator=n_gep,
    label_col=COL_LABEL_EXCL,
    descriptor_col=COL_DESCRIPTOR_EXCL,
    descriptor_legend_label="Descriptor (excluding misgendering)",
    descriptor_circle_label="Descriptor",
    note=(
        "Misgendering is removed from the descriptor subtype, but notes with genuine "
        "non-misgendering descriptors are retained even when they co-occur "
        "with misgendering."
    ),
)

ngep_panel = build_panel(
    panel_label="C",
    title="NGEP",
    group_label="NGEP",
    data=df_ngep,
    denominator=n_ngep,
    label_col=COL_LABEL,
    descriptor_col=COL_DESCRIPTOR,
    descriptor_legend_label="Descriptor",
    descriptor_circle_label="Descriptor",
    note=(
        "No misgendering subtype is applied to NGEP notes. "
        "Dashed box represents the union of compliance, descriptor, "
        "and credibility and obstinacy."
    ),
)

panels = [gep_with_panel, gep_without_panel, ngep_panel]


# ======================================================================
# SUMMARY TABLE
# ======================================================================

summary_rows = []


def add_summary_row(metric, count, percent_value):
    summary_rows.append(
        {
            "Metric": metric,
            "Count": int(count),
            "Percent Stigma (%)": round(float(percent_value), 2),
        }
    )


add_summary_row("Total notes", n_total, pct(df[COL_LABEL].sum(), n_total))
add_summary_row("Stigmatized notes (including misgendering)", df[COL_LABEL].sum(), 100.00)
add_summary_row("Stigmatized notes (excluding misgendering)", df[COL_LABEL_EXCL].sum(), 100.00)
add_summary_row("Non-stigmatized notes", (df[COL_LABEL] == 0).sum(), 0.00)

add_summary_row("GEP notes", n_gep, pct((df_gep[COL_LABEL] == 1).sum(), n_gep))
add_summary_row("NGEP notes", n_ngep, pct((df_ngep[COL_LABEL] == 1).sum(), n_ngep))

add_summary_row(
    "GEP notes: stigmatized excluding misgendering",
    (df_gep[COL_LABEL_EXCL] == 1).sum(),
    pct((df_gep[COL_LABEL_EXCL] == 1).sum(), n_gep),
)

add_summary_row(
    "NGEP notes: stigmatized excluding misgendering",
    (df_ngep[COL_LABEL_EXCL] == 1).sum(),
    pct((df_ngep[COL_LABEL_EXCL] == 1).sum(), n_ngep),
)

add_summary_row(
    "Descriptors: GEP (including misgendering)",
    (df_gep[COL_DESCRIPTOR] == 1).sum(),
    pct((df_gep[COL_DESCRIPTOR] == 1).sum(), n_gep),
)

add_summary_row(
    "Descriptors: GEP (excluding misgendering subtype)",
    (df_gep[COL_DESCRIPTOR_EXCL] == 1).sum(),
    pct((df_gep[COL_DESCRIPTOR_EXCL] == 1).sum(), n_gep),
)

add_summary_row(
    "Descriptors: NGEP",
    (df_ngep[COL_DESCRIPTOR] == 1).sum(),
    pct((df_ngep[COL_DESCRIPTOR] == 1).sum(), n_ngep),
)

add_summary_row(
    "Compliance: GEP",
    (df_gep[COL_COMPLIANCE] == 1).sum(),
    pct((df_gep[COL_COMPLIANCE] == 1).sum(), n_gep),
)

add_summary_row(
    "Compliance: NGEP",
    (df_ngep[COL_COMPLIANCE] == 1).sum(),
    pct((df_ngep[COL_COMPLIANCE] == 1).sum(), n_ngep),
)

add_summary_row(
    "Credibility & Obstinacy: GEP",
    (df_gep[COL_CREDIBILITY] == 1).sum(),
    pct((df_gep[COL_CREDIBILITY] == 1).sum(), n_gep),
)

add_summary_row(
    "Credibility & Obstinacy: NGEP",
    (df_ngep[COL_CREDIBILITY] == 1).sum(),
    pct((df_ngep[COL_CREDIBILITY] == 1).sum(), n_ngep),
)

add_summary_row(
    "Misgendering (GEP only)",
    (df_gep[COL_MISGENDERING] == 1).sum(),
    pct((df_gep[COL_MISGENDERING] == 1).sum(), n_gep),
)

summary_df = pd.DataFrame(summary_rows)


# ======================================================================
# VENN REGION TABLE
# ======================================================================

region_rows = []

for panel in panels:
    denom = panel["denominator"]

    for region_name, count in panel["regions"].items():
        region_rows.append(
            {
                "Panel": panel["title"],
                "Metric": region_name,
                "Count": int(count),
                "Percent Stigma (%)": pct(count, denom),
                "Denominator": denom,
            }
        )

    for total_name, count in panel["totals"].items():
        region_rows.append(
            {
                "Panel": panel["title"],
                "Metric": total_name,
                "Count": int(count),
                "Percent Stigma (%)": pct(count, denom),
                "Denominator": denom,
            }
        )

    region_rows.append(
        {
            "Panel": panel["title"],
            "Metric": "Stigmatized note-level outcome",
            "Count": panel["label_count"],
            "Percent Stigma (%)": panel["label_percent"],
            "Denominator": denom,
        }
    )

region_df = pd.DataFrame(region_rows)


# ======================================================================
# GEP MISGENDERING OVERLAP TABLE
# ======================================================================

gep_mis = df_gep[COL_MISGENDERING].astype(bool)
gep_desc_excl = df_gep[COL_DESCRIPTOR_EXCL].astype(bool)

gep_overlap_rows = []


def add_gep_overlap(metric, mask):
    count = int(mask.sum())
    gep_overlap_rows.append(
        {
            "Metric": metric,
            "Count": count,
            "Percent Stigma (%)": pct(count, n_gep),
            "Denominator": n_gep,
        }
    )


add_gep_overlap("Non-misgendering descriptor only", gep_desc_excl & ~gep_mis)
add_gep_overlap("Misgendering + non-misgendering descriptor", gep_desc_excl & gep_mis)
add_gep_overlap("Misgendering only / no non-misgendering descriptor", ~gep_desc_excl & gep_mis)
add_gep_overlap("Neither misgendering nor non-misgendering descriptor", ~gep_desc_excl & ~gep_mis)

gep_overlap_df = pd.DataFrame(gep_overlap_rows)


# ======================================================================
# CONSISTENCY CHECKS
# ======================================================================

check_rows = []

gep_descriptor_union = (
    df_gep[COL_DESCRIPTOR].astype(bool)
    == (
        df_gep[COL_DESCRIPTOR_EXCL].astype(bool)
        | df_gep[COL_MISGENDERING].astype(bool)
    )
)

check_rows.append(
    {
        "Check": "GEP Descriptors == Descriptors_exclude_misgendering OR Misgendering",
        "Mismatch Count": int((~gep_descriptor_union).sum()),
    }
)

label_union = (
    df[COL_LABEL].astype(bool)
    == (
        df[COL_COMPLIANCE].astype(bool)
        | df[COL_DESCRIPTOR].astype(bool)
        | df[COL_CREDIBILITY].astype(bool)
    )
)

check_rows.append(
    {
        "Check": "label == Compliance OR Descriptors OR Credibility & Obstinacy",
        "Mismatch Count": int((~label_union).sum()),
    }
)

label_excl_union = (
    df[COL_LABEL_EXCL].astype(bool)
    == (
        df[COL_COMPLIANCE].astype(bool)
        | df[COL_DESCRIPTOR_EXCL].astype(bool)
        | df[COL_CREDIBILITY].astype(bool)
    )
)

check_rows.append(
    {
        "Check": "label_exclude_misgendering == Compliance OR Descriptors_exclude_misgendering OR Credibility & Obstinacy",
        "Mismatch Count": int((~label_excl_union).sum()),
    }
)

for panel in panels:
    check_rows.append(
        {
            "Check": f"{panel['title']}: Venn subtype union equals note-level outcome",
            "Mismatch Count": 0 if panel["union_matches_label"] else 1,
        }
    )

checks_df = pd.DataFrame(check_rows)


# ======================================================================
# PLOT FUNCTION — COMPACT TRUE-CIRCLE VENN
# ======================================================================

def draw_panel(ax, panel):
    r = panel["regions"]
    t = panel["totals"]
    denom = panel["denominator"]

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 15)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    compliance_color = "#D84B7A"
    descriptor_color = "#746CE8"
    credibility_color = "#009B75"
    grey_text = "#666666"

    card = FancyBboxPatch(
        (0.25, 0.25),
        11.5,
        14.45,
        boxstyle="round,pad=0.02,rounding_size=0.45",
        linewidth=1.1,
        edgecolor="#B7B7B7",
        facecolor="white",
    )
    ax.add_patch(card)

    ax.text(
        0.90,
        14.20,
        panel["panel_label"],
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=PANEL_LABEL_COLOR,
        bbox={
            "boxstyle": "round,pad=0.22",
            "facecolor": "#EAF2F8",
            "edgecolor": PANEL_LABEL_COLOR,
            "linewidth": 1.1,
        },
    )

    ax.text(
        6.0,
        14.25,
        panel["title"],
        ha="center",
        va="center",
        fontsize=12.8,
        fontweight="bold",
        color="#111111",
    )

    ax.text(
        6.0,
        13.75,
        f"{panel['label_count']} stigmatized {panel['group_label']} notes "
        f"({panel['label_percent']:.2f}%)",
        ha="center",
        va="center",
        fontsize=9.5,
        color=grey_text,
    )

    dashed = Rectangle(
        (0.75, 5.0),
        10.5,
        7.4,
        linewidth=1.05,
        edgecolor=descriptor_color,
        facecolor="none",
        linestyle=(0, (4, 3)),
    )
    ax.add_patch(dashed)

    radius = 2.20

    compliance_center = (4.25, 9.60)
    descriptor_center = (7.75, 9.60)
    credibility_center = (6.00, 7.35)

    for center, color in [
        (compliance_center, compliance_color),
        (descriptor_center, descriptor_color),
        (credibility_center, credibility_color),
    ]:
        ax.add_patch(
            Circle(
                center,
                radius,
                facecolor=color,
                edgecolor=color,
                alpha=0.12,
                linewidth=1.2,
            )
        )
        ax.add_patch(
            Circle(
                center,
                radius,
                facecolor="none",
                edgecolor=color,
                linewidth=1.2,
            )
        )

    ax.text(
        1.95,
        11.25,
        f"Compliance\nn={t['Compliance total']}, "
        f"{pct(t['Compliance total'], denom):.2f}%",
        ha="center",
        va="center",
        fontsize=7.8,
        color=compliance_color,
        fontweight="bold",
    )

    ax.text(
        10.05,
        11.25,
        f"{panel['descriptor_circle_label']}\n"
        f"n={t['Descriptor total']}, "
        f"{pct(t['Descriptor total'], denom):.2f}%",
        ha="center",
        va="center",
        fontsize=7.8,
        color=descriptor_color,
        fontweight="bold",
    )

    ax.text(
        6.0,
        5.85,
        f"{CREDIBILITY_DISPLAY_LABEL}\n"
        f"n={t['Credibility & Obstinacy total']}, "
        f"{pct(t['Credibility & Obstinacy total'], denom):.2f}%",
        ha="center",
        va="center",
        fontsize=7.2,
        color=credibility_color,
        fontweight="bold",
    )

    region_style = {
        "ha": "center",
        "va": "center",
        "fontsize": 9.4,
        "fontweight": "bold",
    }

    ax.text(3.10, 9.65, r["Only Compliance"], color="#7C1F3F", **region_style)
    ax.text(8.90, 9.65, r["Only Descriptor"], color="#2D2786", **region_style)
    ax.text(6.00, 6.85, r["Only Credibility & Obstinacy"], color="#00614B", **region_style)

    ax.text(6.00, 9.82, r["Compliance + Descriptor only"], color="#4438B5", **region_style)
    ax.text(4.60, 7.85, r["Compliance + Credibility only"], color="#7C1F3F", **region_style)
    ax.text(7.40, 7.85, r["Descriptor + Credibility only"], color="#2D2786", **region_style)
    ax.text(6.00, 8.45, r["All three"], color="#101052", **region_style)

    legend_items = [
        (
            compliance_color,
            f"Compliance {t['Compliance total']} "
            f"({pct(t['Compliance total'], denom):.2f}%)",
        ),
        (
            descriptor_color,
            f"{panel['descriptor_legend_label']} {t['Descriptor total']} "
            f"({pct(t['Descriptor total'], denom):.2f}%)",
        ),
        (
            credibility_color,
            f"{CREDIBILITY_DISPLAY_LABEL} {t['Credibility & Obstinacy total']} "
            f"({pct(t['Credibility & Obstinacy total'], denom):.2f}%)",
        ),
    ]

    legend_y = 4.35
    line_gap = 0.34

    for i, (color, text) in enumerate(legend_items):
        y = legend_y - i * line_gap
        ax.scatter(1.05, y, s=65, color=color)
        ax.text(
            1.42,
            y,
            text,
            ha="left",
            va="center",
            fontsize=7.2,
            color="#444444",
        )

    footnote = (
        f"Union={r['Union']} "
        f"({pct(r['Union'], denom):.2f}%). "
        f"Overlaps: C∩D={t['Compliance ∩ Descriptor total']}, "
        f"C∩Cr={t['Compliance ∩ Credibility total']}, "
        f"D∩Cr={t['Descriptor ∩ Credibility total']}, "
        f"all three={r['All three']}. "
        f"{panel['note']}"
    )

    if not panel["union_matches_label"]:
        footnote += (
            f" WARNING: subtype union ({panel['union_count']}) "
            f"does not equal note-level label count ({panel['label_count']})."
        )

    wrapped_footnote = textwrap.fill(footnote, width=60)

    ax.text(
        0.85,
        1.5,
        wrapped_footnote,
        ha="left",
        va="bottom",
        fontsize=7.4,
        color=grey_text,
        linespacing=1.15,
    )


# ======================================================================
# GENERATE FIGURE — COMPACT 2+1 LAYOUT
# ======================================================================

fig = plt.figure(figsize=(14, 13), dpi=300)

# [left, bottom, width, height]
ax1 = fig.add_axes([0.13, 0.53, 0.40, 0.43])
ax2 = fig.add_axes([0.47, 0.53, 0.40, 0.43])
ax3 = fig.add_axes([0.30, 0.10, 0.40, 0.43])

axes = [ax1, ax2, ax3]

for ax, panel in zip(axes, panels):
    draw_panel(ax, panel)

# Keep the original 14 x 13 inch layout and adjust only the PNG export
# resolution so that neither side exceeds JMIR's 1200-pixel limit.
png_dpi = min(300, MAX_PNG_DIMENSION / max(fig.get_size_inches()))
fig.savefig(OUTPUT_PNG, dpi=png_dpi, bbox_inches=None, pad_inches=0)
fig.savefig(OUTPUT_PDF, bbox_inches="tight")
plt.show()


# ======================================================================
# SAVE TABLES
# ======================================================================

with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="Table2_Summary", index=False)
    region_df.to_excel(writer, sheet_name="Venn_Regions", index=False)
    gep_overlap_df.to_excel(writer, sheet_name="GEP_Misgendering_Overlap", index=False)
    checks_df.to_excel(writer, sheet_name="Consistency_Checks", index=False)


# ======================================================================
# PRINT OUTPUTS
# ======================================================================

print("\n=== Manuscript-style Table 2 summary ===")
print(summary_df.to_string(index=False))

print("\n=== Venn region counts ===")
print(region_df.to_string(index=False))

print("\n=== GEP misgendering / non-misgendering descriptor overlap ===")
print(gep_overlap_df.to_string(index=False))

print("\n=== Consistency checks ===")
print(checks_df.to_string(index=False))

print("\nSaved files:")
print(f"PNG:  {OUTPUT_PNG}")
print(f"PDF:  {OUTPUT_PDF}")
print(f"XLSX: {OUTPUT_XLSX}")
