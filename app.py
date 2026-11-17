# =====================================================================
# APP.PY - Interface Web Profissional com Leitor Universal de Arquivos
# =====================================================================
import streamlit as st
from ai_engine import analisar_e_otimizar_curriculo
from pdf_generator import gerar_pdf_curriculo
from base_master import CURRICULO_BASE
import io

# Leitor de PDF
from pypdf import PdfReader
# Leitor de Word (.docx)
from docx import Document

st.set_page_config(
    page_title="Gerador de Currículo Inteligente | ATS Optimizer",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilização visual limpa e profissional
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        padding: 0.6rem;
    }
    .stButton>button:hover { background-color: #1D4ED8; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Gerador de Currículo Inteligente (ATS Optimizer)")
st.markdown("Envie o seu currículo atual em **qualquer formato (PDF, Word, TXT)**, cole a vaga desejada e deixe a IA otimizá-lo para os robôs de ATS!")

st.divider()

# =====================================================================
# FUNÇÃO PARA EXTRAIR TEXTO DE QUALQUER ARQUIVO
# =====================================================================
def extrair_texto_arquivo(uploaded_file):
    extensao = uploaded_file.name.split(".")[-1].lower()
    texto_extraido = ""
    
    try:
        if extensao == "pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                texto_extraido += page.extract_text() or ""
                
        elif extensao == "docx":
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                texto_extraido += para.text + "\n"
                
        elif extensao in ["txt", "md"]:
            texto_extraido = uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        
    return texto_extraido

# =====================================================================
# BARRA LATERAL: UPLOAD DO CURRÍCULO DO USUÁRIO
# =====================================================================
st.sidebar.header("📁 Seu Currículo Base")
st.sidebar.markdown("Envie o seu currículo em **PDF, Word (.docx) ou Texto** para servir de base.")

arquivo_usuario = st.sidebar.file_uploader("Escolha o arquivo:", type=["pdf", "docx", "txt", "md"])

texto_base_utilizado = CURRICULO_BASE # Padrão caso nenhum arquivo seja enviado

if arquivo_usuario is not None:
    with st.spinner("Lendo o seu arquivo..."):
        texto_lido = extrair_texto_arquivo(arquivo_usuario)
        if texto_lido.strip():
            texto_base_utilizado = texto_lido
            st.sidebar.success(f"✅ Arquivo '{arquivo_usuario.name}' lido com sucesso!")
        else:
            st.sidebar.warning("⚠️ Não conseguimos extrair texto desse arquivo. Usando a base padrão.")

st.sidebar.divider()
st.sidebar.markdown("💡 **Dica:** O sistema extrai todo o conteúdo do seu arquivo e cruza as informações de forma cirúrgica com a vaga.")

# =====================================================================
# CORPO PRINCIPAL: ENTRADA DA VAGA
# =====================================================================
st.subheader("🎯 Descrição da Vaga")
descricao_vaga = st.text_area(
    "Cole os requisitos e detalhes da vaga (LinkedIn, Gupy, etc.):",
    placeholder="Ex: Buscamos estagiário em desenvolvimento backend com Java, Spring Boot...",
    height=220
)

if st.button("🚀 Gerar Currículo Otimizado", type="primary"):
    if not descricao_vaga.strip():
        st.warning("⚠️ Por favor, cole a descrição de uma vaga antes de continuar.")
    else:
        with st.spinner("🤖 A IA está analisando a vaga e otimizando o seu currículo..."):
            try:
                # 1. Roda a IA passando o texto extraído do arquivo do usuário
                resultado_analise = analisar_e_otimizar_curriculo(texto_base_utilizado, descricao_vaga)
                
                # 2. Gera o PDF formatado ATS-Friendly
                nome_pdf = "curriculo_otimizado_ia.pdf"
                gerar_pdf_curriculo(resultado_analise, nome_pdf)
                
                st.success("✅ Currículo otimizado gerado com sucesso!")
                
                # Exibe o relatório de análise
                st.markdown("---")
                st.subheader("📊 Relatório de Análise e Ajustes da IA")
                st.markdown(resultado_analise)
                
                st.markdown("---")
                # Botão de Download
                with open(nome_pdf, "rb") as file:
                    st.download_button(
                        label="📥 Baixar Currículo Otimizado em PDF",
                        data=file,
                        file_name="Curriculo_Otimizado.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao processar: {e}")