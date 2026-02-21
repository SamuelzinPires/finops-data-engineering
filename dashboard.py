import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.database.connection import engine
from datetime import datetime
import calendar

# ==============================================================================
# CONFIGURAÇÃO GERAL
# ==============================================================================
st.set_page_config(
    page_title="Controle Financeiro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS — CYBER DARK PREMIUM
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --bg-base:        #060B14;
        --bg-card:        #0D1521;
        --bg-card-hover:  #111D2E;
        --border:         #1A2840;
        --border-bright:  #1E3A5F;
        --cyan:           #00D4FF;
        --cyan-dim:       rgba(0, 212, 255, 0.12);
        --cyan-glow:      rgba(0, 212, 255, 0.25);
        --blue:           #2F81F7;
        --blue-dim:       rgba(47, 129, 247, 0.12);
        --purple:         #A855F7;
        --purple-dim:     rgba(168, 85, 247, 0.12);
        --red:            #F85149;
        --red-dim:        rgba(248, 81, 73, 0.12);
        --yellow:         #F0B429;
        --yellow-dim:     rgba(240, 180, 41, 0.12);
        --green:          #3FB950;
        --green-dim:      rgba(63, 185, 80, 0.12);
        --text-primary:   #E6EDF3;
        --text-secondary: #7D8FA8;
        --text-muted:     #3D5069;
        --font-main:      'Space Grotesk', sans-serif;
        --font-mono:      'JetBrains Mono', monospace;
    }

    /* BASE
       CORREÇÃO CRÍTICA: [class*="css"] NÃO recebe background-color.
       O Streamlit usa classes como "css-1d391kg" para montar o esqueleto
       interno da página. Pintar tudo que tem "css" no nome com fundo sólido
       cria cobertores opacos sobre a sidebar inteira e seus widgets.
       Regra de ouro: background-color SOMENTE em html e body. */
    html, body {
        font-family: var(--font-main) !important;
        background-color: var(--bg-base) !important;
        color: var(--text-primary) !important;
    }

    [class*="css"] {
        font-family: var(--font-main) !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #080E1A !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
    }

    /* SIDEBAR TITLE */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 0 20px 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 24px;
    }

    .sidebar-brand-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, var(--cyan), var(--blue));
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 0 12px var(--cyan-glow);
    }

    .sidebar-brand-text {
        font-family: var(--font-main);
        font-size: 14px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .sidebar-brand-sub {
        font-size: 10px;
        color: var(--text-muted);
        letter-spacing: 0.05em;
    }

    /* SELECTBOX / INPUTS */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stNumberInput"] > div {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    /* LABELS */
    .stSelectbox label, .stNumberInput label, .stCheckbox label {
        color: var(--text-secondary) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }

    /* METRICAS - esconder padrão, usamos HTML customizado */
    div[data-testid="stMetric"] {
        display: none !important;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 7px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        padding: 8px 16px !important;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--border-bright) !important;
        color: var(--cyan) !important;
    }

    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* CHECKBOX */
    .stCheckbox > label {
        color: var(--text-secondary) !important;
        font-size: 12px !important;
    }

    /* SECTION TITLES */
    .section-title {
        font-family: var(--font-main);
        font-size: 11px;
        font-weight: 700;
        color: var(--text-muted);
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* KPI CARDS */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 14px 14px 0 0;
    }

    .kpi-card.cyan::before  { background: linear-gradient(90deg, var(--cyan), transparent); }
    .kpi-card.blue::before  { background: linear-gradient(90deg, var(--blue), transparent); }
    .kpi-card.purple::before{ background: linear-gradient(90deg, var(--purple), transparent); }
    .kpi-card.red::before   { background: linear-gradient(90deg, var(--red), transparent); }
    .kpi-card.yellow::before{ background: linear-gradient(90deg, var(--yellow), transparent); }
    .kpi-card.green::before { background: linear-gradient(90deg, var(--green), transparent); }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
    }

    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--text-secondary);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        line-height: 1.4;
    }

    .kpi-icon {
        width: 36px;
        height: 36px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }

    .kpi-icon.cyan   { background: var(--cyan-dim);   }
    .kpi-icon.blue   { background: var(--blue-dim);   }
    .kpi-icon.purple { background: var(--purple-dim); }
    .kpi-icon.red    { background: var(--red-dim);    }
    .kpi-icon.yellow { background: var(--yellow-dim); }
    .kpi-icon.green  { background: var(--green-dim);  }

    .kpi-value {
        font-family: var(--font-mono);
        font-size: 26px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }

    .kpi-value.cyan   { color: var(--cyan);   }
    .kpi-value.red    { color: var(--red);    }

    .kpi-delta {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 20px;
        letter-spacing: 0.03em;
    }

    .kpi-delta.positive { background: var(--green-dim); color: var(--green); }
    .kpi-delta.negative { background: var(--red-dim);   color: var(--red);   }
    .kpi-delta.neutral  { background: var(--border);    color: var(--text-secondary); }
    .kpi-delta.info     { background: var(--blue-dim);  color: var(--blue);  }

    /* ALERT BADGES */
    .alert-badges {
        display: flex;
        gap: 6px;
        margin-top: 10px;
        flex-wrap: wrap;
    }

    .badge {
        font-size: 10px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 20px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .badge.red    { background: var(--red-dim);    color: var(--red);    border: 1px solid rgba(248,81,73,0.3); }
    .badge.yellow { background: var(--yellow-dim); color: var(--yellow); border: 1px solid rgba(240,180,41,0.3); }

    /* SUMMARY TABLE */
    .summary-table {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        width: 100%;
    }

    .summary-table table {
        width: 100%;
        border-collapse: collapse;
    }

    .summary-table th {
        background: #0A1422;
        color: var(--text-muted);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 12px 16px;
        text-align: right;
        border-bottom: 1px solid var(--border);
    }

    .summary-table th:first-child { text-align: left; }

    .summary-table td {
        padding: 12px 16px;
        font-size: 13px;
        font-family: var(--font-mono);
        color: var(--text-primary);
        text-align: right;
        border-bottom: 1px solid var(--border);
    }

    .summary-table td:first-child {
        text-align: left;
        font-family: var(--font-main);
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 12px;
    }

    .summary-table tr:last-child td { border-bottom: none; }

    .summary-table tr.total-row td {
        background: #0A1422;
        font-weight: 700;
        color: var(--text-primary);
        border-top: 1px solid var(--border-bright);
    }

    .summary-table tr.total-row td:first-child {
        color: var(--cyan);
        font-family: var(--font-mono);
        font-size: 12px;
    }

    .val-pos  { color: var(--green) !important; }
    .val-neg  { color: var(--red)   !important; }
    .val-cyan { color: var(--cyan)  !important; }
    .val-blue { color: var(--blue)  !important; }

    /* GRAPH CARD WRAPPER */
    .graph-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px;
    }

    /* HEADER */
    .page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 28px;
    }

    .page-title {
        font-family: var(--font-main);
        font-size: 22px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.3px;
    }

    .page-title span {
        color: var(--cyan);
    }

    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--green-dim);
        border: 1px solid rgba(63,185,80,0.3);
        color: var(--green);
        font-size: 11px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        letter-spacing: 0.05em;
    }

    .live-dot {
        width: 6px;
        height: 6px;
        background: var(--green);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* DIVIDER */
    hr { border-color: var(--border) !important; margin: 24px 0 !important; }

    /* HIDE STREAMLIT */
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* SIDEBAR — garantir que o botao de reabrir sempre aparece */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #00D4FF !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #00D4FF !important;
    }

    /* Garantir que widgets nativos da sidebar sejam sempre visiveis */
    [data-testid="stSidebar"] [data-testid="stSelectbox"],
    [data-testid="stSidebar"] [data-testid="stNumberInput"],
    [data-testid="stSidebar"] [data-testid="stCheckbox"],
    [data-testid="stSidebar"] [data-testid="stButton"],
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stCheckbox,
    [data-testid="stSidebar"] button {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: relative !important;
        z-index: 1 !important;
    }

    /* Impedir que o section-title sobreponha elementos na sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        overflow: visible !important;
        position: relative !important;
        z-index: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# CARGA DE DADOS
# ==============================================================================
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_sql("SELECT * FROM transactions", engine)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return pd.DataFrame()


df_raw = load_data()

if df_raw.empty:
    st.markdown("""
    <div style="text-align:center;padding:80px 0;color:#3D5069;">
        <div style="font-size:48px;margin-bottom:16px;">⬡</div>
        <div style="font-size:16px;font-weight:600;">Aguardando dados</div>
        <div style="font-size:13px;margin-top:8px;">Importe os arquivos CSV para começar</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-icon">◈</div>
    <div>
        <div class="sidebar-brand-text">FinOps</div>
        <div class="sidebar-brand-sub">Controle Financeiro</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:10px;font-weight:700;color:#3D5069;letter-spacing:0.15em;text-transform:uppercase;border-bottom:1px solid #1A2840;padding-bottom:8px;margin:0 0 12px 0;'>Periodo</p>", unsafe_allow_html=True)

anos = sorted(df_raw['date'].dt.year.unique(), reverse=True)
ano_sel = st.sidebar.selectbox("ANO", anos)

df_ano = df_raw[df_raw['date'].dt.year == ano_sel].copy()

meses = sorted(df_ano['date'].dt.month.unique())
mapa_meses = {
    1: 'JANEIRO', 2: 'FEVEREIRO', 3: 'MARCO', 4: 'ABRIL',
    5: 'MAIO', 6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO',
    9: 'SETEMBRO', 10: 'OUTUBRO', 11: 'NOVEMBRO', 12: 'DEZEMBRO'
}
meses_fmt = ['TODOS'] + [mapa_meses[m] for m in meses]
mes_sel = st.sidebar.selectbox("MES", meses_fmt)

st.sidebar.markdown("<p style='font-size:10px;font-weight:700;color:#3D5069;letter-spacing:0.15em;text-transform:uppercase;border-bottom:1px solid #1A2840;padding-bottom:8px;margin:24px 0 12px 0;'>Configuracao</p>", unsafe_allow_html=True)

saldo_inicial = st.sidebar.number_input(
    "SALDO INICIAL",
    value=994.30,
    step=10.0,
    format="%.2f",
    help="Saldo na conta antes do primeiro mes importado. Ajuste para o saldo bater com o Nubank."
)

st.sidebar.markdown("<p style='font-size:10px;font-weight:700;color:#3D5069;letter-spacing:0.15em;text-transform:uppercase;border-bottom:1px solid #1A2840;padding-bottom:8px;margin:24px 0 12px 0;'>Filtro de Dia</p>", unsafe_allow_html=True)
filtro_dia_ativo = st.sidebar.checkbox("Filtrar por dia especifico")
dia_sel = None
if filtro_dia_ativo:
    dia_sel = st.sidebar.number_input("DIA", min_value=1, max_value=31, value=1, step=1)

st.sidebar.markdown("---")
if st.sidebar.button("Recarregar Dados", use_container_width=True):
    st.cache_data.clear()
    st.rerun()


# ==============================================================================
# FILTRAGEM TEMPORAL
# ==============================================================================
if mes_sel != 'TODOS':
    mes_num = [k for k, v in mapa_meses.items() if v == mes_sel][0]
    df_mes = df_ano[df_ano['date'].dt.month == mes_num].copy()
    last_day = calendar.monthrange(ano_sel, mes_num)[1]
    data_limite = datetime(ano_sel, mes_num, last_day)
    df_acumulado = df_raw[df_raw['date'] <= data_limite]
else:
    df_mes = df_ano.copy()
    df_acumulado = df_raw.copy()

if filtro_dia_ativo and dia_sel:
    df_mes = df_mes[df_mes['date'].dt.day == dia_sel].copy()


# ==============================================================================
# LOGICA DE NEGOCIO
# ==============================================================================
df_conta_mes = df_mes[df_mes['source'] == 'Nubank'].copy()
df_cartao_mes = df_mes[df_mes['source'] == 'Nubank Credit Card'].copy()

# Entradas reais (excluindo estornos)
mask_entrada = (
    (df_conta_mes['amount'] > 0) &
    (~df_conta_mes['description'].str.startswith('Estorno', na=False))
)
receita_mes = df_conta_mes[mask_entrada]['amount'].sum()

# Saidas
despesas_totais = df_conta_mes[df_conta_mes['amount'] < 0].copy()
investimentos_mes = abs(despesas_totais[despesas_totais['category'] == 'Investimento']['amount'].sum())
fatura_paga_mes = abs(despesas_totais[despesas_totais['category'] == 'Pagamento de Fatura']['amount'].sum())

despesas_reais = abs(despesas_totais[
    (despesas_totais['category'] != 'Investimento') &
    (despesas_totais['category'] != 'Pagamento de Fatura')
]['amount'].sum())

# Gastos cartao (excl pagamento recebido)
gastos_cartao = df_cartao_mes[df_cartao_mes['amount'] < 0]['amount'].abs().sum()

# Despesa total (conta + cartao)
despesa_total = despesas_reais + gastos_cartao

# Resultado
resultado_mes = receita_mes - despesa_total
margem = (resultado_mes / receita_mes * 100) if receita_mes > 0 else 0

# Saldo acumulado
df_conta_acumulado = df_acumulado[df_acumulado['source'] == 'Nubank']
saldo_acumulado = saldo_inicial + df_conta_acumulado['amount'].sum()

# Alertas
n_sem_categoria = df_conta_mes[df_conta_mes['category'].isna()].shape[0]
n_cartao_sem_cat = df_cartao_mes[df_cartao_mes['category'].isna()].shape[0]
total_sem_cat = n_sem_categoria + n_cartao_sem_cat
resultado_negativo = resultado_mes < 0


# ==============================================================================
# HEADER
# ==============================================================================
col_title, col_badge = st.columns([4, 1])
with col_title:
    periodo_label = f"{mes_sel} / {ano_sel}" if mes_sel != 'TODOS' else str(ano_sel)
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div style="font-size:11px;color:#3D5069;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:4px;">
                Painel Financeiro — {periodo_label}
            </div>
            <div class="page-title">Fluxo de <span>Caixa</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_badge:
    st.markdown("""
    <div style="text-align:right;padding-top:20px;">
        <div class="live-badge">
            <div class="live-dot"></div>
            CONECTADO
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# KPI CARDS — LINHA 1
# ==============================================================================
def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

resultado_class = "val-neg" if resultado_mes < 0 else "val-pos"
resultado_icon  = "▼" if resultado_mes < 0 else "▲"
resultado_delta = "negative" if resultado_mes < 0 else "positive"
margem_delta    = "negative" if margem < 0 else "positive"

alertas_total = total_sem_cat + (1 if resultado_negativo else 0)
alertas_criticos = 1 if resultado_negativo else 0
alertas_aviso = total_sem_cat

st.markdown(f"""
<div class="kpi-grid">
<div class="kpi-card cyan">
<div class="kpi-header">
<div class="kpi-label">Receita Total<br>do Mes</div>
<div class="kpi-icon cyan">$</div>
</div>
<div class="kpi-value cyan">{fmt_brl(receita_mes)}</div>
<span class="kpi-delta positive">▲ Entradas na conta</span>
</div>
<div class="kpi-card purple">
<div class="kpi-header">
<div class="kpi-label">Despesa Total<br>do Mes</div>
<div class="kpi-icon purple">⬡</div>
</div>
<div class="kpi-value">{fmt_brl(despesa_total)}</div>
<span class="kpi-delta negative">▼ Conta + Cartao</span>
</div>
<div class="kpi-card blue">
<div class="kpi-header">
<div class="kpi-label">Resultado<br>do Mes</div>
<div class="kpi-icon blue">◈</div>
</div>
<div class="kpi-value {resultado_class}">{fmt_brl(resultado_mes)}</div>
<span class="kpi-delta {resultado_delta}">{resultado_icon} Margem {margem:.1f}%</span>
</div>
<div class="kpi-card yellow">
<div class="kpi-header">
<div class="kpi-label">Alertas<br>Ativos</div>
<div class="kpi-icon yellow">⚠</div>
</div>
<div class="kpi-value">{alertas_total}</div>
<div class="alert-badges">
{"<span class='badge red'>" + str(alertas_criticos) + " critico</span>" if alertas_criticos > 0 else ""}
{"<span class='badge yellow'>" + str(alertas_aviso) + " sem categoria</span>" if alertas_aviso > 0 else "<span class='badge yellow'>0 avisos</span>"}
</div>
</div>
</div>
""", unsafe_allow_html=True)

# LINHA 2 — Saldo e Investimento
st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:28px;">
<div class="kpi-card green">
<div class="kpi-header">
<div class="kpi-label">Saldo em<br>Conta</div>
<div class="kpi-icon green">◎</div>
</div>
<div class="kpi-value" style="color:{'var(--green)' if saldo_acumulado >= 0 else 'var(--red)'}">
{fmt_brl(saldo_acumulado)}
</div>
<span class="kpi-delta info">Acumulado historico</span>
</div>
<div class="kpi-card blue">
<div class="kpi-header">
<div class="kpi-label">Investido<br>no Mes</div>
<div class="kpi-icon cyan">◇</div>
</div>
<div class="kpi-value" style="font-size:22px;">{fmt_brl(investimentos_mes)}</div>
<span class="kpi-delta info">RDB / Caixinha</span>
</div>
<div class="kpi-card red">
<div class="kpi-header">
<div class="kpi-label">Fatura Cartao<br>Paga</div>
<div class="kpi-icon red">□</div>
</div>
<div class="kpi-value" style="font-size:22px;">{fmt_brl(fatura_paga_mes)}</div>
<span class="kpi-delta neutral">Ja incluida nos gastos</span>
</div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# GRAFICOS — FLUXO DE CAIXA + DISTRIBUICAO
# ==============================================================================
st.markdown('<div class="section-title">Analise Visual</div>', unsafe_allow_html=True)

g1, g2 = st.columns([3, 2])

with g1:
    st.markdown("<p style='font-size:12px;font-weight:700;color:#7D8FA8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;margin-top:0;'>Fluxo de Caixa — Evolucao do Saldo</p>", unsafe_allow_html=True)

    df_chart = df_conta_acumulado.sort_values(by='date').copy()
    df_chart['saldo_acumulado'] = saldo_inicial + df_chart['amount'].cumsum()
    if ano_sel:
        df_chart = df_chart[df_chart['date'].dt.year == ano_sel]

    if not df_chart.empty:
        fig_area = go.Figure()

        # Area preenchida
        fig_area.add_trace(go.Scatter(
            x=df_chart['date'],
            y=df_chart['saldo_acumulado'],
            fill='tozeroy',
            mode='lines',
            name='Saldo',
            line=dict(width=2.5, color='#00D4FF'),
            fillcolor='rgba(0, 212, 255, 0.06)',
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>'
        ))

        # Linha zero
        fig_area.add_hline(y=0, line_dash="dot", line_color="#F85149", line_width=1, opacity=0.5)

        fig_area.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=260,
            xaxis=dict(
                showgrid=False,
                showline=False,
                tickfont=dict(size=10, color='#3D5069', family='JetBrains Mono'),
                tickformat='%d/%b'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(26,40,64,0.8)',
                zeroline=False,
                tickfont=dict(size=10, color='#3D5069', family='JetBrains Mono'),
                tickprefix='R$ ',
                tickformat=',.0f'
            ),
            hoverlabel=dict(
                bgcolor='#0D1521',
                bordercolor='#1A2840',
                font=dict(family='Space Grotesk', size=12, color='#E6EDF3')
            ),
            showlegend=False
        )
        st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Sem dados para o periodo.")


with g2:
    st.markdown("<p style='font-size:12px;font-weight:700;color:#7D8FA8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;margin-top:0;'>Distribuicao de Despesas</p>", unsafe_allow_html=True)

    # Unir gastos conta + cartao por categoria
    df_g_conta = despesas_totais[
        (despesas_totais['category'] != 'Pagamento de Fatura') &
        (despesas_totais['category'] != 'Investimento')
    ].copy()
    df_g_conta['abs_val'] = df_g_conta['amount'].abs()

    df_g_cartao = df_cartao_mes[df_cartao_mes['amount'] < 0].copy()
    df_g_cartao['abs_val'] = df_g_cartao['amount'].abs()

    df_pizza = pd.concat([
        df_g_conta[['category', 'abs_val']],
        df_g_cartao[['category', 'abs_val']]
    ])

    if not df_pizza.empty and df_pizza['abs_val'].sum() > 0:
        df_cat_pizza = df_pizza.groupby('category')['abs_val'].sum().reset_index()
        df_cat_pizza = df_cat_pizza.sort_values('abs_val', ascending=False)

        COLORS = ['#00D4FF', '#2F81F7', '#A855F7', '#F85149', '#F0B429',
                  '#3FB950', '#58a6ff', '#ff7b72', '#d2a8ff', '#79c0ff']

        fig_donut = go.Figure(data=[go.Pie(
            labels=df_cat_pizza['category'],
            values=df_cat_pizza['abs_val'],
            hole=0.65,
            marker=dict(
                colors=COLORS[:len(df_cat_pizza)],
                line=dict(color='#060B14', width=3)
            ),
            textinfo='none',
            hovertemplate='<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>'
        )])

        fig_donut.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=260,
            showlegend=True,
            legend=dict(
                orientation='v',
                x=1.0,
                y=0.5,
                font=dict(size=10, color='#7D8FA8', family='Space Grotesk'),
                bgcolor='rgba(0,0,0,0)'
            ),
            hoverlabel=dict(
                bgcolor='#0D1521',
                bordercolor='#1A2840',
                font=dict(family='Space Grotesk', size=12, color='#E6EDF3')
            ),
            annotations=[dict(
                text=f"<b>{len(df_cat_pizza)}</b><br><span style='font-size:10px'>categorias</span>",
                x=0.5, y=0.5,
                font=dict(size=14, color='#E6EDF3', family='Space Grotesk'),
                showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Sem despesas no periodo.")


# ==============================================================================
# GRAFICO DE BARRAS — GASTOS POR CATEGORIA
# ==============================================================================
st.markdown('<div class="section-title" style="margin-top:24px;">Gastos por Categoria</div>', unsafe_allow_html=True)

if not df_pizza.empty and df_pizza['abs_val'].sum() > 0:
    df_bar = df_pizza.groupby('category')['abs_val'].sum().reset_index().sort_values('abs_val', ascending=True)

    fig_bar = go.Figure(go.Bar(
        x=df_bar['abs_val'],
        y=df_bar['category'],
        orientation='h',
        marker=dict(
            color=df_bar['abs_val'],
            colorscale=[[0, '#0D2040'], [0.5, '#1E3A5F'], [1, '#00D4FF']],
            line=dict(width=0)
        ),
        text=[fmt_brl(v) for v in df_bar['abs_val']],
        textposition='outside',
        textfont=dict(color='#7D8FA8', size=11, family='JetBrains Mono'),
        hovertemplate='<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>'
    ))

    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=100, t=0, b=0),
        height=max(280, len(df_bar) * 44),
        xaxis=dict(showgrid=True, gridcolor='rgba(26,40,64,0.8)', showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#7D8FA8', family='Space Grotesk')),
        hoverlabel=dict(bgcolor='#0D1521', bordercolor='#1A2840', font=dict(family='Space Grotesk', size=12, color='#E6EDF3')),
        showlegend=False
    )

    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})


# ==============================================================================
# TABELA RESUMO — SALDO INICIAL / ENTRADA / SAIDA / PRODUTO
# ==============================================================================
st.markdown('<div class="section-title" style="margin-top:24px;">Resumo Consolidado</div>', unsafe_allow_html=True)


def color_val(v, invert=False):
    if v == 0:
        return f'<td style="color:#3D5069;">{fmt_brl(v)}</td>'
    if (v > 0 and not invert) or (v < 0 and invert):
        return f'<td class="val-pos">{fmt_brl(v)}</td>'
    return f'<td class="val-neg">{fmt_brl(v)}</td>'


def pct(v):
    if receita_mes == 0:
        return '<td style="color:#3D5069;">—</td>'
    p = v / receita_mes * 100
    cls = 'val-pos' if p > 0 else 'val-neg'
    return f'<td class="{cls}">{p:.1f}%</td>'


# Montar linhas: cada fonte de dado
rows_html = ""

# Linha: Conta Corrente
entrada_conta = receita_mes
saida_conta = despesas_reais + fatura_paga_mes
resultado_conta = entrada_conta - saida_conta - investimentos_mes

rows_html += f"""<tr>
<td>Conta Corrente</td>
{color_val(saldo_inicial)}
{color_val(entrada_conta)}
{color_val(saida_conta, invert=True)}
{color_val(resultado_conta)}
</tr>
"""

# Linha: Cartao de Credito
entrada_cartao = 0.0
resultado_cartao = -gastos_cartao

rows_html += f"""<tr>
<td>Cartao de Credito</td>
<td style="color:#3D5069;">—</td>
<td style="color:#3D5069;">—</td>
{color_val(gastos_cartao, invert=True)}
{color_val(resultado_cartao)}
</tr>
"""

# Linha: Investimentos
rows_html += f"""<tr>
<td>Investimentos (RDB)</td>
<td style="color:#3D5069;">—</td>
<td style="color:#3D5069;">—</td>
{color_val(investimentos_mes, invert=True)}
<td class="val-blue">{fmt_brl(investimentos_mes)}</td>
</tr>
"""

# Total
total_entrada = receita_mes
total_saida = despesa_total
total_resultado = resultado_mes
total_margem = margem

st.markdown(f"""
<div class="summary-table">
<table>
<thead>
<tr>
<th>Produto / Fonte</th>
<th>Saldo Inicial</th>
<th>Entrada</th>
<th>Saida</th>
<th>Resultado</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
<tfoot>
<tr class="total-row">
<td>TOTAL GERAL</td>
{color_val(saldo_inicial)}
<td class="val-cyan">{fmt_brl(total_entrada)}</td>
{color_val(total_saida, invert=True)}
{color_val(total_resultado)}
</tr>
<tr class="total-row" style="border-top:none;">
<td>MARGEM / RESULTADO</td>
<td style="color:#3D5069;">—</td>
<td style="color:#3D5069;">—</td>
<td style="color:#3D5069;">—</td>
<td class="{'val-pos' if total_margem >= 0 else 'val-neg'}">{total_margem:.1f}%</td>
</tr>
</tfoot>
</table>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# TABS — EXTRATO DETALHADO
# ==============================================================================
st.markdown('<div class="section-title" style="margin-top:28px;">Extrato Detalhado</div>', unsafe_allow_html=True)

t1, t2 = st.tabs(["CONTA CORRENTE", "CARTAO DE CREDITO"])

with t1:
    categorias = ['TODAS'] + sorted(df_conta_mes['category'].dropna().unique().tolist())
    cat_filtro = st.selectbox("Categoria", categorias, key="cat_conta")

    df_table = df_conta_mes.copy()
    if cat_filtro != 'TODAS':
        df_table = df_table[df_table['category'] == cat_filtro]

    df_table = df_table[['date', 'description', 'category', 'amount']].sort_values('date', ascending=False)

    st.dataframe(
        df_table.style
        .format({'date': lambda x: x.strftime('%d/%m/%Y'), 'amount': lambda x: fmt_brl(x)})
        .applymap(lambda v: 'color: #3FB950' if isinstance(v, (int, float)) and v > 0
                  else ('color: #F85149' if isinstance(v, (int, float)) and v < 0 else ''),
                  subset=['amount']),
        use_container_width=True,
        height=380
    )

with t2:
    categorias_cc = ['TODAS'] + sorted(df_cartao_mes['category'].dropna().unique().tolist())
    cat_filtro_cc = st.selectbox("Categoria", categorias_cc, key="cat_cartao")

    df_table_cc = df_cartao_mes.copy()
    if cat_filtro_cc != 'TODAS':
        df_table_cc = df_table_cc[df_table_cc['category'] == cat_filtro_cc]

    df_table_cc = df_table_cc[['date', 'description', 'category', 'amount']].sort_values('date', ascending=False)

    st.dataframe(
        df_table_cc.style
        .format({'date': lambda x: x.strftime('%d/%m/%Y'), 'amount': lambda x: fmt_brl(x)}),
        use_container_width=True,
        height=380
    )
