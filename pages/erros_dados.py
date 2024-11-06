import streamlit as st
from utils.data_validation import (
    verifica_dimensoes_invalidas,
    verifica_codigos_malformados,
    verifica_marca_invalida,
    verifica_ncm_invalido,
    verifica_barcode_invalido,
    verifica_peso_invalido
)

from utils.auth import check_login

check_login()

def exibir_erros_dados():
    st.title("Detecção de Erros nos Dados")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return

    df = st.session_state.df

    # Função auxiliar para exibir erros detalhados
    def mostrar_erro(df_erro, mensagem, coluna_nome):
        if df_erro.empty:
            st.success(f"### Nenhum erro encontrado na coluna {coluna_nome}.")
        else:
            st.error(mensagem)
            st.write(f"Número de registros com erro na coluna {coluna_nome}: {len(df_erro)}")
            st.dataframe(df_erro)

    # Verifica e exibe erros de marca
    marcas_invalidas, brand_error = verifica_marca_invalida(df)
    mostrar_erro(marcas_invalidas, brand_error or "Marcas com formatação incorreta encontradas.", "marca")

    # Verifica e exibe erros de NCM
    ncm_invalidos, ncm_error = verifica_ncm_invalido(df)
    mostrar_erro(ncm_invalidos, ncm_error or "NCMs com formato incorreto encontrados.", "NCM")

    # Verifica e exibe erros de Barcode
    barcode_invalido, barcode_error = verifica_barcode_invalido(df)
    mostrar_erro(barcode_invalido, barcode_error or "Barcodes com formato incorreto encontrados.", "barcode")

    # Verifica e exibe erros de peso
    peso_invalido, peso_error = verifica_peso_invalido(df)
    mostrar_erro(peso_invalido, peso_error or "Registros com peso bruto menor que o peso líquido encontrados.", "peso")

    # Verifica e exibe dimensões inválidas
    dimensoes_invalidas, dim_error = verifica_dimensoes_invalidas(df)
    mostrar_erro(dimensoes_invalidas, dim_error or "Registros com dimensões inválidas encontrados.", "dimensões")

    # Verifica e exibe códigos malformados
    codigos_malformados, cod_error = verifica_codigos_malformados(df)
    mostrar_erro(codigos_malformados, cod_error or "Códigos malformados encontrados.", "códigos")

    # Mensagem final se não houver erros
    if all(df_erro.empty for df_erro in [marcas_invalidas, ncm_invalidos, barcode_invalido, peso_invalido, dimensoes_invalidas, codigos_malformados]):
        st.success("Todos os dados estão válidos!")

exibir_erros_dados()
