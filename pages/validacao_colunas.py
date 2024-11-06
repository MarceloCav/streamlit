import streamlit as st
import pandas as pd
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

# Função para verificar se as colunas de strings estão em UTF-8
def verifica_utf8(df, colunas):
    erros_utf8 = {}
    for coluna in colunas:
        erros = df[~df[coluna].apply(lambda x: isinstance(x, str) and is_utf8(x) if x is not None else True)]
        if not erros.empty:
            erros_utf8[coluna] = erros
    return erros_utf8

def is_utf8(texto):
    if texto is None:
        return True  # Ignora valores nulos
    try:
        texto.encode('utf-8').decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

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

    # Verifica e exibe erros de codificação UTF-8 nas colunas especificadas
    colunas_utf8 = ['applications', 'notes', 'name', 'brand']
    erros_utf8 = verifica_utf8(df, colunas_utf8)
    for coluna, df_erro in erros_utf8.items():
        mostrar_erro(df_erro, f"Erros de codificação UTF-8 encontrados na coluna {coluna}.", coluna)

    # Mensagem final se não houver erros
    if all(df_erro.empty for df_erro in [marcas_invalidas, ncm_invalidos, barcode_invalido, peso_invalido, dimensoes_invalidas, codigos_malformados]) and not erros_utf8:
        st.success("Todos os dados estão válidos!")

exibir_erros_dados()
