import yfinance as yf
import plotly.graph_objects as go

def obtener_datos(ticker, intervalo="1d"):
    try:
        periodo = "7d" if intervalo in ["15m", "1h", "4h"] else "3mo"
        df = yf.download(ticker, period=periodo, interval=intervalo, progress=False)
        return df
    except Exception as e:
        print("Error al obtener datos:", e)
        return None

def generar_grafico(df, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Velas"
    )])
    fig.update_layout(title=f"Gráfico de {ticker}", xaxis_title="Fecha", yaxis_title="Precio")
    return fig

def detectar_senales(df):
    senales = {"compra": False, "venta": False, "doji": False}
    if df is None or len(df) < 2:
        return senales

    vela = df.iloc[-1]
    cuerpo = abs(vela["Close"] - vela["Open"])
    mecha = vela["High"] - vela["Low"]

    if cuerpo < 0.1 * mecha:
        senales["doji"] = True
    elif vela["Close"] > vela["Open"]:
        senales["compra"] = True
    elif vela["Close"] < vela["Open"]:
        senales["venta"] = True

    return senales
