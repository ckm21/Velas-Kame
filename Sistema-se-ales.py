import streamlit as st
from funciones import obtener_datos, generar_grafico, detectar_senales
import json

st.set_page_config(page_title="Velas Kame", layout="wide")

# Cargar configuración de usuario
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"favoritas": [], "inversiones": {}, "objetivos": {}, "perfil_riesgo": "moderado"}

# Sidebar
st.sidebar.title("📊 Velas Kame")
menu = st.sidebar.radio("Ir a:", ["Análisis de Acción", "Mi Portafolio", "Objetivos"])

# ----- MÓDULO DE ANÁLISIS -----
if menu == "Análisis de Acción":
    st.title("🔍 Análisis Técnico de Acciones")
    ticker = st.text_input("Símbolo de la acción (ej. AAPL, NVDA):")
    periodo = st.selectbox("Intervalo de velas:", ["15m", "1h", "4h", "1d", "1w"], index=3)

    if ticker:
        df = obtener_datos(ticker, periodo)
        if df is not None:
            fig = generar_grafico(df, ticker)
            st.plotly_chart(fig, use_container_width=True)

            senales = detectar_senales(df)
            if senales["compra"]:
                st.success("✅ Señal de COMPRA detectada")
            if senales["venta"]:
                st.error("⚠️ Señal de VENTA detectada")
            if senales["doji"]:
                st.warning("⚠️ Doji detectado - posible indecisión")

            # Opciones
            if st.button("Agregar a favoritas"):
                if ticker not in config["favoritas"]:
                    config["favoritas"].append(ticker)

            if st.button("Registrar inversión"):
                monto = st.number_input("Monto invertido ($)", min_value=1.0)
                precio = st.number_input("Precio de entrada", min_value=0.01)
                config["inversiones"][ticker] = {"monto": monto, "precio_entrada": precio}

# ----- MÓDULO DE PORTAFOLIO -----
elif menu == "Mi Portafolio":
    st.title("💼 Mi Portafolio")

    favoritas = config.get("favoritas", [])
    inversiones = config.get("inversiones", {})

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⭐ Favoritas")
        for fav in favoritas:
            st.write(fav)
            if st.button(f"❌ Quitar {fav}", key=f"del_{fav}"):
                config["favoritas"].remove(fav)

    with col2:
        st.subheader("📈 Inversiones Activas")
        total_ganancia = 0
        for ticker, data in inversiones.items():
            df = obtener_datos(ticker, "1d")
            if df is not None and not df.empty:
                precio_actual = df["Close"].iloc[-1]
                ganancia = ((precio_actual - data["precio_entrada"]) / data["precio_entrada"]) * 100
                total_ganancia += ganancia
                st.metric(label=f"{ticker}", value=f"{ganancia:.2f}%", delta=f"${precio_actual:.2f}")

    st.markdown("### 📊 Semillero (solo favoritas sin inversión)")
    semillero = [x for x in favoritas if x not in inversiones]
    for s in semillero:
        st.write(s)

# ----- MÓDULO DE OBJETIVOS -----
elif menu == "Objetivos":
    st.title("🎯 Objetivos de Ganancia")
    tipo_obj = st.radio("Frecuencia del objetivo", ["Diario", "Semanal", "Mensual"])
    objetivo = st.slider("Meta de ganancia (%)", 1, 20, 3)
    perfil = st.selectbox("Perfil de riesgo", ["bajo", "moderado", "alto"])

    config["objetivos"][tipo_obj.lower()] = objetivo
    config["perfil_riesgo"] = perfil

    st.success(f"Objetivo {tipo_obj.lower()} establecido en {objetivo}% con perfil {perfil}")

    if objetivo <= 2:
        st.info("🟢 Meta alcanzable")
    elif objetivo <= 5:
        st.warning("🟠 Meta moderada")
    else:
        st.error("🔴 ¿Te crees el lobo de Wall Street?")

# Guardar cambios en config
with open("config.json", "w") as f:
    json.dump(config, f)
