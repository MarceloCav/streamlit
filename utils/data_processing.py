import pandas as pd
import numpy as np
import re

def gerar_search_ref(df):
    df['search_ref'] = df['manufacturer_ref'].str.replace(' ', '_').str.upper()
    return df

def gerar_born_deprecated_at(df):
    year_pattern = re.compile(r'\b(19\d{2}|20[0-9]{2})\b')
    error_logs = []

    def check_invalid_characters(value):
        non_ascii = re.findall(r'[^\x00-\x7F]', value)
        if non_ascii:
            return f"Caracteres inválidos: {', '.join(non_ascii)}"
        return None

    def extract_years_and_validate(row):
        value = row['applications']
        if pd.isna(value) or str(value).strip().lower() in ['none', 'null', '']:
            return None, None
        years = year_pattern.findall(value)
        return (min(years) if years else None, max(years) if years else None)

    df['born_at'], df['deprecated_at'] = zip(*df.apply(extract_years_and_validate, axis=1))
    df['born_at'] = df['born_at'].fillna(np.nan)
    df['deprecated_at'] = df['deprecated_at'].fillna(np.nan)

    return df, error_logs
