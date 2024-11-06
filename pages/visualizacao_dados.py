import streamlit as st
from utils.auth import check_login

check_login()

def exibir_visualizacao_dados():
    st.title("Visualização de Dados")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return

    df = st.session_state.df
    st.text(f"Número total de (linhas, colunas): {df.shape}")

    intervalo = st.text_input('Digite o intervalo de linhas (ex: 0-20)', '0-20')
    df_exibir = None

    try:
        inicio, fim = map(int, intervalo.split('-'))
        if 0 <= inicio < fim <= len(df):
            df_exibir = df.iloc[inicio:fim]
        else:
            st.error('Intervalo inválido')
    except ValueError:
        st.error('Formato de intervalo inválido. Use o formato início-fim.')

    st.dataframe(df_exibir)

# Chama a função principal da página
exibir_visualizacao_dados()
