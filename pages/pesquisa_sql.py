import streamlit as st
import pandas as pd
import sqlite3
from utils.auth import check_login

check_login()

if 'df' not in st.session_state or st.session_state.df is None:
    st.warning("Por favor, carregue um arquivo CSV na página principal para continuar.")
else:
    df = st.session_state.df  # Referência ao DataFrame carregado na sessão

def pesquisa_sql():
    st.title("Pesquisa SQL no DataFrame")

    st.text("Exemplo de consulta SQL:")
    st.code("SELECT * FROM df WHERE height > 10")
    st.text("'df' é o nome da tabela que contém o DataFrame carregado.")
    st.text("Verifique o nome das colunas na página 'Visualização de Dados'.")
    st.text("Evite realizar modificações no DataFrame com comandos SQL. Para isso utilize a página de 'Correção de Outliers'.")
    
    # Caixa de texto para a consulta SQL
    sql_query = st.text_area("Digite sua consulta SQL:", "")

    if st.button("Executar SQL"):
        if sql_query.strip():
            try:
                # Conectar ao banco SQLite em memória
                conn = sqlite3.connect(':memory:')
                # Carregar o DataFrame na tabela SQLite
                df.to_sql('df', conn, index=False, if_exists='replace')

                # Executar a consulta SQL
                resultado = pd.read_sql(sql_query, conn)

                # Exibir o resultado da consulta
                st.write("Resultado da consulta:")
                st.dataframe(resultado)
                
                # Fechar a conexão após a consulta
                conn.close()

            except Exception as e:
                st.error(f"Erro ao executar a consulta: {e}")
        else:
            st.warning("Por favor, insira um comando SQL.")

pesquisa_sql()
