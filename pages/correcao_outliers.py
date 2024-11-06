import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import check_login

check_login()

def correcao_outliers():
    st.title("Correção de Outliers")
    st.text("Aqui você pode corrigir os outliers do seu DataFrame.")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return
    
    df = st.session_state.df

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_file_name = st.session_state.file_name if 'file_name' in st.session_state else f"dataframe_{timestamp}.csv"
    
    st.dataframe(df)

    coluna_para_filtrar = st.selectbox("Selecione a coluna para filtrar:", df.columns, key='coluna_para_filtrar')

    valor_para_filtrar = st.text_input("Digite o dado que deseja filtrar:", key='valor_para_filtrar')

    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = df
        
    if st.button("Filtrar"):
        if valor_para_filtrar:
            try:
                st.session_state.filtered_df = df[df[coluna_para_filtrar].astype(str) == valor_para_filtrar]
                if not st.session_state.filtered_df.empty:
                    st.success("Dados filtrados com sucesso!")
                else:
                    st.warning("Nenhum dado encontrado para o valor informado.")
            except Exception as e:
                st.error(f"Erro ao filtrar os dados: {e}")
        else:
            st.warning("Por favor, insira o dado a ser filtrado.")

    if not st.session_state.filtered_df.empty:
        st.subheader("Dados Filtrados:")
        st.dataframe(st.session_state.filtered_df)

        id_coluna = df.index.name if df.index.name else "ID"
        id_selecionado = st.selectbox(f"Selecione o {id_coluna} para editar:", st.session_state.filtered_df.index, key='id_selecionado')

        coluna_para_editar = st.selectbox("Selecione a coluna para editar:", df.columns, key='coluna_para_editar')

        novo_valor = st.text_input("Digite o novo valor:", key='novo_valor')
        
        if 'atualizacao_feita' not in st.session_state:
            st.session_state.atualizacao_feita = False

        if st.button("Atualizar Valor"):
            if novo_valor:
                try:
                    df.at[id_selecionado, coluna_para_editar] = novo_valor
                    st.success(f"Valor atualizado com sucesso: {coluna_para_editar} = {novo_valor} para {id_coluna} = {id_selecionado}.")
                    st.session_state.atualizacao_feita = True
                except Exception as e:
                    st.error(f"Erro ao atualizar o valor: {e}")
            else:
                st.warning("Por favor, insira um novo valor.")

        if st.session_state.atualizacao_feita:
            if st.button("Salvar Alterações"):
                try:
                    df.to_csv(original_file_name, index=False)
                    st.success(f"Alterações salvas com sucesso em '{original_file_name}'.")
                except Exception as e:
                    st.error(f"Erro ao salvar o arquivo: {e}")

        if st.button("Remover Linhas Filtradas"):
            df = df[~df.index.isin(st.session_state.filtered_df.index)]
            st.session_state.df = df  
            st.success("Linhas filtradas removidas com sucesso!")
            st.session_state.filtered_df = pd.DataFrame()

correcao_outliers()
