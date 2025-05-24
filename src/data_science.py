import streamlit as st
import pandas as pd
import numpy as np
import datetime
import joblib
import time
import plotly.express as px

def dt_science():
    # Importa a classe do sistema
    from irrig_preditiva import SmartIrrigationSystem

    # Inicializa o sistema de irrigação
    sistema = SmartIrrigationSystem()

    
    # Carrega modelo e scaler
    try:
        modelo = joblib.load("irrigacao_modelo.pkl")
        scaler = joblib.load("irrigacao_scaler.pkl")
        st.sidebar.success("Modelo carregado com sucesso!")
    except FileNotFoundError:
        st.sidebar.error("Modelo não encontrado. Treine o modelo antes de usar o dashboard.")

    

    # Caminho do arquivo de dados
    data_file = "leituras.csv"

    # Função para carregar dados
    @st.cache_data
    def carregar_dados():
        try:
            return pd.read_csv(data_file)
        except FileNotFoundError:
            return pd.DataFrame(columns=['leit_p', 'leit_k', 'leit_ph', 'leit_umidade', 'leit_temperatura', 'data_leitura'])

    

    def visualizar_dados():
        st.subheader("📊 Visualizar Dados Coletados")

        # Exibe a tabela de dados
        if not dados.empty:
            st.write(f"📂 Dados mais recentes coletados ({len(dados)} leituras):")
            st.dataframe(dados.tail(10))

            # Gráficos interativos com Plotly
            st.subheader("Gráficos")
            col1, col2 = st.columns(2)

            with col1:
                fig_umidade = px.line(dados, x='data_leitura', y='leit_umidade', title='Variação da Umidade do Solo')
                st.plotly_chart(fig_umidade, use_container_width=True)

            with col2:
                fig_temperatura = px.line(dados, x='data_leitura', y='leit_temperatura', title='Variação da Temperatura')
                st.plotly_chart(fig_temperatura, use_container_width=True)

            # Histogramas
            st.subheader("Distribuição de Variáveis")
            variavel = st.selectbox("Selecione uma variável", ['leit_ph', 'leit_umidade', 'leit_temperatura'])
            fig_hist = px.histogram(dados, x=variavel, title=f"Distribuição de {variavel}")
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível. Execute o monitoramento para coletar dados.")

    def previsao_tempo_real():
        st.subheader("🔮 Previsão em Tempo Real")
        

        # Simula dados do sensor
        st.write("Coletando dados do sensor...")
        dados_sensores = sistema.coletar_dados_sensores()
        st.write("Dados coletados:")
        st.json(dados_sensores)

        # Gera previsão usando o modelo carregado
        if modelo and scaler:
            try:
                features = ['leit_p', 'leit_k', 'leit_ph', 'leit_temperatura']
                dados_array = np.array([
                    dados_sensores['leit_p'],
                    dados_sensores['leit_k'],
                    dados_sensores['leit_ph'],
                    dados_sensores['leit_temperatura']
                ]).reshape(1, -1)

                dados_array_scaled = scaler.transform(dados_array)
                umidade_prevista = modelo.predict(dados_array_scaled)[0]

                # Exibe a previsão e recomendação
                st.write("📈 Previsão do Modelo:")
                st.write(f"Umidade prevista: {umidade_prevista:.2f}%")
                if umidade_prevista < sistema.UMIDADE_IDEAL:
                    tempo_irrigacao = int((sistema.UMIDADE_IDEAL - umidade_prevista) * 10)
                    st.success(f"✅ Irrigação recomendada por {min(tempo_irrigacao, 300)} segundos.")
                else:
                    st.info("💧 Solo com umidade suficiente. Irrigação não necessária.")

            except Exception as e:
                st.error(f"Erro ao gerar previsão: {e}")
        else:
            st.warning("Modelo e scaler não estão carregados. Treine ou carregue os arquivos.")

    def train_model():
        st.subheader("🎯 Treinar Modelo")
        if not dados.empty:
            if st.button("Treinar Modelo"):
                sistema.treinar_modelo()
                st.success("Modelo treinado e salvo com sucesso!")
        else:
            st.warning("Nenhum dado disponível para treinar o modelo.")

    dados = carregar_dados()
    visualizar_dados()
    previsao_tempo_real()
    train_model()
   
