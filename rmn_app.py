import streamlit as st
import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from io import BytesIO

def plot_spectrum(picos, graph_color, x_range=None):
    x_total = np.arange(0, 15.001, 0.001)
    y_total = np.zeros_like(x_total)

    for pico in picos:
        centro = pico[1]
        intensidade = pico[2]
        mask = (x_total >= centro - 0.05) & (x_total <= centro + 0.05)
        y_lorentziana = np.zeros_like(x_total)
        y_lorentziana[mask] = intensidade / (1 + ((x_total[mask] - centro) / 0.001)**2)
        y_total += y_lorentziana

    # Criar o gráfico com Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_total, y=y_total, mode='lines', line=dict(color=graph_color)))

    # Invertendo o eixo x
    fig.update_layout(
        xaxis=dict(title='Deslocamento Químico (ppm)', range=[15, 0], showgrid=True, ticks='outside'),
        yaxis=dict(title='Intensidade', showgrid=True, ticks='outside'),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return fig, x_total, y_total

def create_matplotlib_plot(x_total, y_total, graph_color, x_range=None):
    fig, ax = plt.subplots()
    ax.plot(x_total, y_total, color=graph_color)
    ax.set_xlim(x_range if x_range else (15, 0))  # Manter o eixo invertido no matplotlib
    ax.set_xlabel("Deslocamento Químico (ppm)")
    ax.set_ylabel("Intensidade")
    ax.grid(True)
    ax.tick_params(direction='in', length=6, width=2)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Streamlit Interface
st.title('Gerador de Espectro de RMN com Integração de Picos')

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

# Opções de cor limitadas
color_options = {
    "Preta": "black",
    "Verde": "green",
    "Azul": "blue",
    "Vermelha": "red"
}

# Definir a cor default como preta
color_choice = st.selectbox("Escolha a cor do gráfico", options=list(color_options.keys()), index=0)
graph_color = color_options[color_choice]

# Plotar o espectro com Plotly
if picos:
    fig, x_total, y_total = plot_spectrum(picos, graph_color)
    plotly_chart = st.plotly_chart(fig, use_container_width=True)

    # Botão para capturar a imagem do gráfico
    if st.button("Copiar gráfico como imagem"):
        try:
            x_range = fig.layout.xaxis.range  # Capturar a área de zoom atual
            img_buf = create_matplotlib_plot(x_total, y_total, graph_color, x_range=x_range)
            st.download_button(label="Baixar imagem", data=img_buf, file_name="grafico_rmn.png", mime="image/png")
        except Exception as e:
            st.error(f"Erro ao gerar a imagem: {e}")
