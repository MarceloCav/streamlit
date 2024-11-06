import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from utils.data_validation import verifica_dimensoes_invalidas, verifica_codigos_malformados, valida_colunas
from pages.estatisticas import exibir_graficos
from utils.auth import check_login

check_login()

def exibir_relatorio():
    st.title("Gerar Relatório em PDF")

    # Verifica se o DataFrame foi carregado
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return

    df = st.session_state.df

    # Define colunas obrigatórias e opcionais para validação
    obrigatorias = ['search_ref', 'manufacturer_ref', 'name']
    opcionais = [
        'barcode', 'ncm', 'application', 'net_weight', 'gross_weight', 'born_at', 'deprecated_at', 'manufacturer', 
        'catalog_id', 'height', 'width', 'length', 'url_thumb', 'notes', 'file_high', 'file_low', 
        'file_medium', 'file_water_mark', 'position'
    ]

    # Valida colunas e verifica erros nos dados
    colunas_faltantes, colunas_erradas = valida_colunas(df, obrigatorias, opcionais)
    dimensoes_invalidas, _ = verifica_dimensoes_invalidas(df)
    codigos_malformados, _ = verifica_codigos_malformados(df)

    # Gera o relatório PDF ao clicar no botão
    if st.button("Gerar Relatório PDF"):
        # Cria um buffer para o relatório PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Cabeçalho do relatório
        p.setFont("Helvetica-Bold", 16)
        p.drawString(30, height - 30, "Relatório de Catálogo de Peças Automotivas")
        p.setFont("Helvetica", 12)
        p.drawString(30, height - 50, "Este relatório contém informações sobre o arquivo CSV analisado.")

        # Informações Gerais
        p.setFont("Helvetica-Bold", 14)
        p.drawString(30, height - 80, "Informações Gerais:")
        p.setFont("Helvetica", 12)
        p.drawString(30, height - 100, f"Total de peças no catálogo: {len(df)}")
        p.drawString(30, height - 120, f"Colunas obrigatórias faltando: {', '.join(colunas_faltantes) if colunas_faltantes else 'Nenhuma'}")
        p.drawString(30, height - 140, f"Colunas não reconhecidas: {', '.join(colunas_erradas) if colunas_erradas else 'Nenhuma'}")

        # Erros nos Dados
        p.setFont("Helvetica-Bold", 14)
        p.drawString(30, height - 170, "Erros nos Dados:")
        p.setFont("Helvetica", 12)
        p.drawString(30, height - 190, f"Peças com dimensões inválidas: {len(dimensoes_invalidas)}")
        p.drawString(30, height - 210, f"Peças com códigos malformados: {len(codigos_malformados)}")

        # Finaliza e salva o relatório PDF
        p.showPage()
        p.save()

        # Configura o buffer para download
        buffer.seek(0)
        st.download_button(
            label="Baixar Relatório PDF",
            data=buffer,
            file_name="relatorio_catalogo_pecas.pdf",
            mime="application/pdf"
        )
        

# Chama a função principal da página
exibir_relatorio()
