# =====================================================================
# PDF GENERATOR - Criação do arquivo PDF formatado
# =====================================================================
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def gerar_pdf_curriculo(conteudo_otimizado: str, nome_arquivo="curriculo_otimizado.pdf"):
    """
    Compila o texto otimizado pela IA em um PDF limpo de coluna única.
    """
    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    estilo_titulo = ParagraphStyle(
        'TituloCustom',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=10
    )
    
    estilo_cabecalho_secao = ParagraphStyle(
        'SecaoCustom',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=12,
        spaceAfter=6
    )
    
    estilo_corpo = ParagraphStyle(
        'CorpoCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    story = []
    
    # Cabeçalho fixo com meus contatos
    story.append(Paragraph("Ualace de Araújo Serra", estilo_titulo))
    story.append(Paragraph("Araraquara, SP | (16) 99623-7503 | ualacearaujo@hotmail.com", estilo_corpo))
    story.append(Paragraph("linkedin.com/in/ualacearaujo | github.com/UalaceAraujo", estilo_corpo))
    story.append(Spacer(1, 10))

    # Processando o texto da IA linha por linha
    linhas = conteudo_otimizado.split("\n")
    for linha in linhas:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
        
        if linha_limpa.startswith("==="):
            story.append(Spacer(1, 6))
            story.append(Paragraph(linha_limpa.replace("=", "").strip(), estilo_cabecalho_secao))
        else:
            story.append(Paragraph(linha_limpa, estilo_corpo))

    doc.build(story)
    return nome_arquivo