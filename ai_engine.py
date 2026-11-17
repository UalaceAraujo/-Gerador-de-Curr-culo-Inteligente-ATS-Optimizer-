# =====================================================================
# AI ENGINE - Lógica de Comunicação com o Gemini (Seguro)
# =====================================================================
import os
from google import genai

# Puxa a chave de forma segura do ambiente do seu sistema ou do Streamlit
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_e_otimizar_curriculo(texto_curriculo_base: str, descricao_vaga: str):
    prompt = f"""
    Você é um especialista em ATS (Applicant Tracking System) e recrutamento tech.
    Abaixo está o currículo base de um candidato e a descrição de uma vaga de emprego.

    --- CURRICULO BASE DO CANDIDATO ---
    {texto_curriculo_base}

    --- DESCRIÇÃO DA VAGA ---
    {descricao_vaga}

    --- INSTRUÇÕES ---
    1. Selecione e reorganize APENAS as informações do currículo base que dão match direto com os requisitos da vaga.
    2. Reescreva o Resumo Profissional focando nas palavras-chave exigidas pela vaga.
    3. Identifique 2 ou 3 "gaps" (requisitos da vaga que o candidato ainda não tem explicitamente).
    
    Retorne a resposta estritamente no seguinte formato de texto limpo para gerar o currículo:
    === RESUMO OTIMIZADO ===
    (texto do resumo focado na vaga)
    === COMPETÊNCIAS SELECIONADAS ===
    (lista de competências que dão match)
    === PROJETOS E EXPERIÊNCIAS DESTAQUE ===
    (experiências e projetos mais relevantes para esta vaga)
    === GAPS E SUGESTÕES DE ESTUDO ===
    (o que estudar para futuros processos desta área)
    """

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    
    return response.text