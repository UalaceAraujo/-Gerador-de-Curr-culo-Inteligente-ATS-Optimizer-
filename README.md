# ATS Resume Optimizer

Aplicativo web desenvolvido em Streamlit que extrai texto de currículos em múltiplos formatos (PDF, Word, TXT) e utiliza a inteligência artificial do Google Gemini para otimizar e adaptar o perfil do candidato diretamente aos requisitos de uma vaga de emprego específica.

## Funcionalidades

- **Upload Universal:** Suporte para arquivos em formato PDF, DOCX e TXT.
- **Análise Inteligente por IA:** Integração com a API do Google Gemini para cruzamento cirúrgico de palavras-chave e competências.
- **Garantia de ATS:** Reestruturação de currículos focada em passar pelos sistemas automatizados de triagem (Applicant Tracking Systems).
- **Interface Intuitiva:** Painel limpo e responsivo construído em Python com Streamlit.

## Tecnologias Utilizadas

- **Python** (Ambiente virtual isolado via `.venv`)
- **Streamlit** (Interface gráfica web)
- **Google GenAI SDK** (`gemini-3.8-flash`)
- **PyPDF** e **Python-Docx** (Processamento de documentos)

## Instalação e Execução Local

Siga os passos abaixo para clonar e rodar o projeto na sua máquina:

1. Clone o repositório:
   ```bash
   git clone [https://github.com/UalaceAraujo/gerador_curriculo.git](https://github.com/UalaceAraujo/gerador_curriculo.git)
   cd gerador_curriculo