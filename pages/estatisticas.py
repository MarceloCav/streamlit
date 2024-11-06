import streamlit as st
import plotly.express as px
from utils.auth import check_login

check_login()

def exibir_graficos():
    st.title("Estatísticas do DataFrame")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Para acessar esta página, carregue um arquivo CSV na página principal.")
        return 

    if 'df' in st.session_state:
        df = st.session_state.df
        st.text("Estatísticas do dataset:")
        st.dataframe(df.describe())

    colunas_faltantes = [col for col in ['height', 'width', 'length', 'net_weight', 'gross_weight', 'applications'] if col not in df.columns]

    if all(col in df.columns for col in ['height', 'width', 'length', 'net_weight', 'gross_weight', 'applications']):
        colunas = df[['height', 'width', 'length', 'net_weight', 'gross_weight', 'applications']]
        colunas['app_truncated'] = colunas['applications'].str[:80]
        try:
            fig_height_length = px.scatter(colunas, x='height', y='length', title='Dispersão entre Altura e Comprimento', hover_name='app_truncated', color='length')
            st.plotly_chart(fig_height_length)

            fig_height_width = px.scatter(colunas, x='height', y='width', title='Dispersão entre Altura e Largura', hover_name='app_truncated', color='width')
            st.plotly_chart(fig_height_width)

            fig_weights = px.scatter(colunas, x='net_weight', y='gross_weight', title='Dispersão entre Peso Líquido e Peso Bruto', hover_name='app_truncated', color='gross_weight')
            st.plotly_chart(fig_weights)

            for pos, coluna in enumerate(colunas.columns):
                fig = px.box(colunas, x=coluna, title=f'Gráfico de Boxplot para {coluna}')
                fig.update_traces(marker_color='gray', marker_line_width=1.5)
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o gráfico: {e}")
        
        for pos, coluna in enumerate(colunas.columns):      
            fig = px.histogram(colunas, x=coluna, title=f'Histograma de {coluna}', nbins=30)
            fig.update_traces(marker_color='gray', marker_line_width=1.5)

            st.plotly_chart(fig)

    else:
        colunas_faltantes_str = ', '.join(colunas_faltantes)
        st.error(f"As colunas {colunas_faltantes_str} não estão presentes no DataFrame. Verifique a aba 'Validação de Colunas' e corrija os nomes das colunas.")
    st.text("Informações estatítiscas sobre os gráficos plotados:")
    st.text("-> O gráfico de dispersão mostra a relação entre duas variáveis. Cada ponto representa um par de valores.")
    st.text("-> O gráfico de boxplot mostra a distribuição dos dados, destacando a mediana, os quartis e os outliers.")
    st.text("-> O histograma mostra a distribuição dos dados em intervalos, chamados de bins.")
    st.text("-> Os gráficos são interativos, permitindo zoom e mostrando informações dos pontos.")


exibir_graficos()