# utils/auth.py
import streamlit as st

def check_login():
    if 'user' not in st.session_state:
        st.warning("### Você precisa estar logado para acessar esta página.")
        st.stop()
