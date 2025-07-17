
import streamlit as st
from funciones import *

st.set_page_config(page_title="Velas Kame", layout="wide")

menu = st.sidebar.selectbox("Menú", ["Inicio", "Mi portafolio", "Radar de Oportunidades", "Resumen"])

if menu == "Inicio":
    mostrar_inicio()

elif menu == "Mi portafolio":
    mostrar_portafolio()

elif menu == "Radar de Oportunidades":
    mostrar_radar()

elif menu == "Resumen":
    mostrar_resumen()
