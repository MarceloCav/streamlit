import pandas as pd
import re
import unidecode

def valida_colunas(df, obrigatorias, opcionais):
    colunas_faltantes = [col for col in obrigatorias if col not in df.columns]
    colunas_erradas = [col for col in df.columns if col not in obrigatorias + opcionais]
    return colunas_faltantes, colunas_erradas

def verifica_dimensoes_invalidas(df):
    required_columns = ['width', 'height', 'length']
    mensagens_erro = []

    # Verifica se todas as colunas obrigatórias estão presentes
    for col in required_columns:
        if col not in df.columns:
            return pd.DataFrame(), f"Coluna {col} não encontrada no CSV."

    # Verifica valores nulos
    nulos = df[required_columns].isnull().any(axis=1)
    if nulos.any():
        mensagens_erro.append("Existem valores nulos nas colunas de dimensões obrigatórias (width, height, length).")

    # Verifica tipos de dados
    tipos_incorretos = [col for col in required_columns if not pd.api.types.is_numeric_dtype(df[col])]
    if tipos_incorretos:
        mensagens_erro.append(f"As colunas {', '.join(tipos_incorretos)} devem conter apenas números.")

    # Verifica valores negativos e fora do intervalo
    invalidas = df[
        (df['width'] <= 0) | (df['height'] <= 0) | (df['length'] <= 0) |
        (df['width'] > 10000) | (df['height'] > 10000) | (df['length'] > 10000)
    ]
    if not invalidas.empty:
        mensagens_erro.append("Existem dimensões inválidas com valores negativos ou fora do intervalo aceitável (0 < valor < 10000).")
    
    colunas_exibidas = ['search_ref', 'manufacturer_ref', 'brand', 'width', 'height', 'length']
    return invalidas[colunas_exibidas], " | ".join(mensagens_erro) if mensagens_erro else None

def verifica_codigos_malformados(df):
    if 'search_ref' not in df.columns:
        return pd.DataFrame(), "Coluna 'search_ref' não encontrada no CSV."
    
    malformados = df[~df['search_ref'].str.match(r'^[A-Za-z0-9]+$')]
    if not malformados.empty:
        colunas_exibidas = ['search_ref', 'manufacturer_ref', 'brand']
        return malformados[colunas_exibidas], "Códigos de referência do fabricante contêm caracteres inválidos. Permitidos apenas letras e números."
    
    return pd.DataFrame(), None

def verifica_ncm_invalido(df):
    if 'ncm' not in df.columns:
        return pd.DataFrame(), "Coluna 'ncm' não encontrada no CSV."
    
    df['ncm'] = df['ncm'].astype(str).str.replace(' ', '').str.replace('.', '')  # Remove espaços e pontos
    ncm_invalidos = df[df['ncm'].notnull() & ~df['ncm'].str.match(r'^\d{4}\d{2}\d{2}$')]
    
    if not ncm_invalidos.empty:
        ncm_invalidos['ncm'] = ncm_invalidos['ncm'].apply(lambda x: f"{str(x)[:4]}.{str(x)[4:6]}.{str(x)[6:]}" if len(str(x)) == 8 else x)
        colunas_exibidas = ['search_ref', 'manufacturer_ref', 'brand', 'ncm']
        return ncm_invalidos[colunas_exibidas], "NCMs com formato incorreto. Formato esperado: 0000.00.00."
    
    return pd.DataFrame(), None


def verifica_barcode_invalido(df):
    if 'barcode' not in df.columns:
        return pd.DataFrame(), "Coluna 'barcode' não encontrada no CSV."
    
    barcode_invalido = df[(df['barcode'].str.len() != 13) | df['barcode'].str.endswith('.0')]
    if not barcode_invalido.empty:
        barcode_invalido['barcode'] = barcode_invalido['barcode'].str.replace('.0', '', regex=False)
        colunas_exibidas = ['search_ref', 'manufacturer_ref', 'brand', 'barcode']
        return barcode_invalido[colunas_exibidas], "Barcodes incorretos: devem conter 13 caracteres sem sufixo '.0'."
    
    return pd.DataFrame(), None

def verifica_marca_invalida(df):
    if 'brand' not in df.columns:
        return pd.DataFrame(), "Coluna 'brand' não encontrada no CSV."
    
    marcas_invalidas = df[~df['brand'].apply(lambda x: unidecode.unidecode(x).isupper())]
    if not marcas_invalidas.empty:
        colunas_exibidas = ['search_ref', 'manufacturer_ref', 'brand']
        return marcas_invalidas[colunas_exibidas], "Marcas com formatação incorreta: devem estar em maiúsculas e sem acentos."
    
    return pd.DataFrame(), None

def verifica_peso_invalido(df):
    required_columns = ['gross_weight', 'net_weight']
    mensagens_erro = []
    peso_invalido = pd.DataFrame()

    # Verifica se as colunas de peso estão presentes
    for col in required_columns:
        if col not in df.columns:
            mensagens_erro.append(f"Coluna '{col}' não encontrada no CSV.")
            return pd.DataFrame(), " | ".join(mensagens_erro)

    # Verifica se o peso bruto é menor que o peso líquido
    peso_invalido = df[df['gross_weight'] < df['net_weight']]
    if not peso_invalido.empty:
        mensagens_erro.append("Peso bruto menor que o peso líquido para algumas linhas.")

    # Verifica valores nulos para peso bruto quando há peso líquido
    peso_invalido_null = df[df['gross_weight'].isnull() & df['net_weight'].notnull()]
    if not peso_invalido_null.empty:
        mensagens_erro.append("Existem valores de peso bruto nulos, embora o peso líquido esteja preenchido.")

    # Corrige os pesos
    peso_invalido['gross_weight'].fillna(peso_invalido['net_weight'], inplace=True)
    peso_invalido['net_weight'] = peso_invalido['net_weight'].apply(lambda x: 0 if pd.isna(x) else x)

    colunas_exibidas = ['search_ref', 'manufacturer_ref', 'brand', 'gross_weight', 'net_weight']
    return peso_invalido[colunas_exibidas], " | ".join(mensagens_erro) if mensagens_erro else None
