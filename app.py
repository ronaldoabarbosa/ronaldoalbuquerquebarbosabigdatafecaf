import pandas as pd
import plotly.express as px
import streamlit as st
import os
import altair as alt
from supabase import create_client, Client
from dotenv import load_dotenv

#Carregar variáveis do arquvio .env
load_dotenv()
# Configuração do Supabase
url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

#supabase = create_client(url, key)
supabase: Client = create_client(url,key)
if not url or not key:
    st.error("Credenciais do Supabase não encontradas nas variaveis de ambiente.")
    st.stop()

# Função para carregar dados da tabela no Supabase
def load_data(temp_log):
    response = supabase.table(temp_log).select("*").execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

# Título do Dashboard
st.title("Dashboard de Temperaturas IoT")

# Gráfico 1: Média de temperatura por dispositivo
st.header('Média de Temperatura por Dispositivo')
df_avg_temp = load_data('avg_temp_por_dispositivo2')
if not df_avg_temp.empty:
    fig1 = px.bar(df_avg_temp, x='noted_date', y='avg_temp')
    st.plotly_chart(fig1)
else:
    st.write("Nenhum dado disponível para 'avg_temp_por_dispositivo'.")

# Gráfico 2: Contagem de leituras por hora
st.header('Leituras por Hora do Dia')
df_leituras_hora = load_data('avg_temp_por_dispositivo2')
if not df_leituras_hora.empty:
    fig2 = px.line(df_leituras_hora, x='noted_date', y='avg_temp')
    st.plotly_chart(fig2)
else:
    st.write("Nenhum dado disponível para 'leituras_por_hora'.")

# Gráfico 3: Temperaturas máximas e mínimas por dia
st.header('Temperaturas Máximas e Mínimas por Dia')

df_temp_max_min = load_data('avg_temp_por_dispositivo2')

if not df_temp_max_min.empty:
    # Criando gráficos separados para temperatura máxima e mínima
    fig_max = px.line(df_temp_max_min, x='noted_date', y='avg_temp', title="Temperatura Máxima por Dia")
    fig_min = px.line(df_temp_max_min, x='noted_date', y='avg_temp', title="Temperatura Mínima por Dia")

 # Exibindo os gráficos
    st.plotly_chart(fig_max)
    st.plotly_chart(fig_min)
else:
    st.write("Nenhum dado disponível para 'temp_max_min_por_dia'.")


