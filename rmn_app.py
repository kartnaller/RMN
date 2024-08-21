import streamlit as st
import numpy as np
import plotly.graph_objs as go

def lorentziana(x, centro, intensidade, largura=0.001):
    return intensidade * (largura**2 / ((x - centro)**2 + largura**2))

def plot_spectrum(picos, graph_color):
    x_total = np.arange(0, 15.001, 0.001)
    y_total = np.zeros_like(x_total)

    for pico in picos:
        centro = pico[1]
        intensidade = pico[2]
        mask = (x_total >= centro - 0.05) & (x_total <= centro + 0.05)
        y_lorentziana = np.zeros_like(x_total)
        y_lorentziana[mask] = lorentziana(x_total[mask], centro, intensidade)
        y_total += y_lorentziana

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_total, y=y_total, mode='lines', line=dict(color=graph_color)))
    fig.update_layout(
        xaxis=dict(title='Deslocamento Químico (ppm)', range=[15, 0]),  # Inverted x-axis
        yaxis=dict(title='Intensidade'),
        title='Espectro de RMN Somado',
    )
    return fig

# Streamlit Interface
st.title('Gerador de Espectro de RMN')

# Input data
data = st.text_area("Entre com os dados (Hz, ppm, Int)", "")
picos = []

if data:
    lines = data.splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            try:
                hz = float(parts[0])
                ppm = float(parts[1])
                intensity = float(parts[2])
                picos.append((hz, ppm, intensity))
            except ValueError:
                continue

# Color picker for the graph
graph_color = st.color_picker("Escolha a cor do gráfico", "#FFA500")

if picos:
    fig = plot_spectrum(picos, graph_color)
    st.plotly_chart(fig, use_container_width=True)
