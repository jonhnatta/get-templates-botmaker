# BotMaker Templates - Listagem e Filtragem

Aplicação Streamlit para listar, filtrar e exportar templates do BotMaker WhatsApp.

## 🚀 Instalação

1. Instale as dependências usando `uv`:
```bash
uv sync
```

2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
API_URL=https://api.botmaker.com/v2.0/whatsapp/templates
ACCESS_TOKEN=seu_token_aqui
```

## 📋 Uso

Execute a aplicação Streamlit:
```bash
uv run streamlit run app.py
```

A aplicação será aberta no navegador em `http://localhost:8501`.

## ✨ Funcionalidades

- ✅ Listagem de todos os templates da API
- 🔍 Filtros por:
  - Números de telefone (phoneLinesNumbers)
  - Nome do template (name)
  - Estado (state)
  - Categoria (category)
- 📥 Exportação para CSV (com ou sem filtros aplicados)
- 📊 Estatísticas dos templates
- 🖼️ Visualização de imagens dos templates

## 📦 Dependências

- streamlit
- requests
- python-dotenv
- pandas

