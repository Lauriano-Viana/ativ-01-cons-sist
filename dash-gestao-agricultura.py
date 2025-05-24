import streamlit as st
import pandas as pd
import os
from src.irrig_auto import *
from src.base_dados_coleta import calculos_insumos
from src.estruturacao_dados import estrutura_dados
from src.data_science import dt_science
from src.detect_images import detect_imgs_yolov8



# Inicializa o histórico se não existir
if "historico_leituras" not in st.session_state:
    st.session_state.historico_leituras = []

st.set_page_config(page_title="Dashboard de Agricultura Inteligente", layout="wide")

st.title("🌾 Dashboard de Gestão Agrícola Inteligente")

with st.sidebar:
    st.header("🔍 Navegação por Fase")
    fase = st.radio("Escolha uma fase:", [
    "1. Base de Dados e Coleta",
    "2. Estruturação dos Dados",
    "3. IoT & Automação",
    "4. Data Science",
    "5. Visão Computacional",
    
])

if fase == "1. Base de Dados e Coleta":
    calculos_insumos()

elif fase == "2. Estruturação dos Dados":
    estrutura_dados()
   
elif fase == "3. IoT & Automação":
    irrig_ia()
    
elif fase == "4. Data Science":
    dt_science()
    
elif fase == "5. Visão Computacional":
    detect_imgs_yolov8()   


# Rodapé opcional
st.markdown("---")
st.caption("Desenvolvido para monitoramento e tomada de decisão agrícola com tecnologias inteligentes.")

