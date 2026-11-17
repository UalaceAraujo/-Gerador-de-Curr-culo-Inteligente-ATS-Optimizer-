# =====================================================================
# GERADOR DE CURRÍCULOS COM IA (Versão Projeto Pessoal / Portfólio)
# =====================================================================
# Fala, pessoal! Esse é um projetinho que criei para resolver uma dor real:
# o cansaço de ficar reescrevendo o currículo toda vez que acho uma vaga 
# nova. Aqui a ideia é automatizar o processo usando Python e a IA do Gemini
# para fazer o "match" do meu perfil com a vaga e ainda me gerar um PDF limpo.
# =====================================================================

import os
from google import genai
from google.genai import types
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ---------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA CHAVE DA API
# ---------------------------------------------------------------------
# Aqui a gente puxa a chave da API do Gemini direto das variáveis de ambiente
# do computador. É o jeito mais seguro para não deixar chave exposta no código.
# Para configurar no terminal: export GEMINI_API_KEY="sua-chave"
client = genai.Client()

# ---------------------------------------------------------------------
# 2. A MINHA "BASE MASTER" (O currículo raiz)
# ---------------------------------------------------------------------
# Esse é o meu "banco de dados" pessoal em texto. Tem tudo o que eu já fiz:
# faculdade na UNIP, experiências em logística (Copling), meus projetos 
# do GitHub (Assistente com IA, TCC, WMS) e meus certificados. 
# A IA vai ler isso aqui e escolher só o que importa para a vaga do dia.
CURRICULO_BASE = """
Nome: Ualace de Araújo Serra
Localização: Araraquara, SP
Objetivo: Estágio em Desenvolvimento Backend (Java) ou QA
Formação: Bacharelado em Ciência da Computação - Universidade Paulista (UNIP) (Previsão: Junho/2027)

Experiência Profissional:
- Almoxarife / Controle de Estoque na Fábrica de Máquinas Copling Ltda (2024-2026): Auditoria cíclica de inventário, conferência de notas fiscais e validação de dados.
- Auxiliar de Logística e Expedição na Empresa Tratamentos em Metais Copling (2022-2024): Conferência técnica de componentes e controle operacional de remessas.

Competências Técnicas:
- Linguagens: Java, Python, SQL, TypeScript.
- Backend & Frameworks: Spring Boot, Spring Data, Spring Security, APIs RESTful, Maven.
- Qualidade & Boas Práticas: Testes de Unidade, Validação de APIs, Tratamento de Exceções, SOLID, Clean Code, Design Patterns.
- Bancos de Dados: SQL Server, SQLite, H2 Database.
- Ferramentas: Git, GitHub, Docker, Postman.

Projetos Técnicos (GitHub):
- Assistente Financeiro com IA: API em Java (Spring Boot e Spring AI) para processamento de transações.
- Sistema de Recomendação de Locais (TCC - MyVicinity): Sistema web em desenvolvimento usando dados geográficos abertos (OpenStreetMap).
- WMS Enterprise: Sistema desktop em Python (PyQt6, SQLite) para controle de inventário e rastreabilidade inspirado na vivência de almoxarifado.

Certificações:
- Bootcamp CI&T - Java AI Copilot (53h)
- Bootcamp NTT DATA - Backend Java com Spring AI (54h)
- Bootcamp Itaú - Java com Inteligência Artificial (45h)
"""

# ---------------------------------------------------------------------
# 3. O CÉREBRO DA IA (Enviando a vaga e o currículo para o Gemini)
# ---------------------------------------------------------------------
def analisar_e_otimizar_curriculo(descricao_vaga: str):
    """
    Essa função pega a descrição da vaga que eu colei, junta com o meu 
    currículo base e manda para o modelo do Gemini analisar. 
    O objetivo é fazer a IA reescrever o foco do currículo para aquela vaga 
    específica e ainda me dar dicas do que falta estudar (gaps).
    """
    print("\n[🤖 IA] Mandando a vaga para o Gemini analisar e cruzar com o meu perfil...")
    
    # Montando o prompt (as instruções que dou para a IA)
    prompt = f"""
    Você é um especialista em ATS (Applicant Tracking System) e recrutamento tech.
    Abaixo está o currículo base de um candidato e a descrição de uma vaga de emprego.

    --- CURRICULO BASE DO CANDIDATO ---
    {CURRICULO_BASE}

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

    # Chamando o modelo de IA do Google (usando o gemini-2.5-flash que é rápido e ótimo para texto)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text

# ---------------------------------------------------------------------
# 4. GERADOR DE PDF (Deixando o currículo pronto para os robôs de ATS)
# ---------------------------------------------------------------------
def gerar_pdf_curriculo(conteudo_otimizado: str, nome_arquivo="curriculo_otimizado.pdf"):
    """
    Aqui entra a biblioteca ReportLab. Como os robôs de ATS (tipo Gupy) 
    odeiam tabelas malucas e colunas duplas, criei um layout super limpo, 
    de coluna única, para garantir que o sistema leia tudo sem bugar.
    """
    print(f"\n[📄 PDF] Compilando o texto otimizado em um PDF limpo: {nome_arquivo}...")
    
    # Configurando o documento (tamanho carta e margens seguras)
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Criando meus próprios estilos de texto (cores corporativas e fontes limpas)
    estilo_titulo = ParagraphStyle(
        'TituloCustom',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"), # Azul escuro profissional
        spaceAfter=10
    )
    
    estilo_cabecalho_secao = ParagraphStyle(
        'SecaoCustom',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"), # Azul médio
        spaceBefore=12,
        spaceAfter=6
    )
    
    estilo_corpo = ParagraphStyle(
        'CorpoCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"), # Cinza escuro para leitura confortável
        spaceAfter=6
    )

    story = []
    
    # Cabeçalho fixo com meus contatos (sempre visível no topo)
    story.append(Paragraph("Ualace de Araújo Serra", estilo_titulo))
    story.append(Paragraph("Araraquara, SP | (16) 99623-7503 | ualacearaujo@hotmail.com", estilo_corpo))
    story.append(Paragraph("linkedin.com/in/ualacearaujo | github.com/UalaceAraujo", estilo_corpo))
    story.append(Spacer(1, 10))

    # Pegando o texto que a IA gerou e jogando linha por linha no PDF
    linhas = conteudo_otimizado.split("\n")
    for linha in linhas:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
        
        # Se a linha começar com "===", significa que é um título de seção da IA
        if linha_limpa.startswith("==="):
            story.append(Spacer(1, 6))
            story.append(Paragraph(linha_limpa.replace("=", "").strip(), estilo_cabecalho_secao))
        else:
            story.append(Paragraph(linha_limpa, estilo_corpo))

    # Cria o arquivo PDF de verdade na pasta
    doc.build(story)
    print(f"[✅ SUCESSO] Currículo gerado e salvo com sucesso como '{nome_arquivo}'!")

# ---------------------------------------------------------------------
# 5. ONDE A MÁGICA ACONTECE (Função Principal)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("=== GERADOR DE CURRÍCULOS COM IA (MEU PROJETO DE PORTFÓLIO) ===")
    
    # Simulo aqui colando o texto de uma vaga que achei no LinkedIn
    descricao_vaga_exemplo = """
    Buscamos Estagiário em Desenvolvimento Backend Java. 
    Requisitos: Cursando Ciência da Computação ou áreas afins, 
    conhecimento em Java, Spring Boot, APIs RESTful, SQL e controle de versão Git.
    Diferencial: Noções de testes automatizados e arquitetura de microsserviços.
    """
    
    print("\n[💡] Simulando a leitura de uma vaga de Estágio Java...")
    
    # Passo 1: Peço para a IA analisar a vaga e ajustar meu currículo
    resultado_ia = analisar_e_otimizar_curriculo(descricao_vaga_exemplo)
    
    print("\n--- O QUE A IA AJUSTOU PARA ESTA VAGA ---")
    print(resultado_ia)
    print("------------------------------------------")
    
    # Passo 2: Pego esse resultado formatado e transformo em PDF prontinho para envio
    gerar_pdf_curriculo(resultado_ia, "curriculo_estagio_java.pdf")