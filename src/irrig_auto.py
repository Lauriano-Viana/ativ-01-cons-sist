import random
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import boto3

import boto3

def enviar_sms_sns(mensagem, numero_telefone):
    client = boto3.client(
        'sns',
        region_name='us-east-2',
        aws_access_key_id='AKIAXN7S2VTMRBEWAVL5',
        aws_secret_access_key='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'
    )
    response = client.publish(
        PhoneNumber=numero_telefone,
        Message=mensagem
    )
    return response



def simular_leitura_sensor():
    return {
        "umidade": round(random.uniform(10, 80), 2),
        "ph": round(random.uniform(5.5, 7.5), 2),
        "temperatura": round(random.uniform(18, 35), 2),
        "p": round(random.uniform(5, 40), 2),
        "k": round(random.uniform(5, 50), 2)
    }

def avaliar_irrigacao(leitura):
    motivo = []
    if leitura["umidade"] < 30:
        motivo.append("Umidade baixa")
    if leitura["ph"] < 6.0:
        motivo.append("pH ácido")
    if leitura["temperatura"] > 30:
        motivo.append("Temperatura alta")
    if leitura["p"] < 10:
        motivo.append("Fósforo baixo")
    if leitura["k"] < 15:
        motivo.append("Potássio baixo")
    irrigar = len(motivo) > 0
    return irrigar, motivo

def irrig_ia(): 
    # Inicialização de variáveis de sessão
    if "mostrar_historico" not in st.session_state:
        st.session_state.mostrar_historico = False
    if "historico_leituras" not in st.session_state:
        st.session_state.historico_leituras = []

    st.subheader("🚀 Simulador de Irrigação Inteligente (Fase 3)")

    st.markdown("### 📄 Sobre o Sistema")
    st.markdown("""
    Este sistema simula a irrigação automatizada com base em sensores que monitoram:
    - Umidade do solo
    - Nutrientes (Fósforo - P, Potássio - K)
    - pH
    - Temperatura

    O objetivo é **otimizar o uso de água** e garantir o melhor crescimento das plantas.
    """)

    st.markdown("### 🔎 Coleta e Análise de Dados")
    st.markdown("""
    Os dados são coletados por sensores simulados e processados para decidir se a irrigação é necessária. A decisão é baseada em regras simples:
    - Umidade abaixo de 30%
    - pH abaixo de 6.0
    - Temperatura acima de 30°C
    - P < 10 ou K < 15
    """)

    # Botão de simulação
    if st.button("📡 Simular Leitura dos Sensores"):
        leitura = simular_leitura_sensor()
        irrigar, motivo = avaliar_irrigacao(leitura)
        leitura_registrada = {
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **leitura,
            "irrigar": "Sim" if irrigar else "Não",
            "motivo": ", ".join(motivo) if irrigar else "-"
        }

        st.session_state.historico_leituras.append(leitura_registrada)

        st.markdown("### 📈 Leitura Simulada")
        st.json(leitura)

        st.markdown("### 💧 Decisão de Irrigação")
        mensagem_sms = f"""
            [ALERTA SENSOR]
            Leitura em: {leitura_registrada['data_hora']}
            Umidade: {leitura['umidade']}%
            pH: {leitura['ph']}
            Temperatura: {leitura['temperatura']}°C
            P: {leitura['p']}, K: {leitura['k']}
            Irrigar: {leitura_registrada['irrigar']}
            Motivo: {leitura_registrada['motivo']}
            """
        telefone_destino = "+5586988282470"  # seu número verificado no formato internacional

        try:
            enviar_sms_sns(mensagem_sms, telefone_destino)
            st.success("📲 SMS enviado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao enviar SMS: {e}")

        if irrigar:
            st.success("🚿 Irrigação Ativada!")
            for m in motivo:
                st.write(f"- {m}")
        else:
            st.info("✅ Irrigação não necessária.")
       
    st.markdown("---")

    # Botão para mostrar ou esconder histórico
    st.session_state.mostrar_historico = st.checkbox("📊 Mostrar Histórico de Leituras", value=st.session_state.mostrar_historico)

    if st.session_state.mostrar_historico and st.session_state.historico_leituras:
        df_hist = pd.DataFrame(st.session_state.historico_leituras)

        st.markdown("### 📋 Histórico de Leituras")
        st.dataframe(df_hist, use_container_width=True)

        st.markdown("### 📊 Gráfico: Umidade ao longo do tempo")
        fig = px.line(df_hist, x="data_hora", y="umidade", markers=True, title="Umidade do Solo")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 💾 Exportar Leitura para CSV")
        csv_data = df_hist.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar arquivo CSV",
            data=csv_data,
            file_name="leituras_sensores.csv",
            mime="text/csv"
        )
    else:
        st.info("ℹ️ Nenhuma leitura registrada ainda. Clique no botão acima para iniciar.")

    st.markdown("---")
    st.markdown("### 📦 Tabelas e Fluxo de Dados")
    st.markdown("""
    - **leituras**: recebe os dados coletados pelos sensores.
    - **culturas**: define os níveis ideais de cada cultura.
    - **irrigacoes**: registra as ações de irrigação com base nas leituras.

    Cada nova **leitura** gera automaticamente uma nova **irrigação**, se necessário.
    """)


