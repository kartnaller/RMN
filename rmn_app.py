import streamlit as st
import numpy as np
import plotly.graph_objs as go

def plot_spectrum(picos, graph_color):
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

    fig.add_trace(go.Scatter(
        x=x_total, 
        y=y_total, 
        mode='lines', 
        line=dict(color=graph_color, width=2)
    ))

    # Customizar a aparência
    fig.update_layout(
        plot_bgcolor='white',  # Fundo branco
        xaxis=dict(
            title='Deslocamento Químico (ppm)', 
            range=[15, 0], 
            ticks='outside', 
            showline=True, 
            linecolor='black', 
            tickcolor='black'
        ),
        yaxis=dict(
            title='Intensidade', 
            ticks='outside', 
            showline=True, 
            linecolor='black', 
            tickcolor='black'
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=40)
    )

    return fig

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
    fig = plot_spectrum(picos, graph_color)
    st.plotly_chart(fig, use_container_width=True)
