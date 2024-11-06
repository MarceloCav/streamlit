import streamlit as st
import pandas as pd
from utils.data_validation import valida_colunas
from utils.auth import check_login

check_login()

def exibir_validacao_colunas():
    st.title("Validação de Colunas")

    # Verifica se o DataFrame foi carregado
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return

    df = st.session_state.df
    obrigatorias = ['search_ref', 'manufacturer_ref', 'name', 'brand']
    opcionais = [
        'barcode', 'ncm', 'applications', 'net_weight', 'gross_weight', 'born_at', 'deprecated_at', 
        'catalog_id', 'height', 'width', 'length', 'url_thumb', 'notes', 
        'file_high', 'file_low', 'file_medium', 'file_water_mark', 'position'
    ]
    
    # Criação de dados fictícios para amostra
    st.write("### Dados fictícios para exemplo")
    dados_ficticios = {
        'search_ref': ['REF001', 'REF002'],
        'manufacturer_ref': ['MANU001', 'MANU002'],
        'name': ['Produto A', 'Produto B'],
        'barcode': ['1234567890123', '9876543210123'],
        'ncm': ['12345678', '87654321']
        # Adicione mais colunas conforme necessário
    }
    df_ficticio = pd.DataFrame(dados_ficticios)
    st.dataframe(df_ficticio)

    # Exibe quais colunas devem estar presentes
    st.write("### Colunas obrigatórias:")
    st.write(", ".join(obrigatorias))
    
    st.write("### Colunas opcionais:")
    st.write(", ".join(opcionais))

    # Valida colunas obrigatórias e opcionais
    colunas_faltantes, colunas_erradas = valida_colunas(df, obrigatorias, opcionais)

    # Exibe mensagens de erro para colunas faltantes e erradas
    if colunas_faltantes:
        st.error(f"Colunas obrigatórias faltando: {', '.join(colunas_faltantes)}")

    if colunas_erradas:
        st.warning(f"Colunas não reconhecidas: {', '.join(colunas_erradas)}")

        # Interface para renomeação de colunas não reconhecidas
        st.write("Selecione uma coluna não reconhecida para renomear:")
        
        # Menu de seleção para escolher a coluna a ser renomeada
        coluna_selecionada = st.selectbox("Coluna a ser renomeada:", colunas_erradas)

        # Campo de entrada para o novo nome da coluna
        novo_nome = st.text_input(f"Novo nome para a coluna '{coluna_selecionada}':")
        
        # Botão para aplicar a renomeação
        if st.button("Aplicar renomeação"):
            if novo_nome:
                # Renomeia a coluna no DataFrame
                st.session_state.df.rename(columns={coluna_selecionada: novo_nome}, inplace=True)
                st.success(f"Coluna '{coluna_selecionada}' renomeada para '{novo_nome}' com sucesso!")
                # Remove a coluna renomeada da lista de colunas erradas
                colunas_erradas.remove(coluna_selecionada)
            else:
                st.warning("Por favor, insira um novo nome para a coluna.")

# Chama a função principal da página
exibir_validacao_colunas()
