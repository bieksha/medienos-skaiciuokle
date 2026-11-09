import streamlit as st
import traceback

st.set_page_config(page_title="Medienos Skaičiuoklė", layout="wide", page_icon="🪵")

st.title("🪵 JUNDA Universali Medienos Skaičiuoklė (v1)")

# ---------------------------------------------------------
# GLOBALUS KLAIDŲ PAGAVIMAS (TRY / EXCEPT + ST.STOP)
# ---------------------------------------------------------
try:
    WOOD_SPECIES = {
        "Ąžuolas": {
            "Šviežiai kirsta (~75%)": 1000,
            "Transportinė (~20%)": 730,
            "Orsaūsė (~18%)": 710,
            "Statybinė (~15%)": 690,
            "Džiovykla (8-15%)": 670,
        },
        "Uosis": {
            "Šviežiai kirsta (~75%)": 950,
            "Transportinė (~20%)": 720,
            "Orsaūsė (~18%)": 700,
            "Statybinė (~15%)": 680,
            "Džiovykla (8-15%)": 660,
        },
        "Juodalksnis": {
            "Šviežiai kirsta (~75%)": 800,
            "Transportinė (~20%)": 560,
            "Orsaūsė (~18%)": 540,
            "Statybinė (~15%)": 520,
            "Džiovykla (8-15%)": 500,
        },
        "Pušis": {
            "Šviežiai kirsta (~75%)": 850,
            "Transportinė (~20%)": 550,
            "Orsaūsė (~18%)": 530,
            "Statybinė (~15%)": 510,
            "Džiovykla (8-15%)": 490,
        },
        "Eglė": {
            "Šviežiai kirsta (~75%)": 800,
            "Transportinė (~20%)": 490,
            "Orsaūsė (~18%)": 470,
            "Statybinė (~15%)": 460,
            "Džiovykla (8-15%)": 440,
        },
        "Liepa": {
            "Šviežiai kirsta (~75%)": 780,
            "Transportinė (~20%)": 530,
            "Orsaūsė (~18%)": 510,
            "Statybinė (~15%)": 490,
            "Džiovykla (8-15%)": 470,
        },
    }

    st.sidebar.header("⚙️ Medienos Savybės")
    species = st.sidebar.selectbox("Pasirinkite medienos rūšį", list(WOOD_SPECIES.keys()))
    moisture = st.sidebar.selectbox("Pasirinkite drėgnumą", list(WOOD_SPECIES[species].keys()))

    custom_density = st.sidebar.number_input(
        "Tankis (kg/m³)",
        value=WOOD_SPECIES[species][moisture],
        step=10,
        help="Tankis atnaujinamas automatiškai pagal rūšį ir drėgnumą, bet galite koreguoti rankiniu būdu."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Įvesties režimas (ką norite įvesti?):**")
    input_mode = st.sidebar.radio(
        "Pagrindinis įvesties kintamasis:",
        ["Gaminio matmenys + Kiekis (vnt)", "Norimas tūris (m³)", "Norimas bendras ilgis (m)", "Norimas plotas (m²)"]
    )

    st.header("1. Gaminio Skerspjūvis ir Ilgis")
    col_dim1, col_dim2, col_dim3 = st.columns(3)

    with col_dim1:
        storis_mm = st.number_input("Storis (mm)", min_value=1.0, value=32.0, step=1.0)
    with col_dim2:
        plotis_mm = st.number_input("Plotis (mm)", min_value=1.0, value=100.0, step=1.0)
    with col_dim3:
        ilgis_m = st.number_input("Vieno elemento ilgis (m)", min_value=0.1, value=6.0, step=0.5)

    storis_m = storis_mm / 1000.0
    plotis_m = plotis_mm / 1000.0
    vieno_vnt_m3 = storis_m * plotis_m * ilgis_m
    vieno_vnt_m2 = plotis_m * ilgis_m
    turis_1m_m3 = storis_m * plotis_m

    st.markdown("---")
    st.header("2. Manipuliacija ir Kintamųjų Įvestis")

    total_vnt = 0.0
    total_m = 0.0
    total_m2 = 0.0
    total_m3 = 0.0

    if input_mode == "Gaminio matmenys + Kiekis (vnt)":
        total_vnt = st.number_input("Kiekis (vnt)", min_value=1.0, value=365.0, step=1.0)
        total_m = total_vnt * ilgis_m
        total_m3 = total_vnt * vieno_vnt_m3
        total_m2 = total_vnt * vieno_vnt_m2

    elif input_mode == "Norimas tūris (m³)":
        total_m3 = st.number_input("Bendras tūris (m³)", min_value=0.001, value=7.0, step=0.1)
        total_vnt = total_m3 / vieno_vnt_m3
        total_m = total_vnt * ilgis_m
        total_m2 = total_vnt * vieno_vnt_m2

    elif input_mode == "Norimas bendras ilgis (m)":
        total_m = st.number_input("Bendras ilgis (m)", min_value=0.1, value=2190.0, step=10.0)
        total_vnt = total_m / ilgis_m
        total_m3 = total_m * turis_1m_m3
        total_m2 = total_m * plotis_m

    elif input_mode == "Norimas plotas (m²)":
        total_m2 = st.number_input("Bendras plotas (m²)", min_value=0.1, value=219.0, step=1.0)
        total_vnt = total_m2 / vieno_vnt_m2
        total_m = total_vnt * ilgis_m
        total_m3 = total_m2 * storis_m

    total_svoris_kg = total_m3 * custom_density
    total_svoris_t = total_svoris_kg / 1000.0

    st.markdown("---")
    st.header("📊 Visi Apskaičiuoti Rezultatai")

    m1, m2, m3_col, m4, m5, m6 = st.columns(6)

    m1.metric("Kiekis (vnt)", f"{total_vnt:,.1f} vnt")
    m2.metric("Bendras ilgis (m)", f"{total_m:,.2f} m")
    m3_col.metric("Plotas (m²)", f"{total_m2:,.2f} m²")
    m4.metric("Tūris (m³)", f"{total_m3:,.4f} m³")
    m5.metric("Svoris (kg)", f"{total_svoris_kg:,.1f} kg")
    m6.metric("Svoris (tonos)", f"{total_svoris_t:,.3f} t")

    st.markdown("### 📋 Išsamios Specifikacijos Suvestinė")
    st.table({
        "Parametras": [
            "Medienos rūšis",
            "Drėgnumo būsena",
            "Skaičiuojamasis tankis",
            "Vieno vnt. matmenys (S x P x I)",
            "Vieno vnt. tūris",
            "Vieno vnt. dengiamas plotas",
            "1 bėginio metro tūris",
            "Kiekis vnt.",
            "Bendras ilgis",
            "Bendras plotas",
            "Bendras tūris",
            "Bendras svoris (kg)",
            "Bendras svoris (tonos)"
        ],
        "Reikšmė": [
            species,
            moisture,
            f"{custom_density} kg/m³",
            f"{storis_mm:.0f} x {plotis_mm:.0f} x {ilgis_m:.2f} m",
            f"{vieno_vnt_m3:.6f} m³",
            f"{vieno_vnt_m2:.4f} m²",
            f"{turis_1m_m3:.6f} m³",
            f"{total_vnt:,.2f} vnt (suapvalinus: {round(total_vnt)} vnt)",
            f"{total_m:,.2f} m",
            f"{total_m2:,.2f} m²",
            f"{total_m3:,.4f} m³",
            f"{total_svoris_kg:,.2f} kg",
            f"{total_svoris_t:,.3f} t"
        ]
    })

except Exception as e:
    # Stabdymas ir saugus klaidos rodymas ekrane
    st.error("🚨 **ĮVYKO KLAIDA! SKAIČIAVIMAS SUSTABDYTAS:**")
    st.exception(e)
    st.markdown("### 🔍 Traceback Detalės:")
    st.code(traceback.format_exc(), language="python")
    st.stop()
