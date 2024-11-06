import streamlit as st
from utils.data_processing import gerar_search_ref, gerar_born_deprecated_at
from utils.auth import check_login

check_login()

def exibir_colunas_automatizadas():
    st.title("Criação de Colunas Automatizadas")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return

    df = st.session_state.df
    
    if 'search_ref' not in df.columns:
            if st.button("Gerar 'search_ref'"):
                df = gerar_search_ref(df)
                st.success("Coluna 'search_ref' gerada com sucesso!")
                st.dataframe(df[['manufacturer_ref', 'search_ref']].head())
    else:
        st.success("A coluna 'search_ref' foi encontrada")

    if 'applications' in df.columns:
        if 'born_at' not in df.columns or 'deprecated_at' not in df.columns:
            if st.button("Gerar 'born_at' e 'deprecated_at'"):
                df, error_logs = gerar_born_deprecated_at(df)
                if error_logs:
                    st.error("\n".join(error_logs))
                st.success("Colunas 'born_at' e 'deprecated_at' geradas com sucesso!")
                st.dataframe(df[['born_at', 'deprecated_at']].head())
    else:
        st.warning("A coluna 'applications' é necessária para gerar 'born_at' e 'deprecated_at'.")


# Chama a função principal da página
exibir_colunas_automatizadas()
