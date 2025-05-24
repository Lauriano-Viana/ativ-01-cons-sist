# detect_imgs_streamlit.py
import streamlit as st
from ultralytics import YOLO
import os
import glob
from PIL import Image
from pathlib import Path
import shutil

# --- Função para Detecção de Imagens com YOLOv8 ---
# Esta função treina um modelo YOLOv8 e executa a detecção em imagens de teste.
import streamlit as st
from ultralytics import YOLO
import os
import glob
from PIL import Image
from pathlib import Path
import shutil

def detect_imgs_yolov8():
    st.title("📦 Detecção de Imagens com YOLOv8")

    # Caminhos
    YAML_PATH = '/home/lauriano/Documentos/FIAP/MACHINE-LEARNING/FASE-07/ativ-01-cons-sist/assets/detect_img.yaml'
    TEST_IMAGES_PATH = '/home/lauriano/Documentos/FIAP/MACHINE-LEARNING/FASE-07/ativ-01-cons-sist/assets/test'
    RUNS_PATH = '/home/lauriano/Documentos/FIAP/MACHINE-LEARNING/FASE-07/ativ-01-cons-sist/runs/detect'

    # Limpa a pasta de imagens de teste
    if os.path.exists(TEST_IMAGES_PATH):
        shutil.rmtree(TEST_IMAGES_PATH)

    # Cria pastas se necessário
    Path(TEST_IMAGES_PATH).mkdir(parents=True, exist_ok=True)
    Path(RUNS_PATH).mkdir(parents=True, exist_ok=True)

    def get_latest_train_run_folder():
        if not os.path.exists(RUNS_PATH):
            return None
        subfolders = [f.path for f in os.scandir(RUNS_PATH) if f.is_dir()]
        if not subfolders:
            return None
        subfolders.sort(key=os.path.getctime, reverse=True)
        return subfolders[0]

    def train_model():
        model = YOLO('yolov8s.pt')
        with st.spinner("Treinando o modelo..."):
            results = model.train(
                data=YAML_PATH,
                imgsz=320,
                epochs=45,
                batch=16,
                device='0'
            )
        st.success("✅ Treinamento concluído!")
        return results

    def detect_images():
        latest_run = get_latest_train_run_folder()
        if not latest_run:
            st.error("Nenhuma pasta de treino encontrada.")
            return

        model_path = os.path.join(latest_run, 'weights', 'best.pt')
        if not os.path.exists(model_path):
            st.error(f"Modelo não encontrado: {model_path}")
            return

        try:
            model = YOLO(model_path)
        except RuntimeError as e:
            st.error(f"Erro ao carregar o modelo:\n{e}")
            return

        with st.spinner("Executando detecção nas imagens de teste..."):
            results = model.predict(
                source=TEST_IMAGES_PATH,
                imgsz=320,
                conf=0.25,
                save=True,
                save_txt=True,
                save_conf=True,
                exist_ok=True
            )

        st.success("✅ Detecção concluída!")
        display_detected_images()
        gerar_relatorio_basico(results, model)

    def display_detected_images():
        latest_run = get_latest_train_run_folder()
        pred_folder = os.path.join(latest_run, 'predict')
        # if not os.path.exists(pred_folder):
        #     st.warning("Nenhuma imagem detectada encontrada.")
        #     return

        image_files = sorted(glob.glob(os.path.join(pred_folder, '*.jpg')))
        st.subheader("📸 Imagens com Detecções")

        for img_path in image_files:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(Image.open(img_path), width=200)
            with col2:
                st.write(f"**Arquivo:** {os.path.basename(img_path)}")

    def gerar_relatorio_basico(results, model):
        st.subheader("📊 Relatório Básico das Detecções")

        classes_detectadas = set()
        for result in results:
            nome_imagem = os.path.basename(result.path)
            boxes = result.boxes

            if not boxes or len(boxes) == 0:
                st.write(f"🖼 **{nome_imagem}**: Nenhum objeto detectado.")
                continue

            confs = boxes.conf.tolist()
            ids = boxes.cls.tolist()
            nomes_classes = [model.names[int(i)] for i in ids]
            media_conf = sum(confs) / len(confs)

            for c in nomes_classes:
                classes_detectadas.add(c)

            st.write(f"🖼 **{nome_imagem}**")
            st.write(f"→ Classes detectadas: {', '.join(nomes_classes)}")
            st.write(f"→ Total de objetos: {len(nomes_classes)}")
            st.write(f"→ Confiança média: **{media_conf*100:.1f}%**")
            st.markdown("---")

        if classes_detectadas:
            st.subheader("✅ Classes Totais Detectadas")
            st.write(f"{', '.join(sorted(classes_detectadas))}")
        else:
            st.warning("Nenhuma classe foi detectada.")

    # --- Interface ---
    st.markdown("### ⬆️ Upload de Imagens de Teste")
    uploaded_files = st.file_uploader("Envie imagens para detecção", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        for file in os.listdir(TEST_IMAGES_PATH):
            os.remove(os.path.join(TEST_IMAGES_PATH, file))

        for file in uploaded_files:
            dest_path = os.path.join(TEST_IMAGES_PATH, file.name)
            with open(dest_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"✅ {len(uploaded_files)} imagem(ns) enviada(s) com sucesso!")

    st.divider()
    st.markdown("### 🔧 Ações disponíveis")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Executar Detecção nas Imagens de Teste"):
            detect_images()
    with col2:
        if st.button("▶️ Treinar Modelo YOLOv8"):
            train_model()
