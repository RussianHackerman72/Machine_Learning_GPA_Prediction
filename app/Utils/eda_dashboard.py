"""
Utils/eda_dashboard.py
Generates all EDA artefacts (figures + summary stats) for the GradeOwl
dashboard.  Every function returns a matplotlib Figure so Streamlit can
render it with st.pyplot() without touching the filesystem.
"""

from __future__ import annotations

import pickle
from io import BytesIO
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PALETTE  (matches the app's ocean gradient)
# ─────────────────────────────────────────────────────────────────────────────
C = {
    "bg":        "#0a1628",
    "card":      "#0d2244",
    "border":    "#1e3a5f",
    "blue1":     "#2196f3",
    "blue2":     "#1565c0",
    "teal":      "#34d399",
    "amber":     "#fbbf24",
    "rose":      "#f87171",
    "violet":    "#a78bfa",
    "sky":       "#93c5fd",
    "text":      "#e2e8f0",
    "muted":     "#64748b",
    "seq_start": "#0d2244",
    "seq_end":   "#60a5fa",
}

NUMERIC_FEATURES = [
    "Hours_Studied",
    "Sleep_Hours",
    "Stress_Level",
    "Screen_Time",
    "Attendance",
    "Previous_GPA",
    "Tutoring_Sessions_Per_Week",
    "Exam_Anxiety_Score",
    "Age",
]

CATEGORICAL_FEATURES = [
    "Gender",
    "Part_Time_Job",
    "Study_Method",
    "Diet_Quality",
    "Internet_Quality",
    "Extracurricular",
    "Family_Income_Level",
]

# Common names the target column might have across Kaggle datasets
TARGET_CANDIDATES = ["Exam_Score", "Final_Score", "Score", "exam_score", "final_score", "score"]

# Common dataset paths
DATASET_CANDIDATES = [
    "data/student_data.csv",
    "data/students.csv",
    "data/dataset.csv",
    "data/student_performance.csv",
    "data/StudentPerformanceFactors.csv",
    "data/student-performance.csv",
    "student_data.csv",
    "dataset.csv",
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _apply_theme(fig: plt.Figure, axes=None) -> None:
    """Apply dark ocean theme to a figure and its axes."""
    fig.patch.set_facecolor(C["bg"])
    if axes is None:
        axes = fig.get_axes()
    if not hasattr(axes, "__iter__"):
        axes = [axes]
    for ax in axes:
        ax.set_facecolor(C["card"])
        ax.tick_params(colors=C["muted"], labelsize=8)
        ax.xaxis.label.set_color(C["text"])
        ax.yaxis.label.set_color(C["text"])
        ax.title.set_color(C["text"])
        for spine in ax.spines.values():
            spine.set_edgecolor(C["border"])
        ax.grid(color=C["border"], linewidth=0.4, linestyle="--", alpha=0.6)
        ax.grid(axis="x", visible=False)


def _gradient_palette(n: int) -> list[str]:
    """Return n colours interpolated between blue2 → sky."""
    cmap = plt.cm.Blues
    return [
        "#{:02x}{:02x}{:02x}".format(*[int(v * 255) for v in cmap(0.35 + 0.55 * i / max(n - 1, 1))[:3]])
        for i in range(n)
    ]


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_dataset(custom_path: Optional[str] = None) -> tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Try to load the training dataset.
    Returns (dataframe, target_column) or (None, None) if not found.
    """
    candidates = ([custom_path] if custom_path else []) + DATASET_CANDIDATES

    for path in candidates:
        try:
            df = pd.read_csv(path)
            # detect target column
            for col in TARGET_CANDIDATES:
                if col in df.columns:
                    return df, col
            # fallback: last numeric column
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                return df, numeric_cols[-1]
        except (FileNotFoundError, Exception):
            continue
    return None, None


@st.cache_resource(show_spinner=False)
def load_model():
    """Load the trained XGBoost model."""
    try:
        with open("models/best_xgboost_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("models/model_features.pkl", "rb") as f:
            features = pickle.load(f)
        return model, features
    except Exception:
        return None, None


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY STATS
# ─────────────────────────────────────────────────────────────────────────────

def get_summary(df: pd.DataFrame, target: str) -> dict:
    """Return lightweight summary dict for metric cards."""
    num_df = df.select_dtypes(include="number")
    return {
        "n_rows":      len(df),
        "n_cols":      len(df.columns),
        "n_numeric":   len(num_df.columns),
        "n_missing":   int(df.isnull().sum().sum()),
        "target_mean": round(float(df[target].mean()), 2),
        "target_std":  round(float(df[target].std()), 2),
        "target_min":  round(float(df[target].min()), 2),
        "target_max":  round(float(df[target].max()), 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHART 1 — Target Distribution
# ─────────────────────────────────────────────────────────────────────────────

def fig_target_distribution(df: pd.DataFrame, target: str) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    scores = df[target].dropna()

    # Histogram + KDE
    ax1 = axes[0]
    ax1.hist(scores, bins=30, color=C["blue1"], alpha=0.75, edgecolor=C["bg"], linewidth=0.4)
    ax2_twin = ax1.twinx()
    kde_x = np.linspace(scores.min(), scores.max(), 300)
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(scores)
    ax2_twin.plot(kde_x, kde(kde_x), color=C["teal"], linewidth=2)
    ax2_twin.set_yticks([])
    ax2_twin.set_facecolor(C["card"])
    for spine in ax2_twin.spines.values():
        spine.set_edgecolor(C["border"])
    ax1.set_xlabel("Score")
    ax1.set_ylabel("Count")
    ax1.set_title("Score Distribution")

    # Box plot
    ax2 = axes[1]
    bp = ax2.boxplot(
        scores,
        vert=True,
        patch_artist=True,
        widths=0.45,
        medianprops=dict(color=C["teal"], linewidth=2),
        boxprops=dict(facecolor=C["blue2"], color=C["sky"], linewidth=1.2),
        whiskerprops=dict(color=C["sky"], linewidth=1),
        capprops=dict(color=C["sky"], linewidth=1.5),
        flierprops=dict(marker="o", color=C["rose"], markersize=3, alpha=0.5),
    )
    ax2.set_xticks([1])
    ax2.set_xticklabels(["Score"])
    ax2.set_ylabel("Score")
    ax2.set_title("Score Box-Plot")

    _apply_theme(fig, axes)
    fig.tight_layout(pad=1.5)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART 2 — Numeric Feature Distributions
# ─────────────────────────────────────────────────────────────────────────────

def fig_numeric_distributions(df: pd.DataFrame) -> plt.Figure:
    cols = [c for c in NUMERIC_FEATURES if c in df.columns]
    n = len(cols)
    ncols = 3
    nrows = (n + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=(12, nrows * 2.8))
    axes_flat = axes.flatten() if n > 1 else [axes]
    palette = _gradient_palette(n)

    for i, col in enumerate(cols):
        ax = axes_flat[i]
        data = df[col].dropna()
        ax.hist(data, bins=25, color=palette[i], alpha=0.8, edgecolor=C["bg"], linewidth=0.3)
        ax.set_title(col.replace("_", " "), fontsize=9, pad=4)
        ax.set_xlabel("")
        ax.yaxis.set_major_locator(mticker.MaxNLocator(4))

    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].set_visible(False)

    _apply_theme(fig, [ax for ax in axes_flat if ax.get_visible()])
    fig.suptitle("Numeric Feature Distributions", color=C["text"], fontsize=12, y=1.01)
    fig.tight_layout(pad=1.2)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART 3 — Correlation Heatmap
# ─────────────────────────────────────────────────────────────────────────────

def fig_correlation_heatmap(df: pd.DataFrame, target: str) -> plt.Figure:
    num_cols = [c for c in NUMERIC_FEATURES + [target] if c in df.columns]
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 7))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    sns.heatmap(
        corr,
        mask=mask,
        cmap=cmap,
        center=0,
        vmin=-1, vmax=1,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 8, "color": C["text"]},
        linewidths=0.4,
        linecolor=C["bg"],
        ax=ax,
        cbar_kws={"shrink": 0.7},
    )
    ax.set_title("Correlation Matrix", fontsize=12, pad=10)
    ax.tick_params(axis="x", rotation=40, labelsize=8)
    ax.tick_params(axis="y", rotation=0,  labelsize=8)
    ax.set_facecolor(C["card"])
    fig.patch.set_facecolor(C["bg"])
    ax.title.set_color(C["text"])
    colorbar = ax.collections[0].colorbar
    colorbar.ax.yaxis.set_tick_params(color=C["muted"])
    plt.setp(colorbar.ax.yaxis.get_ticklabels(), color=C["muted"], fontsize=7)
    colorbar.outline.set_edgecolor(C["border"])
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART 4 — Top-N Feature Correlations with Target
# ─────────────────────────────────────────────────────────────────────────────

def fig_feature_target_correlation(df: pd.DataFrame, target: str, top_n: int = 9) -> plt.Figure:
    num_cols = [c for c in df.select_dtypes(include="number").columns if c != target]
    corr_vals = df[num_cols].corrwith(df[target]).abs().nlargest(top_n)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    colors = [C["teal"] if v >= 0.3 else C["blue1"] if v >= 0.15 else C["muted"]
              for v in corr_vals.values]
    bars = ax.barh(corr_vals.index[::-1], corr_vals.values[::-1],
                   color=colors[::-1], edgecolor=C["bg"], linewidth=0.4, height=0.6)
    ax.axvline(0.3, color=C["teal"],  linewidth=1, linestyle="--", alpha=0.5)
    ax.axvline(0.15, color=C["amber"], linewidth=1, linestyle="--", alpha=0.4)
    ax.set_xlabel("|Pearson r| with Score")
    ax.set_title(f"Top {top_n} Features Correlated with Score")
    ax.set_xlim(0, min(1.0, corr_vals.values.max() * 1.15))
    for bar, val in zip(bars, corr_vals.values[::-1]):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", ha="left", color=C["text"], fontsize=8)
    _apply_theme(fig, ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART 5 — Scatter: key numeric features vs Target
# ─────────────────────────────────────────────────────────────────────────────

def fig_scatter_vs_target(df: pd.DataFrame, target: str) -> plt.Figure:
    priority = ["Hours_Studied", "Attendance", "Previous_GPA", "Sleep_Hours",
                "Stress_Level", "Screen_Time"]
    cols = [c for c in priority if c in df.columns][:6]
    ncols = 3
    nrows = (len(cols) + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=(12, nrows * 3.2))
    axes_flat = axes.flatten() if len(cols) > 1 else [axes]
    score = df[target].dropna()

    for i, col in enumerate(cols):
        ax = axes_flat[i]
        x = df[col]
        valid = x.notna() & score.notna()
        ax.scatter(x[valid], score[valid], alpha=0.25, s=10,
                   color=C["blue1"], edgecolors="none")
        # trend line
        try:
            z = np.polyfit(x[valid], score[valid], 1)
            p = np.poly1d(z)
            x_line = np.linspace(x[valid].min(), x[valid].max(), 200)
            ax.plot(x_line, p(x_line), color=C["teal"], linewidth=1.5)
        except Exception:
            pass
        ax.set_xlabel(col.replace("_", " "), fontsize=8)
        ax.set_ylabel("Score" if i % ncols == 0 else "")
        ax.set_title(col.replace("_", " "), fontsize=9)

    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].set_visible(False)

    _apply_theme(fig, [ax for ax in axes_flat if ax.get_visible()])
    fig.suptitle("Feature vs Score Relationships", color=C["text"], fontsize=12, y=1.01)
    fig.tight_layout(pad=1.2)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART 6 — Categorical Features vs Target (box plots)
# ─────────────────────────────────────────────────────────────────────────────

def fig_categorical_vs_target(df: pd.DataFrame, target: str) -> plt.Figure:
    cats = [c for c in CATEGORICAL_FEATURES if c in df.columns][:6]
    if not cats:
        return None

    ncols = 3
    nrows = (len(cats) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, nrows * 3.2))
    axes_flat = axes.flatten() if len(cats) > 1 else [axes]

    for i, col in enumerate(cats):
        ax = axes_flat[i]
        groups = df[col].dropna().unique()
        groups = sorted(groups)
        data = [df.loc[df[col] == g, target].dropna().values for g in groups]
        palette = _gradient_palette(len(groups))
        bp = ax.boxplot(
            data,
            patch_artist=True,
            medianprops=dict(color=C["teal"], linewidth=2),
            whiskerprops=dict(color=C["sky"], linewidth=1),
            capprops=dict(color=C["sky"], linewidth=1.5),
            flierprops=dict(marker=".", color=C["rose"], markersize=3, alpha=0.4),
        )
        for patch, color in zip(bp["boxes"], palette):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
            patch.set_edgecolor(C["border"])
        ax.set_xticks(range(1, len(groups) + 1))
        ax.set_xticklabels(
            [str(g)[:8] for g in groups],
            fontsize=7,
            rotation=20,
            ha="right"
        )
        ax.set_ylabel("Score" if i % ncols == 0 else "")
        ax.set_title(col.replace("_", " "), fontsize=9)

    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].set_visible(False)

    _apply_theme(fig, [ax for ax in axes_flat if ax.get_visible()])
    fig.suptitle("Score by Categorical Feature", color=C["text"], fontsize=12, y=1.01)
    fig.tight_layout(pad=1.2)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART 7 — Model Feature Importance
# ─────────────────────────────────────────────────────────────────────────────

def fig_feature_importance(top_n: int = 15) -> Optional[plt.Figure]:
    model, features = load_model()
    if model is None:
        return None
    try:
        importances = model.feature_importances_
        feat_series = pd.Series(importances, index=features).nlargest(top_n)

        fig, ax = plt.subplots(figsize=(9, 4))
        colors = _gradient_palette(len(feat_series))
        bars = ax.barh(feat_series.index[::-1], feat_series.values[::-1],
                       color=colors[::-1], edgecolor=C["bg"], linewidth=0.3, height=0.65)
        ax.set_xlabel("Importance Score")
        ax.set_title(f"Top {top_n} Model Feature Importances (XGBoost)")
        for bar, val in zip(bars, feat_series.values[::-1]):
            ax.text(val + feat_series.values.max() * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{val:.4f}", va="center", ha="left", color=C["text"], fontsize=7)
        _apply_theme(fig, ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", visible=True)
        fig.tight_layout()
        return fig
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# CHART 8 — Missing values summary
# ─────────────────────────────────────────────────────────────────────────────

def fig_missing_values(df: pd.DataFrame) -> Optional[plt.Figure]:
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, max(2.5, len(missing) * 0.5)))
    pct = (missing / len(df) * 100)
    ax.barh(missing.index[::-1], pct.values[::-1],
            color=C["rose"], alpha=0.8, edgecolor=C["bg"], linewidth=0.3)
    ax.set_xlabel("Missing (%)")
    ax.set_title("Missing Values by Column")
    for i, (idx, val) in enumerate(zip(missing.index[::-1], pct.values[::-1])):
        ax.text(val + 0.2, i, f"{val:.1f}%", va="center", color=C["text"], fontsize=8)
    _apply_theme(fig, ax)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return fig