import streamlit as st

def estrutura_dados( ):
    
    st.markdown("### 🧾 Descrição das Tabelas")

    st.markdown("""
    - **CULTURA**: Guarda os dados básicos sobre cada tipo de cultura (ex: Milho, Feijão).
    - **AREA**: Representa uma área de plantio, vinculada a uma cultura e com tamanho definido.
    - **APLICACAO**: Registra cada aplicação de insumos (fertilizantes, defensivos), informando área, tipo, quantidade e data.
    - **SENSOR**: Tabela de sensores físicos instalados (ex: DHT22, sensores de pH), com tipo e localização.
    - **LEITURA**: Captura as medições feitas pelos sensores, como umidade, nutrientes, temperatura, data e hora.
    - **LEITURA_AREA**: Relaciona as leituras com as áreas específicas de plantio.

    ### 🔗 Relacionamentos
    - Uma **CULTURA** pode ter várias **ÁREAS**.
    - Uma **AREA** pode ter várias **APLICACOES** e **LEITURAS** associadas.
    - As **LEITURAS** são feitas por **SENSORES** e são vinculadas a uma **AREA** por meio da tabela intermediária **LEITURA_AREA**.
    - Esse modelo garante integridade, rastreabilidade e base sólida para decisões automatizadas.
    """)

    st.subheader("📊 Modelo Relacional - Banco de Dados Estruturado (Fase 2)")

    st.image("/home/lauriano/Documentos/FIAP/MACHINE-LEARNING/FASE-07/ativ-01-cons-sist/assets/images/DER.png", caption="Modelo Relacional da Fase 2",use_container_width=True)
    st.markdown("---")

    st.info("Este modelo permite a integração e organização eficiente dos dados coletados e aplicados no campo.")

