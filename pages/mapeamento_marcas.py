import streamlit as st
import pandas as pd
from utils.db_connection import conectar_bd

def consulta_coluna_sql(conn):
    """Função para executar a consulta SQL e retornar a coluna 'name' da tabela."""
    try:
        query = "SELECT name FROM manufacturer_manufacturer mm;"
        df_sql = pd.read_sql(query, conn)
        return df_sql
    except Exception as e:
        st.error(f"Erro ao executar a consulta: {e}")
        return None

def main():
    st.title("Comparação de Colunas - DataFrame e Banco de Dados")

    # Verifica se o DataFrame foi carregado na sessão
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return

    df = st.session_state.df

    # Verifica se a coluna 'brand' está presente no DataFrame
    if 'brand' not in df.columns:
        st.warning("A coluna 'brand' não foi encontrada no DataFrame.")
        return

    # Verifica e avisa sobre linhas vazias na coluna 'brand'
    if df['brand'].isnull().any():
        st.warning("Existem linhas vazias na coluna 'brand', elas serão ignoradas na ordenação.")

    # Remove linhas vazias e ordena a coluna 'brand'
    brand_sorted = df['brand'].dropna().unique()
    brand_sorted.sort()

    # Solicita as credenciais do banco de dados
    st.subheader("Credenciais do Banco de Dados")
    host = st.text_input("URL ou IP do Banco", value="localhost")
    port = st.text_input("Porta", value="5433")
    database = st.text_input("Nome do Banco")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Conectar e Consultar"):
        try:
            conn = conectar_bd(host, port, database, user, password)
            df_sql = consulta_coluna_sql(conn)
            conn.close()

            if df_sql is not None:
                # Verifica e avisa sobre linhas vazias na coluna 'name' da consulta SQL
                if df_sql['name'].isnull().any():
                    st.warning("Existem linhas vazias na coluna 'name' da consulta SQL, elas serão ignoradas na ordenação.")

                # Remove linhas vazias e ordena a coluna 'name' da consulta SQL
                name_sorted = df_sql['name'].dropna().unique()
                name_sorted.sort()

                # Exibe as duas colunas lado a lado
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Coluna 'brand' do DataFrame:**")
                    st.write(brand_sorted)
                with col2:
                    st.write("**Coluna 'name' da consulta SQL:**")
                    st.write(name_sorted)
        except Exception as e:
            st.error(e)

if __name__ == "__main__":
    main()