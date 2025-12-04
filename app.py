import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="BotMaker Templates",
    layout="wide"
)

# Título da aplicação
st.title("BotMaker WhatsApp Templates")
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
        st.error(f"❌ Erro ao buscar templates: {str(e)}")
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
        "name": template.get("name", ""),
        "state": template.get("state", ""),
        "phoneLinesNumbers": ", ".join(template.get("phoneLinesNumbers", [])),
        "botName": template.get("botName", ""),
        "category": template.get("category", ""),
        "requesterEmail": template.get("requesterEmail", ""),
    })

df = pd.DataFrame(df_data)

# Sidebar com filtros
st.sidebar.header("Filtros")

# Filtro por phoneLinesNumbers
phone_numbers = df["phoneLinesNumbers"].unique()
selected_phones = st.sidebar.multiselect(
    "Telefones",
    options=sorted(phone_numbers),
    default=[]
)

# Filtro por name
names = df["name"].unique()
selected_names = st.sidebar.multiselect(
    "Nome do Template",
    options=sorted(names),
    default=[]
)

# Filtro por state
states = df["state"].unique()
selected_states = st.sidebar.multiselect(
    "Estado",
    options=sorted(states),
    default=[]
)

# Filtro por category
categories = df["category"].unique()
selected_categories = st.sidebar.multiselect(
    "Categoria",
    options=sorted(categories),
    default=[]
)

# Aplicar filtros
df_filtered = df.copy()

if selected_phones:
    df_filtered = df_filtered[df_filtered["phoneLinesNumbers"].isin(selected_phones)]

if selected_names:
    df_filtered = df_filtered[df_filtered["name"].isin(selected_names)]

if selected_states:
    df_filtered = df_filtered[df_filtered["state"].isin(selected_states)]

if selected_categories:
    df_filtered = df_filtered[df_filtered["category"].isin(selected_categories)]

# Estatísticas
col1, col2 = st.columns(2)
col1.metric("Total de Templates", len(df))
col2.metric("Templates Filtrados", len(df_filtered))

st.markdown("---")

# Botão para limpar filtros
if st.sidebar.button("🔄 Limpar Filtros"):
    st.rerun()

# Exibir tabela
st.subheader(f"📊 Templates ({len(df_filtered)} encontrados)")

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
        label="📥 Exportar CSV",
        data=csv,
        file_name=f"botmaker_templates_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

