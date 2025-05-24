import streamlit as st
import math
import pandas as pd


def calculos_insumos():
    st.subheader("📐 Cálculo de Área & Insumos")

    culturas = ["Milho", "Feijão","Cana-de-açúcar"]
    cultura = st.selectbox("Escolha a cultura", culturas)
    idx = culturas.index(cultura)

    formato_area = st.radio("Formato da área", ["Retangular", "Circular"])

    if formato_area == "Retangular":
        largura = st.number_input("Largura da área (m)", min_value=1.0)
        comprimento = st.number_input("Comprimento da área (m)", min_value=1.0)
        area = largura * comprimento
    else:
        raio = st.number_input("Raio da área (m)", min_value=1.0)
        area = math.pi * (raio ** 2)

    st.write(f"🌿 Área de cultivo estimada: **{area:.2f} m²**")

    largura_rua = st.number_input("Largura da rua (m)", min_value=0.5)

    if formato_area == "Retangular":
        medida = st.selectbox("Escolha a dimensão para as ruas", ["Comprimento", "Largura"])
        ref = comprimento if medida == "Comprimento" else largura
        num_ruas = int((ref / largura_rua) / 2)
        area_ruas = (ref/2)* num_ruas * largura_rua
    else:
        perimetro = 2 * math.pi * raio
        num_ruas = int((perimetro / largura_rua) / 2)
        area_ruas = num_ruas * largura_rua

    st.write(f"🚜 Ruas estimadas: **{num_ruas}**")
    st.write(f"📏 Área ocupada por ruas: **{area_ruas:.2f} m²**")

    st.markdown("---")
    st.subheader("💧 Cálculo de Insumos")

    produto = st.text_input("Nome do insumo", value="Fosfato")
    quantidade_m2 = st.number_input("Quantidade por m² (mL)", min_value=0.0)
    total_aplicado = quantidade_m2 * (area - area_ruas)

    st.write(f"💡 Total estimado de insumo: **{total_aplicado:.2f} Litros**")

    if st.button("Salvar cálculo"):
        st.success(f"{produto} registrado para {cultura}: {total_aplicado:.2f} L")
