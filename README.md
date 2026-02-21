#  FinOps Data Engineering | Cyber Dark Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy)

Um sistema completo de Engenharia de Dados voltado para finanças pessoais (FinOps). O projeto automatiza a extração de extratos bancários (Nubank, Cartões de Crédito), realiza tratamento e categorização dos dados via scripts Python (ETL) e os consolida em um banco de dados relacional. 

A cereja do bolo é um **Dashboard Interativo** construído em Streamlit, estilizado com uma interface UI/UX avançada no tema **Cyber Dark**, desenvolvido com injeção profunda de CSS para sobrescrever o layout padrão do framework.

---

##  Funcionalidades

- **Pipeline ETL Automatizado:** Extração, transformação e carga de dados de arquivos CSV brutos direto para o Banco de Dados.
- **Categorização Inteligente:** Regras de negócio aplicadas no backend para classificar despesas e receitas automaticamente.
- **Dashboard Cyber Dark Premium:** Interface de alta performance construída no Streamlit, com design exclusivo, responsivo e focado em UX.
- **Gráficos Interativos (Plotly):** Análise visual de Fluxo de Caixa, Distribuição de Despesas e Indicadores (KPIs) com tooltips avançadas.
- **Filtros Dinâmicos:** Controle absoluto por Mês, Ano e Dia, com recarregamento instantâneo via sistema de cache otimizado do Streamlit.

---

## 📂 Estrutura da Arquitetura

```bash
📦 finops-data-engineering
 ┣ 📂 data/               # Armazenamento (Raw e Processed - Ignorados no Git)
 ┣ 📂 logs/               # Registros de execução do Pipeline
 ┣ 📂 src/
 ┃ ┣ 📂 database/         # Conexão SQLAlchemy e Modelos ORM
 ┃ ┣ 📂 extractors/       # Scripts de parser para extratos em CSV
 ┃ ┣ 📂 repositories/     # Padrão Repository para comunicação com o BD
 ┃ ┣ 📂 transformers/     # Camada de transformação de dados e categorias
 ┃ ┣ 📂 scripts/          # Ferramentas auxiliares (ex: Fixer de DB)
 ┃ ┣ 📜 main.py           # Orquestrador do Pipeline ETL
 ┃ ┗ 📜 dashboard.py      # Aplicação Frontend (Streamlit)
 ┣ 📜 .env.example        # Template de variáveis de ambiente
 ┣ 📜 requirements.txt    # Dependências do projeto
 ┗ 📜 README.md

```

---

## ⚙️ Como Executar o Projeto

### 1. Preparando o Ambiente

Clone o repositório e crie um ambiente virtual:

```bash
git clone [https://github.com/SamuelzinPires/finops-data-engineering.git](https://github.com/SamuelzinPires/finops-data-engineering.git)
cd finops-data-engineering
python -m venv venv
source venv/Scripts/activate  # No Windows

```

### 2. Instalando as Dependências

```bash
pip install -r requirements.txt

```

### 3. Configuração do Banco e Dados

1. Crie um arquivo `.env` na raiz do projeto com base no `.env.example` e defina sua `DATABASE_URL`.
2. Coloque seus extratos bancários (CSV) dentro da pasta `data/raw/`.

### 4. Rodando o Pipeline de Dados (ETL)

Execute o orquestrador para processar os arquivos e alimentar o banco:

```bash
python src/main.py

```

### 5. Lançando o Dashboard

Suba a interface gráfica:

```bash
streamlit run src/dashboard.py

```

---

*Desenvolvido com ☕ e muito código por [Samuel Pires](https://github.com/SamuelzinPires).*

```