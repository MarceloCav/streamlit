import streamlit as st
import pandas as pd
from utils.auth import check_login

# Configuração da página deve ser a primeira chamada
st.set_page_config(layout="wide", page_title="Dashboard de Catálogo de Peças Automotivas", initial_sidebar_state="expanded")

def init_session_state(uploaded_file):
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
    elif 'df' not in st.session_state:
        st.session_state.df = None

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    
    if st.sidebar.button("Login"):
        # Usuários e senhas
        users = {"admin": {"password": "adminpass", "role": "admin"},
                 "worker": {"password": "workerpass", "role": "worker"}}
        
        user = users.get(username)
        if user and user["password"] == password:
            st.session_state.user = {"username": username, "role": user["role"]}
            st.sidebar.success(f"Bem-vindo, {username}!")
        else:
            st.sidebar.error("Usuário ou senha incorretos.")

if 'user' not in st.session_state:
    login()  # Chama a função de login se o usuário não estiver logado
else:
    if st.sidebar.button("Logout"):
        st.session_state.pop("user", None)  # Permite que o usuário faça logout

    st.title("📊 Dashboard de Catálogo de Peças Automotivas")
    st.subheader("Simplificando a visualização, validação e correção de seus dados.")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV para visualizar e editar", type="csv", label_visibility="visible")
    init_session_state(uploaded_file)

    if st.session_state.df is None:
        st.warning("Para visualizar as funcionalidades, por favor, carregue um arquivo CSV acima.")
    else:
        st.success("##### O arquivo foi carregado com sucesso. Navegue nas páginas laterais para ver as funcionalidades.")

        csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📥 Baixar CSV Modificado",
            data=csv_data,
            file_name="dados_modificados.csv",
            mime="text/csv"
        )
