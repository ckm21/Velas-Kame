
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

acciones_favoritas = st.session_state.get("favoritas", [])
inversiones = st.session_state.get("inversiones", [])

def mostrar_inicio():
    st.title("Bienvenido a Velas Kame")
    st.markdown("Sistema de señales basado en velas japonesas y análisis técnico adaptado para centennials y millennials.")

def mostrar_portafolio():
    st.header("Mi portafolio")
    favoritas = st.session_state.get("favoritas", [])
    if favoritas:
        st.subheader("Acciones favoritas")
        st.write(", ".join(favoritas))
    else:
        st.info("Aún no has seleccionado acciones favoritas.")

def mostrar_radar():
    st.header("Radar de Oportunidades")
    ticker = st.text_input("Ingresa un ticker (ej. AAPL)")
    if ticker:
        df = yf.download(ticker, period="7d", interval="1h")
        if not df.empty:
            st.line_chart(df["Close"])
            st.success("Análisis técnico cargado.")
        else:
            st.warning("No se pudo obtener la información.")

def mostrar_resumen():
    st.header("Resumen general")
    st.markdown("Aquí podrás ver un resumen de tus objetivos, ganancias y desempeño.")
