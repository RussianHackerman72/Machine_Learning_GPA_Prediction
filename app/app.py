
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import os

from Utils.report_generator import generate_student_report

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="GradeOwl",
    page_icon="🦉",
    layout="wide"
)

st.markdown("""
<style>
            

/* ===== SIDEBAR WRAPPER ===== */
[data-testid="stSidebar"] {
    background: rgba(10, 35, 66, 0.92) !important;
    border-right: 1px solid rgba(255,255,255,0.10) !important;
}

/* ===== SEMBUNYIKAN label default "🧭 Navigation" ===== */
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

/* ===== RADIO GROUP jadi nav list ===== */
[data-testid="stSidebar"] .stRadio > div {
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    padding: 8px 0 !important;
}

/* ===== TIAP ITEM RADIO ===== */
[data-testid="stSidebar"] .stRadio > div > label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.70) !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
    border: 1px solid transparent !important;
}

/* ===== HIDE radio bullet asli ===== */
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}

/* ===== HOVER STATE ===== */
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.09) !important;
    color: #ffffff !important;
}

/* ===== ACTIVE / SELECTED STATE ===== */
[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
    background: rgba(33, 150, 243, 0.22) !important;
    border: 1px solid rgba(33, 150, 243, 0.35) !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* ===== SIDEBAR BRAND AREA (title di atas) ===== */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-size: 18px !important;
}

/* ===== SIDEBAR DIVIDER ===== */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.10) !important;
}


/* ===== OCEAN BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #0a2342 0%, #0d3b6e 30%, #1565a8 60%, #1a7abf 100%);
    min-height: 100vh;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: rgba(10, 35, 66, 0.85) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.12);
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.85) !important;
}

/* ===== TITLES ===== */
h1, h2, h3 {
    color: #ffffff !important;
}
/* ===== TYPOGRAPHY ===== */
.stMarkdown p {
    font-size: 15px !important;
    color: rgba(255,255,255,0.80) !important;
    line-height: 1.7 !important;
}

/* ===== HAPUS border aneh di divider/kolom kosong ===== */
[data-testid="stVerticalBlock"] > div > div {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    backdrop-filter: none !important;
}

/* ===== HAPUS border di horizontal block ===== */
[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
}

/* ===== HAPUS background putih di column ===== */
[data-testid="column"] > div > div > div {
    background: transparent !important;
    border: none !important;
}

/* ===== INPUT ===== */
.stNumberInput input,
.stTextInput input {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    background: linear-gradient(135deg, #2196f3, #1565c0) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    height: 52px;
    font-weight: 600 !important;
    font-size: 15px !important;
    letter-spacing: 0.01em;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    opacity: 0.88;
}

/* ===== METRIC CARD ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    padding: 18px !important;
}
[data-testid="stMetricLabel"] {
    color: rgba(255,255,255,0.6) !important;
}
[data-testid="stMetricValue"] {
    color: #93c5fd !important;
}

/* ===== SUCCESS / WARNING / ERROR / INFO BOX ===== */
.stSuccess {
    background: rgba(52,211,153,0.14) !important;
    border: 1px solid rgba(52,211,153,0.25) !important;
    border-radius: 10px !important;
    color: #a7f3d0 !important;
}
.stWarning {
    background: rgba(251,191,36,0.12) !important;
    border: 1px solid rgba(251,191,36,0.22) !important;
    border-radius: 10px !important;
    color: #fde68a !important;
}
.stError {
    background: rgba(248,113,113,0.14) !important;
    border: 1px solid rgba(248,113,113,0.22) !important;
    border-radius: 10px !important;
    color: #fca5a5 !important;
}
.stInfo {
    background: rgba(96,165,250,0.12) !important;
    border: 1px solid rgba(96,165,250,0.22) !important;
    border-radius: 10px !important;
    color: #bfdbfe !important;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
    color: white !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 0 0 10px 10px !important;
    color: rgba(255,255,255,0.8) !important;
}

/* ===== TEXT UMUM ===== */
p, label, span {
    color: rgba(255,255,255,0.85) !important;
}

/* ===== BAR CHART ===== */
[data-testid="stVegaLiteChart"] {
    background: rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.12) !important;
}

</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR NAVIGATION
# =====================

# Taruh ini SEBELUM st.sidebar.radio
st.sidebar.markdown("""
<div style="
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
    margin-bottom: 12px;
">
    <div style="
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #2196f3, #1565c0);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; flex-shrink: 0;
    ">🦉</div>
    <div>
        <div style="font-size:16px; font-weight:600; color:#fff;">GradeOwl</div>
        <div style="font-size:11px; color:rgba(255,255,255,0.45); margin-top:1px;">AI Grade Predictor</div>
    </div>
</div>
""", unsafe_allow_html=True)


menu = st.sidebar.radio(
    "🧭 Navigation",
    ["🏠 Home", "📊 EDA Dashboard", "🧠 Prediction", "📘 Methodology"]
)

# =====================
# HOME
# =====================
if menu == "🏠 Home":

    # ── HERO ──────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom: 8px;">
        <span style="
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(33,150,243,0.2); border: 1px solid rgba(33,150,243,0.35);
            color: #93c5fd; font-size: 11px; font-weight: 500;
            padding: 5px 12px; border-radius: 999px; letter-spacing: 0.04em;
            text-transform: uppercase;
        ">Machine Learning · XGBoost</span>
    </div>
    <h1 style="font-size:32px; font-weight:700; color:#fff; line-height:1.2; margin-bottom:12px;">
        Predict Your Academic<br>Performance with <span style="color:#60a5fa;">AI</span>
    </h1>
    <p style="font-size:14px; color:rgba(255,255,255,0.6); line-height:1.7; max-width:600px; margin-bottom:8px;">
        GradeOwl menganalisis kebiasaan belajar, pola tidur, dan faktor perilaku untuk
        memprediksi nilai akhir kamu — dan memberikan rekomendasi personal untuk meningkatkannya.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── PROBLEM ───────────────────────────────────────────
    st.markdown('<p style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;">Tantangan yang dihadapi mahasiswa</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="display:flex; align-items:flex-start; gap:10px;
            background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10);
            border-radius:10px; padding:14px; margin-bottom:10px;">
            <div style="width:32px;height:32px;border-radius:8px;background:rgba(248,113,113,0.18);
                display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px;">📱</div>
            <div>
                <div style="font-size:13px;font-weight:500;color:#fff;margin-bottom:2px;">Screen time berlebihan</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.45);">Distraksi media sosial menurunkan fokus belajar</div>
            </div>
        </div>
        <div style="display:flex; align-items:flex-start; gap:10px;
            background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10);
            border-radius:10px; padding:14px;">
            <div style="width:32px;height:32px;border-radius:8px;background:rgba(167,139,250,0.15);
                display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px;">😰</div>
            <div>
                <div style="font-size:13px;font-weight:500;color:#fff;margin-bottom:2px;">Stres akademik tinggi</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.45);">Exam anxiety menurunkan performa saat ujian</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="display:flex; align-items:flex-start; gap:10px;
            background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10);
            border-radius:10px; padding:14px; margin-bottom:10px;">
            <div style="width:32px;height:32px;border-radius:8px;background:rgba(251,191,36,0.15);
                display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px;">😴</div>
            <div>
                <div style="font-size:13px;font-weight:500;color:#fff;margin-bottom:2px;">Kurang tidur</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.45);">Begadang menjelang ujian merusak retensi memori</div>
            </div>
        </div>
        <div style="display:flex; align-items:flex-start; gap:10px;
            background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10);
            border-radius:10px; padding:14px;">
            <div style="width:32px;height:32px;border-radius:8px;background:rgba(96,165,250,0.15);
                display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px;">📖</div>
            <div>
                <div style="font-size:13px;font-weight:500;color:#fff;margin-bottom:2px;">Jam belajar tidak konsisten</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.45);">Tanpa pola belajar teratur, nilai sulit stabil</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── STATS ─────────────────────────────────────────────
    st.markdown('<p style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;">Fakta yang perlu diketahui</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, num, desc in [
        (c1, "60%+", "Mahasiswa alami stres akademik selama kuliah"),
        (c2, "70%+", "Kesulitan mengatur waktu belajar efektif"),
        (c3, "80%+", "Nilai dipengaruhi faktor non-akademik"),
        (c4, "100%", "Butuh evaluasi belajar yang lebih personal"),
    ]:
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.12);
            border-radius:12px; padding:16px 12px; text-align:center;">
            <div style="font-size:26px; font-weight:700; color:#60a5fa; line-height:1; margin-bottom:6px;">{num}</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.45); line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── IMPACT ────────────────────────────────────────────
    st.markdown('<p style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;">Dampak pada mahasiswa</p>', unsafe_allow_html=True)

    i1, i2, i3 = st.columns(3)
    impacts = [
        (i1, "📉", "rgba(248,113,113,0.15)", "Performa Akademik",
         ["Nilai ujian menurun", "Sulit memahami materi", "Risiko gagal mata kuliah"]),
        (i2, "🧠", "rgba(167,139,250,0.15)", "Kesehatan Mental",
         ["Burnout & kelelahan", "Overthinking berlebih", "Academic anxiety"]),
        (i3, "⏰", "rgba(251,191,36,0.15)", "Manajemen Waktu",
         ["Belajar tidak efektif", "Distraksi media sosial", "Produktivitas rendah"]),
    ]
    for col, icon, bg, title, items in impacts:
        items_html = "".join([
            f'<div style="font-size:12px;color:rgba(255,255,255,0.5);padding:3px 0;display:flex;align-items:center;gap:6px;"><div style="width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,0.25);flex-shrink:0;"></div>{i}</div>'
            for i in items
        ])
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10);
            border-radius:12px; padding:16px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                <div style="width:30px;height:30px;border-radius:8px;background:{bg};
                    display:flex;align-items:center;justify-content:center;font-size:15px;">{icon}</div>
                <div style="font-size:13px;font-weight:600;color:#fff;">{title}</div>
            </div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── SOLUTION ──────────────────────────────────────────
    st.markdown('<p style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;">Solusi GradeOwl</p>', unsafe_allow_html=True)

    solutions = [
        "Memprediksi nilai akhir mahasiswa",
        "Mengidentifikasi kekuatan akademik",
        "Menemukan kelemahan yang perlu diperbaiki",
        "Memberikan rekomendasi personal",
        "Simulasi peningkatan nilai",
        "Analisis berbasis data perilaku belajar",
    ]
    s_cols = st.columns(2)
    for i, sol in enumerate(solutions):
        s_cols[i % 2].markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;
            background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.18);
            border-radius:10px; padding:11px 14px; margin-bottom:8px;">
            <div style="width:20px;height:20px;border-radius:50%;background:rgba(52,211,153,0.2);
                color:#6ee7b7;display:flex;align-items:center;justify-content:center;
                flex-shrink:0;font-size:12px;">✓</div>
            <span style="font-size:13px;color:rgba(255,255,255,0.8);">{sol}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── HOW IT WORKS ──────────────────────────────────────
    st.markdown('<p style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;">Cara kerja sistem</p>', unsafe_allow_html=True)

    steps = ["Student Profile", "Feature Engineering", "XGBoost Model",
             "Score Prediction", "Behavior Analysis", "Recommendations"]
    flow_html = " → ".join([
        f'<span style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.14);'
        f'border-radius:8px;padding:7px 13px;font-size:12px;color:rgba(255,255,255,0.7);">{s}</span>'
        for s in steps
    ])
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:8px;">{flow_html}</div>', unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── FEATURES ──────────────────────────────────────────
    st.markdown('<p style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;">Fitur utama</p>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        (f1, "🎯", "rgba(96,165,250,0.18)",  "Score Prediction",  "Prediksi nilai akhir berdasarkan profil belajar"),
        (f2, "💪", "rgba(52,211,153,0.16)",   "Strength Analysis", "Kenali faktor pendukung performa kamu"),
        (f3, "📈", "rgba(251,191,36,0.15)",   "Improvement Plan",  "Simulasi kenaikan nilai dari perubahan perilaku"),
        (f4, "🤖", "rgba(167,139,250,0.15)",  "ML Powered",        "XGBoost dilatih pada data mahasiswa nyata"),
    ]
    for col, icon, bg, title, desc in features:
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.12);
            border-radius:12px; padding:16px 14px;">
            <div style="width:36px;height:36px;border-radius:10px;background:{bg};
                display:flex;align-items:center;justify-content:center;
                font-size:18px;margin-bottom:10px;">{icon}</div>
            <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:4px;">{title}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.45);line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; background:rgba(33,150,243,0.12);
        border:1px solid rgba(33,150,243,0.25); border-radius:16px; padding:36px 24px;">
        <div style="font-size:22px;font-weight:700;color:#fff;margin-bottom:8px;">
            Siap cek performa akademikmu?
        </div>
        <p style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:0;">
            Pilih <b style="color:rgba(255,255,255,0.75);">Prediction</b> di sidebar untuk mulai.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================
# EDA DASHBOARD
# =====================
# =====================
# EDA DASHBOARD  (drop-in replacement for the old static-image block)
# =====================
elif menu == "📊 EDA Dashboard":

    from Utils.eda_dashboard import (
        load_dataset,
        get_summary,
        fig_target_distribution,
        fig_numeric_distributions,
        fig_correlation_heatmap,
        fig_feature_target_correlation,
        fig_scatter_vs_target,
        fig_categorical_vs_target,
        fig_feature_importance,
        fig_missing_values,
    )

    # ── page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:6px;">
        <span style="
            display:inline-flex;align-items:center;gap:6px;
            background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.30);
            color:#6ee7b7;font-size:11px;font-weight:500;
            padding:5px 12px;border-radius:999px;letter-spacing:0.04em;text-transform:uppercase;
        ">Dataset · Exploratory Data Analysis</span>
    </div>
    <h1 style="font-size:28px;font-weight:700;color:#fff;line-height:1.2;margin-bottom:8px;">
        Training Data <span style="color:#60a5fa;">Insights</span>
    </h1>
    <p style="font-size:13px;color:rgba(255,255,255,0.5);max-width:640px;">
        Explore the dataset used to train GradeOwl — distributions, correlations, feature
        importances, and the relationships that drive the prediction.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:20px 0;"></div>',
                unsafe_allow_html=True)

    # ── optional custom path ───────────────────────────────────────────────────
    with st.expander("⚙️  Custom dataset path (optional)"):
        custom_path = st.text_input(
            "CSV path",
            placeholder="e.g. data/student_data.csv",
            help="Leave blank to auto-detect from common paths."
        )

    # ── load data ─────────────────────────────────────────────────────────────
    with st.spinner("Loading dataset…"):
        df, target_col = load_dataset(custom_path if custom_path else None)

    if df is None:
        st.error(
            "**Dataset not found.** GradeOwl looked for the CSV in common paths "
            "(`data/student_data.csv`, etc.) but couldn't find it. "
            "Enter the correct path in the expander above."
        )
        st.stop()

    summary = get_summary(df, target_col)

    # ── SECTION 1 — Dataset overview ─────────────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                'Dataset overview</p>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    for col, label, value in [
        (m1, "Rows",          f"{summary['n_rows']:,}"),
        (m2, "Columns",       str(summary['n_cols'])),
        (m3, "Numeric cols",  str(summary['n_numeric'])),
        (m4, "Missing vals",  str(summary['n_missing'])),
        (m5, "Mean score",    str(summary['target_mean'])),
        (m6, "Score range",   f"{summary['target_min']}–{summary['target_max']}"),
    ]:
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
            border-radius:12px;padding:14px 10px;text-align:center;">
            <div style="font-size:20px;font-weight:700;color:#60a5fa;line-height:1;margin-bottom:5px;">{value}</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.4);">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)

    # ── SECTION 2 — Raw data preview ─────────────────────────────────────────
    with st.expander("🔍  Raw data preview (first 50 rows)"):
        st.dataframe(df.head(50), use_container_width=True)

    with st.expander("📋  Descriptive statistics"):
        st.dataframe(df.describe().T.round(3), use_container_width=True)

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)

    # ── SECTION 3 — Target distribution ──────────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                'Target variable — exam score</p>', unsafe_allow_html=True)

    fig = fig_target_distribution(df, target_col)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # score band breakdown
    bins   = [0, 60, 70, 80, 90, 101]
    labels = ["<60 (Poor)", "60–70 (Fair)", "70–80 (Good)", "80–90 (Very Good)", "90–100 (Excellent)"]
    colors_band = ["rgba(248,113,113,0.20)", "rgba(251,191,36,0.16)",
                   "rgba(96,165,250,0.16)",  "rgba(52,211,153,0.16)", "rgba(167,139,250,0.16)"]

    df["_band"] = pd.cut(df[target_col], bins=bins, labels=labels, right=False)
    band_counts = df["_band"].value_counts().reindex(labels, fill_value=0)
    band_pcts   = (band_counts / len(df) * 100).round(1)

    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.08em;margin:18px 0 10px;">'
                'Score band breakdown</p>', unsafe_allow_html=True)

    b_cols = st.columns(5)
    for i, (label, count, pct, bg) in enumerate(zip(labels, band_counts, band_pcts, colors_band)):
        b_cols[i].markdown(f"""
        <div style="background:{bg};border:1px solid rgba(255,255,255,0.10);
            border-radius:10px;padding:12px 8px;text-align:center;">
            <div style="font-size:18px;font-weight:700;color:#fff;">{count:,}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.55);margin:2px 0;">{pct}%</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.30);line-height:1.4;">{label}</div>
        </div>""", unsafe_allow_html=True)

    df.drop(columns=["_band"], inplace=True, errors="ignore")

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)

    # ── SECTION 4 — Numeric distributions ────────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                'Numeric feature distributions</p>', unsafe_allow_html=True)

    fig = fig_numeric_distributions(df)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)

    # ── SECTION 5 — Correlation heatmap ──────────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                'Correlation matrix</p>', unsafe_allow_html=True)

    col_hm, col_bar = st.columns([3, 2])
    with col_hm:
        fig = fig_correlation_heatmap(df, target_col)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col_bar:
        fig = fig_feature_target_correlation(df, target_col)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.caption("Teal bars (|r| ≥ 0.30) = strong correlation · Dashed lines mark 0.30 and 0.15 thresholds")

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)

    # ── SECTION 6 — Feature vs Score scatter ──────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                'Feature–score relationships</p>', unsafe_allow_html=True)

    fig = fig_scatter_vs_target(df, target_col)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("Teal trend line = linear fit. Upward slope = positive predictor; downward = negative.")

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)

    # ── SECTION 7 — Categorical breakdown ─────────────────────────────────────
    cat_cols = [c for c in [
        "Gender", "Part_Time_Job", "Study_Method", "Diet_Quality",
        "Internet_Quality", "Extracurricular", "Family_Income_Level"
    ] if c in df.columns]

    if cat_cols:
        st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                    'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                    'Score by categorical feature</p>', unsafe_allow_html=True)

        fig = fig_categorical_vs_target(df, target_col)
        if fig:
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                    unsafe_allow_html=True)

    # ── SECTION 8 — Model feature importance ──────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                'Model feature importance (XGBoost)</p>', unsafe_allow_html=True)

    fig_imp = fig_feature_importance(top_n=15)
    if fig_imp:
        st.pyplot(fig_imp, use_container_width=True)
        plt.close(fig_imp)
    else:
        st.info("Feature importance chart unavailable — model files not found at `models/`.")

    # ── SECTION 9 — Missing values ─────────────────────────────────────────────
    fig_mv = fig_missing_values(df)
    if fig_mv:
        st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                    unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.35);'
                    'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">'
                    'Missing values</p>', unsafe_allow_html=True)
        st.pyplot(fig_mv, use_container_width=True)
        plt.close(fig_mv)
    else:
        st.success("✅ No missing values found in the dataset.")

    st.markdown('<div style="border-top:1px solid rgba(255,255,255,0.08);margin:24px 0;"></div>',
                unsafe_allow_html=True)
    st.caption("All charts generated dynamically from the training CSV at runtime.")

# =====================
# PREDICTION
# =====================
# =====================
# PREDICTION
# =====================
elif menu == "🧠 Prediction":

    st.title("🧠 Student Score Prediction")

    st.markdown("Fill in student profile below:")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 15, 40, 20)
        gpa = st.number_input("Previous GPA", 0.0, 4.0, 3.0)
        hours = st.number_input("Hours Studied", 0, 50, 10)
        tutoring = st.number_input("Tutoring Sessions", 0, 10, 2)
        attendance = st.number_input("Attendance (%)", 0, 100, 80)

    with col2:
        sleep = st.number_input("Sleep Hours", 0, 12, 7)
        screen = st.number_input("Screen Time", 0, 15, 5)
        stress = st.number_input("Stress Level", 0, 10, 5)
        anxiety = st.number_input("Exam Anxiety Score", 0, 10, 5)

        gender = st.selectbox(
            "Gender",
            ["Female", "Male", "Non-Binary"]
        )

    st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

    plans = None
    if st.button("🔮 Predict My Grade"):

        student = {
            "Age": age,
            "Gender": gender,
            "Hours_Studied": hours,
            "Attendance": attendance,
            "Sleep_Hours": sleep,
            "Stress_Level": stress,
            "Screen_Time": screen,
            "Previous_GPA": gpa,
            "Tutoring_Sessions_Per_Week": tutoring,
            "Exam_Anxiety_Score": anxiety,

            "Part_Time_Job": "No",
            "Study_Method": "Online",
            "Diet_Quality": "Good",
            "Internet_Quality": "Good",
            "Extracurricular": "No",
            "Family_Income_Level": "Medium"
        }

        report = generate_student_report(student)

        prediction = report["Prediction"]

        score = prediction["score"]
        category = prediction["category"]
        # plans = report["Improvement Plans"]

        st.markdown("## 🎯 Prediction Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Predicted Score",
                value=f"{score:.2f}"
            )
            

        with col2:
            if score >= 80:
                st.success(category)

            elif score >= 60:
                    st.warning(category)

            else:
                st.error(category)

        st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

        st.subheader("💪 Strengths")

        if prediction["strengths"]:
            for item in prediction["strengths"]:
                st.success(item)
        else:
            st.info("No significant strengths detected.")

        st.subheader("⚠️ Weaknesses")

        if prediction["weaknesses"]:
            for item in prediction["weaknesses"]:
                st.warning(item)
        else:
            st.success("No major weaknesses detected.")

        st.subheader("💡 Recommendations")

        if prediction["recommendations"]:
            for item in prediction["recommendations"]:
                st.info(item)
        else:
            st.success("No recommendations needed.")

        st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)

        st.subheader("🚀 Improvement Plans")

        plans = report["Improvement Plans"]

        for plan in plans:

            with st.expander(
            f"{plan['plan']} Plan (+{plan['gain']} Score)"
            ):

                st.write(
                    f"Current Score : {plan['current_score']}"
                )

                st.write(
                    f"Improved Score : {plan['improved_score']}"
                )

                st.write(
                    f"Potential Gain : +{plan['gain']}"
                )

                st.markdown("### Suggested Changes")

                for change in plan["changes"]:
                    st.write(f"✅ {change}")

    # =====================
    # SCORE IMPROVEMENT CHART
    # =====================

    # =====================
# SCORE IMPROVEMENT METRICS
# =====================

    if plans is not None:

        st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;"></div>', unsafe_allow_html=True)
        st.subheader("📈 Score Improvement Projection")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Conservative Gain",
                f"+{plans[0]['gain']}"
            )

        with col2:
            st.metric(
                "Moderate Gain",
                f"+{plans[1]['gain']}"
            )

        with col3:
            st.metric(
                "Ambitious Gain",
                f"+{plans[2]['gain']}"
            )

    # =====================
    # BAR CHART
    # =====================

        chart_df = pd.DataFrame({
            "Plan": [
            "Current",
                "Conservative",
                "Moderate",
                "Ambitious"
            ],
        
            "Score": [
                plans[0]["current_score"],
                plans[0]["improved_score"],
                plans[1]["improved_score"],
                plans[2]["improved_score"]
            ]
        })

        st.bar_chart(
            chart_df.set_index("Plan")
        )

        st.caption(
            "Estimated score improvement based on simulated behavioral changes."
        )

# =====================
# METHODOLOGY
# =====================
elif menu == "📘 Methodology":

    st.title("📘 Machine Learning Pipeline")

    st.markdown("""
    ### 1. Data Collection
    Student academic & behavioral dataset

    ### 2. Preprocessing
    - Handling missing values
    - Feature selection

    ### 3. Model Training
    - XGBoost Regressor (best performance)
    - Random Forest (comparison model)

    ### 4. Evaluation
    - MAE, RMSE metrics
    - Model selection based on accuracy

    ### 5. Deployment
    - Streamlit web app
    - model.pkl integration
    """)

    st.success("End-to-end ML pipeline completed 🚀")