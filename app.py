import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Botmaker WhatsApp Templates",
    layout="wide"
)

# Título da aplicação
st.title("Botmaker WhatsApp Templates")
st.markdown("---")

# Obter configurações do ambiente
API_URL = os.getenv("API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@st.cache_data(ttl=300)  # Cache por 5 minutos
def fetch_templates():
    """Busca templates da API"""
    try:
        headers = {
            "access-token": ACCESS_TOKEN
        }
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar templates: {str(e)}")
        return []

# Buscar templates
with st.spinner("Carregando templates..."):
    templates = fetch_templates()

if not templates:
    st.warning("Nenhum template encontrado ou erro ao carregar dados.")
    st.stop()

# Criar DataFrame apenas com os campos solicitados
df_data = []
for template in templates:
    df_data.append({
        "Nome": template.get("name", ""),
        "Estado": template.get("state", ""),
        "Telefones": ", ".join(template.get("phoneLinesNumbers", [])),
        "Chatbot": template.get("botName", ""),
        "Categoria": template.get("category", ""),
    })

df = pd.DataFrame(df_data)

# Sidebar com filtros
st.sidebar.header("Filtros")

# Filtro por phoneLinesNumbers
phone_numbers = df["Telefones"].unique()
selected_phones = st.sidebar.multiselect(
    "Telefones",
    options=sorted(phone_numbers),
    default=[],
    placeholder="Filtre por telefones"
)

# Filtro por name
names = df["Nome"].unique()
selected_names = st.sidebar.multiselect(
    "Nome do Template",
    options=sorted(names),
    default=[],
    placeholder="Filtre por templates"
)

# Filtro por state
states = df["Estado"].unique()
selected_states = st.sidebar.multiselect(
    "Estado",
    options=sorted(states),
    default=[],
    placeholder="Filtre por estado"
)

# Filtro por category
categories = df["Categoria"].unique()
selected_categories = st.sidebar.multiselect(
    "Categoria",
    options=sorted(categories),
    default=[],
    placeholder="Filtre por categoria"
)

# Aplicar filtros
df_filtered = df.copy()

if selected_phones:
    df_filtered = df_filtered[df_filtered["Telefones"].isin(selected_phones)]

if selected_names:
    df_filtered = df_filtered[df_filtered["Nome"].isin(selected_names)]

if selected_states:
    df_filtered = df_filtered[df_filtered["Estado"].isin(selected_states)]

if selected_categories:
    df_filtered = df_filtered[df_filtered["Categoria"].isin(selected_categories)]

# Estatísticas
col1, col2 = st.columns(2)
col1.metric("Total de Templates", len(df))
col2.metric("Templates Filtrados", len(df_filtered))

st.markdown("---")

# Botão para limpar filtros
if st.sidebar.button("Limpar Filtros"):
    st.rerun()

# Exibir tabela
st.subheader(f"Templates ({len(df_filtered)} encontrados)")

# Configurar exibição da tabela
st.dataframe(
    df_filtered,
    use_container_width=True,
    hide_index=True
)

# Botão para exportar CSV
st.markdown("---")
col1, col2 = st.columns([1, 4])

with col1:
    csv = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="Exportar CSV",
        data=csv,
        file_name=f"botmaker_templates_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

