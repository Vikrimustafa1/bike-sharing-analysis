"""
Dashboard Analisis Data: Bike Sharing Dataset
Proyek Akhir Kelas Belajar Analisis Data dengan Python — Dicoding
Author : Muhammad Vikri Mustafa
Email  : vikrimustafa24@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ─── Konfigurasi Halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Kustom ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title   { font-size:2rem; font-weight:700; color:#1565C0; margin-bottom:0.2rem; }
    .sub-title    { font-size:1rem; color:#546E7A; margin-bottom:1.5rem; }
    .metric-card  { background:#F0F4FF; border-radius:12px; padding:1rem 1.2rem; 
                    border-left:4px solid #1565C0; }
    .metric-val   { font-size:1.8rem; font-weight:700; color:#1565C0; }
    .metric-lbl   { font-size:0.82rem; color:#546E7A; }
    .section-hdr  { font-size:1.15rem; font-weight:600; color:#1A237E; 
                    border-bottom:2px solid #E8EAF6; padding-bottom:4px; margin-top:0.5rem; }
    .insight-box  { background:#E8F5E9; border-left:4px solid #43A047; 
                    border-radius:8px; padding:0.9rem 1rem; margin-top:0.6rem; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)

@st.cache_data
def load_data():
    day_path  = os.path.join(BASE_DIR, "main_data_day.csv")
    hour_path = os.path.join(BASE_DIR, "main_data_hour.csv")
    day_df  = pd.read_csv(day_path,  parse_dates=["dteday"])
    hour_df = pd.read_csv(hour_path, parse_dates=["dteday"])
    return day_df, hour_df

day_df, hour_df = load_data()

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-size:4rem; text-align:center;'>🚲</div>", unsafe_allow_html=True)
    st.markdown("## 🚲 Bike Sharing")
    st.markdown("**Proyek Analisis Data**\nMuhammad Vikri Mustafa")
    st.markdown("---")

    st.markdown("### 🔎 Filter Data")

    # Filter Tahun
    year_options = {"Semua Tahun": None, "2011": "2011", "2012": "2012"}
    selected_year = st.selectbox("Tahun:", list(year_options.keys()))

    # Filter Musim (multiselect agar heatmap & clustering bisa tampil)
    all_seasons = ["Spring", "Summer", "Fall", "Winter"]
    selected_season = st.multiselect(
        "Musim:",
        options=all_seasons,
        default=all_seasons,
    )

    # Filter Cuaca
    weather_options = ["Semua Cuaca", "Clear/Partly Cloudy", "Mist/Cloudy", "Light Rain/Snow"]
    selected_weather = st.selectbox("Kondisi Cuaca:", weather_options)

    st.markdown("---")
    st.markdown("### ℹ️ Tentang Dataset")
    st.markdown(
        "**Capital Bikeshare System**  \nWashington D.C., USA  \n"
        "Periode: Jan 2011 – Des 2012  \n"
        "Sumber: UCI Machine Learning Repository"
    )

# ─── Filter Logic ───────────────────────────────────────────────────────────
filtered_day  = day_df.copy()
filtered_hour = hour_df.copy()

if year_options[selected_year]:
    filtered_day  = filtered_day[filtered_day["yr_label"]  == year_options[selected_year]]
    filtered_hour = filtered_hour[filtered_hour["yr_label"] == year_options[selected_year]]

if selected_season and len(selected_season) < 4:
    filtered_day  = filtered_day[filtered_day["season_label"].isin(selected_season)]
    filtered_hour = filtered_hour[filtered_hour["season_label"].isin(selected_season)]

if selected_weather != "Semua Cuaca":
    filtered_day  = filtered_day[filtered_day["weather_label"]  == selected_weather]
    filtered_hour = filtered_hour[filtered_hour["weather_label"] == selected_weather]

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🚲 Dashboard Analisis Bike Sharing</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Capital Bikeshare System, Washington D.C. 2011–2012 | '
    'Proyek Akhir — Belajar Analisis Data dengan Python (Dicoding)</div>',
    unsafe_allow_html=True
)

# ─── Metric Cards ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">📊 Ringkasan Statistik Terpilih</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

total_rent   = filtered_day["cnt"].sum()
avg_daily    = filtered_day["cnt"].mean()
total_casual = filtered_day["casual"].sum()
total_reg    = filtered_day["registered"].sum()
peak_day_val = filtered_day["cnt"].max()

def fmt_metric(val):
    """Format angka metric; tampilkan '-' jika NaN atau data kosong."""
    try:
        if pd.isna(val):
            return "-"
        return f"{val:,.0f}"
    except (TypeError, ValueError):
        return "-"

def metric_html(value, label):
    return f"""
    <div class="metric-card">
        <div class="metric-val">{value}</div>
        <div class="metric-lbl">{label}</div>
    </div>"""

c1.markdown(metric_html(fmt_metric(total_rent),   "Total Penyewaan"), unsafe_allow_html=True)
c2.markdown(metric_html(fmt_metric(avg_daily),    "Rata-rata Harian"), unsafe_allow_html=True)
c3.markdown(metric_html(fmt_metric(total_casual), "Pengguna Kasual"), unsafe_allow_html=True)
c4.markdown(metric_html(fmt_metric(total_reg),    "Pengguna Terdaftar"), unsafe_allow_html=True)
c5.markdown(metric_html(fmt_metric(peak_day_val), "Penyewaan Tertinggi/Hari"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB NAVIGASI
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🌤️ Q1: Musim & Cuaca",
    "⏱️ Q2: Pola Per Jam",
    "📈 Tren Waktu",
    "🔬 Analisis Lanjutan",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Pertanyaan 1: Musim & Cuaca
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-hdr">Pertanyaan 1: Pengaruh Musim & Cuaca terhadap Penyewaan Harian</div>',
                unsafe_allow_html=True)
    st.markdown(
        "> **Bagaimana rata-rata jumlah peminjaman sepeda harian berdasarkan musim dan kondisi cuaca "
        "selama 2011–2012, dan kombinasi mana yang menghasilkan penyewaan tertinggi?**"
    )

    col_a, col_b = st.columns(2)

    # ── Bar Chart: Per Musim ─────────────────────────────────────────────────
    with col_a:
        st.markdown("**Rata-rata Penyewaan per Musim**")
        season_order   = ["Spring", "Summer", "Fall", "Winter"]
        season_colors  = ["#FFA726", "#66BB6A", "#EF5350", "#42A5F5"]
        season_avg     = (
            filtered_day.groupby("season_label")["cnt"]
            .mean()
            .reindex([s for s in season_order if s in filtered_day["season_label"].unique()])
        )

        fig1, ax1 = plt.subplots(figsize=(6, 4.2))
        bars = ax1.bar(season_avg.index, season_avg.values,
                       color=[season_colors[season_order.index(s)] for s in season_avg.index],
                       width=0.55, edgecolor="white", linewidth=0.8)
        for bar, val in zip(bars, season_avg.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 40,
                     f"{val:,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        if not filtered_day.empty:
            ax1.axhline(filtered_day["cnt"].mean(), color="black",
                        linestyle="--", linewidth=1.2, alpha=0.6,
                        label=f"Rata-rata ({filtered_day['cnt'].mean():,.0f})")
            ax1.legend(fontsize=8)
        ax1.set_xlabel("Musim", fontsize=9)
        ax1.set_ylabel("Rata-rata Penyewaan", fontsize=9)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.tick_params(labelsize=9)
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

    # ── Bar Chart: Per Cuaca ─────────────────────────────────────────────────
    with col_b:
        st.markdown("**Rata-rata Penyewaan per Kondisi Cuaca**")
        weather_order  = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Rain/Snow"]
        weather_colors = ["#2196F3", "#78909C", "#FF7043"]
        weather_short  = ["Clear/\nPartly Cloudy", "Mist/\nCloudy", "Light Rain/\nSnow"]
        weather_avg    = (
            filtered_day.groupby("weather_label")["cnt"]
            .mean()
            .reindex([w for w in weather_order if w in filtered_day["weather_label"].unique()])
        )

        fig2, ax2 = plt.subplots(figsize=(6, 4.2))
        idx_map  = {w: i for i, w in enumerate(weather_order)}
        bar_lbls = [weather_short[idx_map[w]] for w in weather_avg.index]
        bars2 = ax2.bar(bar_lbls, weather_avg.values,
                        color=[weather_colors[idx_map[w]] for w in weather_avg.index],
                        width=0.5, edgecolor="white", linewidth=0.8)
        for bar, val in zip(bars2, weather_avg.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 40,
                     f"{val:,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        if not filtered_day.empty:
            ax2.axhline(filtered_day["cnt"].mean(), color="black",
                        linestyle="--", linewidth=1.2, alpha=0.6)
        ax2.set_xlabel("Kondisi Cuaca", fontsize=9)
        ax2.set_ylabel("Rata-rata Penyewaan", fontsize=9)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.tick_params(labelsize=9)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # ── Heatmap Musim × Cuaca ────────────────────────────────────────────────
    st.markdown("**Heatmap: Rata-rata Penyewaan per Kombinasi Musim × Cuaca**")
    if not filtered_day.empty:
        pivot = (
            filtered_day.groupby(["season_label", "weather_label"])["cnt"]
            .mean()
            .unstack(fill_value=0)
            .reindex(index=[s for s in season_order if s in filtered_day["season_label"].unique()],
                     columns=[w for w in weather_order if w in filtered_day["weather_label"].unique()])
        )
        fig_hm, ax_hm = plt.subplots(figsize=(9, 3.5))
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd",
                    linewidths=0.5, linecolor="white",
                    annot_kws={"size": 10, "weight": "bold"}, ax=ax_hm)
        ax_hm.set_xlabel("Kondisi Cuaca", fontsize=10)
        ax_hm.set_ylabel("Musim", fontsize=10)
        ax_hm.tick_params(labelsize=9)
        plt.tight_layout()
        st.pyplot(fig_hm)
        plt.close()

    st.markdown(
        '<div class="insight-box">'
        "💡 <strong>Insight:</strong> Musim Gugur (<em>Fall</em>) menghasilkan rata-rata penyewaan "
        "tertinggi (~5.644/hari), 116% lebih tinggi dari Spring. Cuaca cerah meningkatkan "
        "penyewaan hingga 170% dibandingkan kondisi hujan/salju ringan. Suhu berkorelasi "
        "positif kuat dengan jumlah penyewaan (r ≈ 0.63)."
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Pertanyaan 2: Pola Per Jam
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-hdr">Pertanyaan 2: Pola Penggunaan Per Jam — Hari Kerja vs Hari Libur</div>',
                unsafe_allow_html=True)
    st.markdown(
        "> **Pada jam berapa puncak penggunaan terjadi pada hari kerja vs hari libur/akhir pekan, "
        "dan bagaimana pola ini mencerminkan perilaku pengguna kasual vs terdaftar?**"
    )

    hours = list(range(24))
    working = filtered_hour[filtered_hour["workingday"] == 1].groupby("hr")["cnt"].mean()
    holiday = filtered_hour[filtered_hour["workingday"] == 0].groupby("hr")["cnt"].mean()
    casual_h = filtered_hour.groupby("hr")["casual"].mean()
    reg_h    = filtered_hour.groupby("hr")["registered"].mean()

    col1, col2 = st.columns(2)

    # ── Line Chart: Hari Kerja vs Libur ──────────────────────────────────────
    with col1:
        st.markdown("**Total Penyewaan per Jam: Hari Kerja vs Hari Libur/Akhir Pekan**")
        fig3, ax3 = plt.subplots(figsize=(7, 4.5))
        if not working.empty:
            ax3.plot(working.index, working.values, marker="o", color="#1565C0",
                     linewidth=2.2, markersize=4, label="Hari Kerja")
            pk_w = working.idxmax()
            ax3.annotate(f"Puncak\n{pk_w:02d}:00\n({working.max():.0f})",
                         xy=(pk_w, working.max()),
                         xytext=(pk_w - 5 if pk_w > 5 else pk_w + 1, working.max() + 15),
                         fontsize=8, color="#1565C0", fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.2))
        if not holiday.empty:
            ax3.plot(holiday.index, holiday.values, marker="s", color="#E53935",
                     linewidth=2.2, markersize=4, linestyle="--",
                     label="Hari Libur/Akhir Pekan")
            pk_h = holiday.idxmax()
            ax3.annotate(f"Puncak\n{pk_h:02d}:00\n({holiday.max():.0f})",
                         xy=(pk_h, holiday.max()),
                         xytext=(pk_h + 1 if pk_h < 20 else pk_h - 6, holiday.max() + 15),
                         fontsize=8, color="#E53935", fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#E53935", lw=1.2))
        ax3.axvspan(7.5, 9.5,   alpha=0.10, color="#1565C0")
        ax3.axvspan(16.5, 18.5, alpha=0.10, color="#4CAF50")
        ax3.axvspan(11.5, 14.5, alpha=0.10, color="#E53935")
        ax3.set_xlabel("Jam (0–23)", fontsize=9)
        ax3.set_ylabel("Rata-rata Penyewaan/Jam", fontsize=9)
        ax3.set_xticks(hours)
        ax3.legend(fontsize=9)
        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)
        ax3.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    # ── Area Chart: Kasual vs Terdaftar ──────────────────────────────────────
    with col2:
        st.markdown("**Penyewaan per Jam: Pengguna Kasual vs Terdaftar**")
        fig4, ax4 = plt.subplots(figsize=(7, 4.5))
        if not casual_h.empty:
            ax4.fill_between(hours, casual_h.reindex(hours, fill_value=0).values, alpha=0.25, color="#FF7043")
            ax4.plot(hours, casual_h.reindex(hours, fill_value=0).values, marker="o", color="#FF7043",
                     linewidth=2.2, markersize=4, label="Kasual")
            pk_c = casual_h.idxmax()
            ax4.annotate(f"{pk_c:02d}:00\n({casual_h.max():.0f})",
                         xy=(pk_c, casual_h.max()),
                         xytext=(pk_c - 4 if pk_c > 4 else pk_c + 1, casual_h.max() + 5),
                         fontsize=8, color="#E64A19", fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#E64A19", lw=1.2))
        if not reg_h.empty:
            ax4.fill_between(hours, reg_h.reindex(hours, fill_value=0).values, alpha=0.20, color="#1565C0")
            ax4.plot(hours, reg_h.reindex(hours, fill_value=0).values, marker="s", color="#1565C0",
                     linewidth=2.2, markersize=4, label="Terdaftar")
            pk_r = reg_h.idxmax()
            ax4.annotate(f"{pk_r:02d}:00\n({reg_h.max():.0f})",
                         xy=(pk_r, reg_h.max()),
                         xytext=(pk_r + 1, reg_h.max() + 5),
                         fontsize=8, color="#0D47A1", fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#0D47A1", lw=1.2))
        ax4.set_xlabel("Jam (0–23)", fontsize=9)
        ax4.set_ylabel("Rata-rata Penyewaan/Jam", fontsize=9)
        ax4.set_xticks(hours)
        ax4.legend(fontsize=9)
        ax4.spines["top"].set_visible(False)
        ax4.spines["right"].set_visible(False)
        ax4.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    # ── Tabel ringkasan jam puncak ────────────────────────────────────────────
    st.markdown("**Ringkasan Jam Puncak**")
    summary_rows = []
    if not working.empty:
        summary_rows.append({"Kategori": "Hari Kerja", "Jam Puncak": f"{working.idxmax():02d}:00",
                              "Rata-rata/Jam": f"{working.max():,.1f}"})
    if not holiday.empty:
        summary_rows.append({"Kategori": "Hari Libur/Akhir Pekan", "Jam Puncak": f"{holiday.idxmax():02d}:00",
                              "Rata-rata/Jam": f"{holiday.max():,.1f}"})
    if not casual_h.empty:
        summary_rows.append({"Kategori": "Pengguna Kasual", "Jam Puncak": f"{casual_h.idxmax():02d}:00",
                              "Rata-rata/Jam": f"{casual_h.max():,.1f}"})
    if not reg_h.empty:
        summary_rows.append({"Kategori": "Pengguna Terdaftar", "Jam Puncak": f"{reg_h.idxmax():02d}:00",
                              "Rata-rata/Jam": f"{reg_h.max():,.1f}"})
    if summary_rows:
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="insight-box">'
        "💡 <strong>Insight:</strong> Hari kerja menunjukkan pola <em>bimodal komuter</em> "
        "(puncak 08:00 & 17:00), sedangkan hari libur menunjukkan pola <em>unimodal rekreasi</em> "
        "(puncak 13:00). Pengguna terdaftar mendominasi hari kerja (~76%), sementara pengguna "
        "kasual lebih aktif di hari libur (~37% dari total)."
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Tren Waktu
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-hdr">📈 Tren Penyewaan Sepanjang Waktu</div>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)

    # ── Tren Bulanan ──────────────────────────────────────────────────────────
    with col_t1:
        st.markdown("**Tren Bulanan per Tahun**")
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        fig5, ax5 = plt.subplots(figsize=(7, 4.2))
        colors_yr = {"2011": "#1E88E5", "2012": "#E53935"}
        for yr in sorted(filtered_day["yr_label"].unique()):
            data = filtered_day[filtered_day["yr_label"] == yr].groupby("mnth")["cnt"].mean()
            ax5.plot(data.index, data.values, marker="o", label=f"Tahun {yr}",
                     color=colors_yr.get(yr, "gray"), linewidth=2, markersize=5)
        ax5.set_xticks(range(1, 13))
        ax5.set_xticklabels(month_names, fontsize=9)
        ax5.set_ylabel("Rata-rata Penyewaan Harian", fontsize=9)
        ax5.legend(fontsize=9)
        ax5.spines["top"].set_visible(False)
        ax5.spines["right"].set_visible(False)
        ax5.tick_params(labelsize=9)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

    # ── Distribusi per Hari dalam Seminggu ────────────────────────────────────
    with col_t2:
        st.markdown("**Rata-rata Penyewaan per Hari dalam Seminggu**")
        weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekday_avg   = (
            filtered_day.groupby("weekday_label")["cnt"]
            .mean()
            .reindex([w for w in weekday_order if w in filtered_day["weekday_label"].unique()])
        )
        fig6, ax6 = plt.subplots(figsize=(7, 4.2))
        bar_colors = ["#1565C0" if w not in ["Sat","Sun"] else "#E53935" for w in weekday_avg.index]
        bars6 = ax6.bar(weekday_avg.index, weekday_avg.values,
                        color=bar_colors, width=0.6, edgecolor="white", linewidth=0.8)
        for bar, val in zip(bars6, weekday_avg.values):
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                     f"{val:,.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
        from matplotlib.patches import Patch
        ax6.legend(handles=[Patch(color="#1565C0", label="Hari Kerja"),
                             Patch(color="#E53935", label="Akhir Pekan")],
                   fontsize=8)
        ax6.set_xlabel("Hari", fontsize=9)
        ax6.set_ylabel("Rata-rata Penyewaan", fontsize=9)
        ax6.spines["top"].set_visible(False)
        ax6.spines["right"].set_visible(False)
        ax6.tick_params(labelsize=9)
        plt.tight_layout()
        st.pyplot(fig6)
        plt.close()

    # ── Scatter Plot Suhu vs Penyewaan ────────────────────────────────────────
    st.markdown("**Hubungan Suhu dengan Total Penyewaan Harian**")
    if not filtered_day.empty:
        fig7, ax7 = plt.subplots(figsize=(12, 4))
        season_colors_sc = {"Spring": "#FFA726", "Summer": "#66BB6A",
                            "Fall": "#EF5350", "Winter": "#42A5F5"}
        for season in filtered_day["season_label"].unique():
            sub = filtered_day[filtered_day["season_label"] == season]
            ax7.scatter(sub["temp_celsius"], sub["cnt"],
                        color=season_colors_sc.get(season, "gray"),
                        alpha=0.55, s=28, label=season)
        if len(filtered_day) > 2:
            z = np.polyfit(filtered_day["temp_celsius"], filtered_day["cnt"], 1)
            p = np.poly1d(z)
            x_line = np.linspace(filtered_day["temp_celsius"].min(),
                                 filtered_day["temp_celsius"].max(), 100)
            ax7.plot(x_line, p(x_line), color="black", linewidth=1.5,
                     linestyle="--", alpha=0.8, label="Trendline")
            r = filtered_day["temp_celsius"].corr(filtered_day["cnt"])
            ax7.text(0.02, 0.95, f"r = {r:.3f}", transform=ax7.transAxes,
                     fontsize=10, verticalalignment="top",
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        ax7.set_xlabel("Suhu (°C)", fontsize=10)
        ax7.set_ylabel("Total Penyewaan Harian", fontsize=10)
        ax7.legend(fontsize=9, loc="upper left")
        ax7.spines["top"].set_visible(False)
        ax7.spines["right"].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig7)
        plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Analisis Lanjutan
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-hdr">🔬 Analisis Lanjutan: Clustering Performa Penyewaan (Binning)</div>',
                unsafe_allow_html=True)
    st.markdown(
        "Hari-hari penyewaan dikelompokkan ke dalam empat klaster performa menggunakan teknik "
        "**manual binning berbasis kuartil** tanpa algoritma machine learning."
    )

    # Hitung klaster untuk filtered_day
    if not filtered_day.empty and len(filtered_day) >= 4:
        q1f = filtered_day["cnt"].quantile(0.25)
        q2f = filtered_day["cnt"].quantile(0.50)
        q3f = filtered_day["cnt"].quantile(0.75)
        bins_f  = [0, q1f, q2f, q3f, filtered_day["cnt"].max() + 1]
        lbls_f  = ["Low", "Medium", "High", "Very High"]
        fd = filtered_day.copy()
        fd["perf_cluster"] = pd.cut(fd["cnt"], bins=bins_f, labels=lbls_f, right=True,
                                    duplicates="drop")

        col_cl1, col_cl2 = st.columns(2)

        # ── Distribusi klaster ────────────────────────────────────────────────
        with col_cl1:
            st.markdown("**Distribusi Klaster Performa**")
            cluster_dist = fd["perf_cluster"].value_counts().reindex(lbls_f).fillna(0)
            cluster_colors = ["#EF5350", "#FFA726", "#66BB6A", "#42A5F5"]
            fig8, ax8 = plt.subplots(figsize=(5.5, 4))
            bars8 = ax8.bar(cluster_dist.index, cluster_dist.values,
                            color=cluster_colors, width=0.55, edgecolor="white")
            for bar, val in zip(bars8, cluster_dist.values):
                ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                         f"{int(val)}", ha="center", va="bottom", fontsize=10, fontweight="bold")
            ax8.set_xlabel("Klaster Performa", fontsize=9)
            ax8.set_ylabel("Jumlah Hari", fontsize=9)
            ax8.spines["top"].set_visible(False)
            ax8.spines["right"].set_visible(False)
            ax8.tick_params(labelsize=9)
            plt.tight_layout()
            st.pyplot(fig8)
            plt.close()

        # ── Profil klaster ────────────────────────────────────────────────────
        with col_cl2:
            st.markdown("**Profil Karakteristik per Klaster**")
            profile = fd.groupby("perf_cluster", observed=True).agg(
                Hari        = ("cnt", "count"),
                Rata2_Cnt   = ("cnt", "mean"),
                Suhu_C      = ("temp_celsius", "mean"),
                Kelembapan  = ("hum_pct", "mean"),
            ).round(1).reindex(lbls_f).dropna()
            profile.columns = ["Jumlah Hari", "Rata-rata Cnt", "Suhu (°C)", "Kelembapan (%)"]
            st.dataframe(profile, use_container_width=True)

        # ── Komposisi musim per klaster ───────────────────────────────────────
        st.markdown("**Komposisi Musim per Klaster Performa**")
        if not fd.empty:
            pivot_cl = pd.crosstab(fd["perf_cluster"], fd["season_label"]).reindex(lbls_f).fillna(0)
            season_c = {"Fall": "#E65100", "Spring": "#43A047", "Summer": "#FB8C00", "Winter": "#1E88E5"}
            fig9, ax9 = plt.subplots(figsize=(9, 4))
            bottom = np.zeros(len(pivot_cl))
            for season in ["Spring", "Summer", "Fall", "Winter"]:
                if season in pivot_cl.columns:
                    values = pivot_cl[season].values
                    ax9.bar(pivot_cl.index, values, bottom=bottom,
                            color=season_c.get(season, "gray"), label=season,
                            alpha=0.85, edgecolor="white")
                    bottom += values
            ax9.set_xlabel("Klaster Performa", fontsize=9)
            ax9.set_ylabel("Jumlah Hari", fontsize=9)
            ax9.legend(title="Musim", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
            ax9.spines["top"].set_visible(False)
            ax9.spines["right"].set_visible(False)
            ax9.tick_params(labelsize=9)
            plt.tight_layout()
            st.pyplot(fig9)
            plt.close()
    else:
        st.warning("Data tidak cukup untuk clustering. Coba perluas filter.")

    st.markdown(
        '<div class="insight-box">'
        "💡 <strong>Insight:</strong> Klaster <em>Very High</em> didominasi oleh hari-hari di musim "
        "Fall dan Summer dengan suhu rata-rata ~24°C. Klaster <em>Low</em> banyak terjadi di musim "
        "Spring dan Winter dengan suhu rata-rata ~11°C. Suhu adalah prediktor kuat performa penyewaan."
        "</div>",
        unsafe_allow_html=True,
    )

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#9E9E9E; font-size:0.82rem;'>"
    "🚲 Bike Sharing Dashboard | Muhammad Vikri Mustafa | "
    "Proyek Akhir Belajar Analisis Data dengan Python — Dicoding 2024"
    "</div>",
    unsafe_allow_html=True,
)
