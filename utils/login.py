import streamlit as st
import json

# Lista de usuários e senhas (isso pode ser substituído por um banco de dados no futuro)
# Estrutura JSON: { "username": {"password": "senha", "role": "admin"} }
users = {
    "admin": {"password": "admin_pass", "role": "admin"},
    "worker": {"password": "worker_pass", "role": "worker"}
}

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = users[username]["role"]
        return True
    return False

def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None

def is_logged_in():
    return st.session_state.get("logged_in", False)

def get_user_role():
    return st.session_state.get("role", "guest")
