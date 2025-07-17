import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import datetime

def obtener_datos_accion(ticker):
    try:
        data = yf.download(ticker, period="7d", interval="1h")
        return data
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return pd.DataFrame()

def analizar_velas_japonesas(data):
    if data.empty or len(data) < 2:
        return "Sin datos"
    candle = data.iloc[-1]
    cuerpo = abs(candle["Close"] - candle["Open"])
    mecha_superior = candle["High"] - max(candle["Close"], candle["Open"])
    mecha_inferior = min(candle["Close"], candle["Open"]) - candle["Low"]
    if cuerpo < mecha_superior and cuerpo < mecha_inferior:
        return "Doji - indecisión"
    elif candle["Close"] > candle["Open"]:
        return "Posible compra"
    elif candle["Close"] < candle["Open"]:
        return "Posible venta"
    return "Sin señal clara"

def mostrar_grafico_candlestick(data, ticker):
    if data.empty:
        return
    fig, ax = plt.subplots()
    data["Color"] = data["Close"] >= data["Open"]
    for i in range(len(data)):
        color = "green" if data["Color"].iloc[i] else "red"
        ax.plot([i, i], [data["Low"].iloc[i], data["High"].iloc[i]], color="black")
        ax.add_patch(plt.Rectangle((i-0.2, min(data["Open"].iloc[i], data["Close"].iloc[i])),
                                   0.4, abs(data["Close"].iloc[i] - data["Open"].iloc[i]), color=color))
    ax.set_title(f"Velas Japonesas: {ticker}")
    st.pyplot(fig)

def calcular_porcentaje_ganancia(ticker):
    try:
        data = yf.download(ticker, period="2d")
        if len(data) < 2:
            return 0
        precio_ayer = data["Close"].iloc[0]
        precio_hoy = data["Close"].iloc[-1]
        return round(((precio_hoy - precio_ayer) / precio_ayer) * 100, 2)
    except:
        return 0