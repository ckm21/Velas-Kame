import streamlit as st
import json
from funciones import (
    obtener_datos_accion,
    analizar_velas_japonesas,
    mostrar_grafico_candlestick,
    calcular_porcentaje_ganancia
)

# Cargar configuración
with open("config.json", "r") as f:
    config = json.load(f)

usuario = config.get("usuario", "ejemplo")
modo = config.get("modo", "demo")

st.title("📈 Sistema de Señales por Velas Japonesas")
st.markdown("Bienvenido a la aplicación de análisis de acciones basada en velas japonesas.")
st.markdown(f"**Usuario:** {usuario} | **Modo:** {modo}")

# Semillero
st.subheader("🌱 Semillero de Inversiones")
st.info("Acciones con pequeñas inversiones activas a largo plazo.")

# Objetivos del usuario
st.subheader("🎯 Objetivos del Usuario")
meta = st.slider("Define tu meta de ganancia (%)", 1, 20, config.get("objetivo_semanal", 5))
if meta < 5:
    st.success("Buen objetivo.")
elif meta < 10:
    st.warning("Objetivo moderado.")
else:
    st.error("🚨 ¿Te crees el lobo de Wall Street?")
st.markdown(f"**Tu objetivo semanal:** {meta}%")

# Portafolio
st.subheader("📊 Mi Portafolio")
st.info("Aquí podrás ver tus acciones favoritas, ganancias y estado general.")

acciones = config.get("acciones_favoritas", [])
for accion in acciones:
    datos = obtener_datos_accion(accion)
    senal = analizar_velas_japonesas(datos)
    ganancia = calcular_porcentaje_ganancia(accion)
    st.write(f"📌 {accion} | Señal: {senal} | Ganancia: {ganancia}%")
    mostrar_grafico_candlestick(datos, accion)