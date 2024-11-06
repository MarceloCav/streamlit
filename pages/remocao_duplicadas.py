# pages/resolucao_duplicadas.py
import streamlit as st
import pandas as pd
from utils.auth import check_login

check_login()

# Função para exibir e resolver duplicados com base em 'search_ref' e 'brand'
def resolver_duplicatas(df):
    if 'search_ref' not in df.columns or 'brand' not in df.columns:
        st.warning("As colunas 'search_ref' e 'brand' são necessárias para verificar duplicatas.")
        return

    # Filtrando duplicatas com base em 'search_ref' e 'brand'
    duplicados = df[df.duplicated(subset=['search_ref', 'brand'], keep=False)]

    if duplicados.empty:
        st.info("Nenhuma duplicata encontrada com base nas colunas 'search_ref' e 'brand'.")
        return

    # Exibindo duplicatas encontradas
    st.write("## Linhas duplicadas encontradas")
    st.write("As seguintes linhas têm valores duplicados nas colunas 'search_ref' e 'brand'.")
    st.dataframe(duplicados[['search_ref', 'manufacturer_ref', 'brand'] + [col for col in duplicados.columns if col not in ['search_ref', 'manufacturer_ref', 'brand']]])

    # Botão para remover duplicatas
    if st.button("Remover Duplicadas"):
        # Mantém apenas o primeiro registro de cada duplicata
        df.drop_duplicates(subset=['search_ref', 'brand'], keep='first', inplace=True)
        st.success("Duplicatas removidas com sucesso!")
        st.experimental_rerun()  # Recarrega a página para atualizar o dataframe

# Função principal para carregar o dataframe e verificar duplicatas
def main():
    st.title("🔄 Resolução de Duplicatas")
    
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Por favor, carregue um arquivo CSV na página principal para acessar essa funcionalidade.")
    else:
        resolver_duplicatas(st.session_state.df)

main()
