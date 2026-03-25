import streamlit as st
import pandas as pd
from google import genai
import os
import time

st.set_page_config(
    page_title="DataFinder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global Reset */
.stApp {
    font-family: 'Inter', sans-serif;
    background-color: #ffffff;
    color: #111827;
}




/* Align main block */
.block-container {
    padding-top: 1rem !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #fcfcfc;
    border-right: 1px solid #f0f0f0;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #4b5563;
}

/* Sidebar structure mimicking BeeBot */
.logo-container {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.5rem;
}
.logo-icon {
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 6px;
}
.logo-text {
    font-weight: 700;
    font-size: 1.3rem;
    color: #111827;
}

.search-bar {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #9ca3af;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.nav-menu {
    list-style: none;
    padding: 0;
    margin: 0 0 2rem 0;
}
.nav-menu li {
    padding: 0.55rem 0.8rem;
    margin-bottom: 0.2rem;
    border-radius: 8px;
    color: #6b7280;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.nav-menu li.active {
    background-color: #f3f4f6;
    color: #111827;
    font-weight: 500;
}

.history-group {
    font-size: 0.75rem;
    font-weight: 600;
    color: #9ca3af;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    text-transform: capitalize;
}
.history-item {
    font-size: 0.8rem;
    color: #4b5563;
    padding: 0.2rem 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    opacity: 0.8;
}

/* Badge at top */
.badge-container {
    margin-bottom: 2rem;
}
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: #374151;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Hero section */
.hero {
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 3rem;
}
.glass-sphere {
    width: 60px;
    height: 60px;
    margin: 0 auto 1.5rem auto;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 25%, #fff 0%, #e0c3fc 30%, #8ec5fc 80%, #6366f1 100%);
    box-shadow: 0 12px 35px rgba(142, 197, 252, 0.4);
}
.hero-greeting {
    font-size: 2.2rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.2rem;
}
.hero-question {
    font-size: 2.2rem;
    font-weight: 600;
    color: #111827;
}
.hero-question span {
    color: #6366f1; /* accent color */
}

/* Agent cards (Light Theme) */
.agent-card {
    background: #ffffff;
    border: 1px solid #f3f4f6;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.agent-card.engineer { border-left: 4px solid #3b82f6; }
.agent-card.consultant { border-left: 4px solid #a855f7; }

.agent-title {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.agent-title.eng { color: #3b82f6; }
.agent-title.cons { color: #a855f7; }

/* Metrics */
.metric-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 1rem; }
.metric-box {
    flex: 1;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.metric-box .value { font-size: 1.25rem; font-weight: 700; color: #111827; }
.metric-box .label { font-size: 0.7rem; color: #6b7280; text-transform: uppercase; font-weight: 600; margin-top: 0.2rem; }

/* Status */
.upload-success {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #166534;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

/* Chat Input Overrides */
div[data-testid="stChatInput"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.05);
}

/* Visual chips placement underneath chat */
.chat-chips-container {
    position: fixed;
    bottom: 30px;
    left: 55%;
    transform: translateX(-50%);
    display: flex;
    gap: 0.5rem;
    z-index: 99;
    pointer-events: none;
}
.chat-chip {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    color: #4b5563;
    box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    display: flex;
    align-items: center;
    gap: 0.4rem;
    pointer-events: auto;
    cursor: pointer;
    transition: all 0.2s ease;
}
.chat-chip:hover {
    background: #f9fafb;
    border-color: #d1d5db;
}
</style>
""", unsafe_allow_html=True)

# --- Prompts & Data Helpers ---
ENGINEER_PROMPT = """Eres un Ingeniero de Datos experto en Python y Pandas.
TU MISIÓN: Analizar los datos estadísticos y el contexto del CSV.
Responde EXCLUSIVAMENTE con hallazgos técnicos.
Usa markdown. NO des opiniones de negocio."""

CONSULTANT_PROMPT = """Eres un Consultor de Negocio Senior.
TU MISIÓN: Interpretar los datos técnicos y dar insights de negocio.
Enfócate en oportunidades, riesgos y eficiencia. Usa markdown."""

def build_context(df: pd.DataFrame, filename: str = "dataset") -> str:
    num_cols = df.select_dtypes(include="number").columns.tolist()
    context_parts = [f"=== DATASET: {filename} ===", f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}", "", "--- Tipos ---", df.dtypes.to_string(), ""]
    missing = df.isnull().sum()
    if missing.sum() > 0:
        context_parts.extend(["--- Valores Faltantes ---", missing[missing > 0].to_string(), ""])
    if num_cols:
        context_parts.extend(["--- Estadísticas (numéricas) ---", df[num_cols].describe().to_string(), ""])
    max_rows = min(50, len(df))
    context_parts.extend([f"--- Muestra ({max_rows} filas) ---", df.head(max_rows).to_string(index=False)])
    return "\n".join(context_parts)

def get_smart_metrics(df: pd.DataFrame) -> list:
    metrics = [{"value": f"{len(df):,}", "label": "Registros"}, {"value": str(len(df.columns)), "label": "Columnas"}]
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        col = num_cols[0]
        total = df[col].sum()
        display = f"{total/1_000_000:,.1f}M" if total > 1_000_000 else f"{total:,.0f}" if total > 1_000 else f"{total:,.2f}"
        metrics.append({"value": display, "label": f"Σ {col[:12]}"})
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        metrics.append({"value": str(df[cat_cols[0]].nunique()), "label": f"# {cat_cols[0][:12]}"})
    return metrics[:4]

def call_gemini(api_key: str, system_prompt: str, context: str, user_query: str, model_name: str = "gemini-2.5-flash") -> str:
    client = genai.Client(api_key=api_key)
    full_prompt = f"Datos:\n{context}\n\nPREGUNTA:\n{user_query}\n"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
            )
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep((attempt + 1) * 5)
            else:
                raise e
    return "❌ Error de conexión al procesar la solicitud."

def smart_parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include="object").columns:
        try:
            parsed = pd.to_datetime(df[col], infer_datetime_format=True)
            if parsed.notna().sum() > len(df) * 0.5: df[col] = parsed
        except: pass
    return df

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="logo-container">
        <div class="logo-icon"></div>
        <div class="logo-text">DataFinder</div>
    </div>
    
    """, unsafe_allow_html=True)
    
    st.markdown("<br><hr style='border-top: 1px solid #f0f0f0;'><br>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#6b7280; margin-bottom:0.5rem;'>⚙️ CONFIGURATION</div>", unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
    selected_model_label = st.selectbox("Model", ["Gemini 2.5 Flash", "Gemini 2.5 Pro"], label_visibility="collapsed")
    selected_model = "gemini-2.5-flash" if "Flash" in selected_model_label else "gemini-2.5-pro"
    
    uploaded_file = st.file_uploader("Upload Data", type=["csv"], label_visibility="collapsed")
    DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "data", "ventas_q1.csv")
    use_demo = False
    
    if uploaded_file is None and os.path.exists(DEFAULT_CSV):
        use_demo = st.toggle("Use demo (ventas_q1.csv)", value=False)
        
    df = None
    csv_filename = None
    
    if uploaded_file:
        try:
            try: df = pd.read_csv(uploaded_file)
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="latin-1")
            csv_filename = uploaded_file.name
            df = smart_parse_dates(df)
            st.markdown(f'<div class="upload-success">✅ {csv_filename} ({df.shape[0]} rows)</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")
    elif use_demo:
        df = pd.read_csv(DEFAULT_CSV)
        df = smart_parse_dates(df)
        csv_filename = "ventas_q1.csv"
        st.markdown(f'<div class="upload-success">✅ {csv_filename} ({df.shape[0]} rows)</div>', unsafe_allow_html=True)

# --- Main Page ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_csv" not in st.session_state:
    st.session_state.last_csv = None

current_csv_id = csv_filename if csv_filename else None
if current_csv_id != st.session_state.last_csv:
    st.session_state.messages = []
    st.session_state.last_csv = current_csv_id

st.markdown(f"""
<div class="badge-container">
    <div class="model-badge">
        <span style="color:#6366f1;">🤖</span> {selected_model_label} <span style="color:#d1d5db; margin-left:2px;">v</span>
    </div>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="hero">
        <div class="glass-sphere"></div>
        <div class="hero-greeting">Bienvenido a DataFinder</div>
        <div class="hero-question">¿Qué datos vamos a <span>analizar hoy?</span></div>
    </div>
    """, unsafe_allow_html=True)

    if df is not None:
        smart_metrics = get_smart_metrics(df)
        boxes_html = "".join(f'<div class="metric-box"><div class="value">{m["value"]}</div><div class="label">{m["label"]}</div></div>' for m in smart_metrics)
        st.markdown(f'<div class="metric-row" style="max-width: 800px; margin: 0 auto;">{boxes_html}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            with st.expander("👀 View Data Preview", expanded=False):
                st.dataframe(df.head(50), use_container_width=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"], unsafe_allow_html=True)

user_query = st.chat_input("Initiate a query or send a command to the AI..." if df is not None else "Upload a CSV to start...")



if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    if not api_key:
        with st.chat_message("assistant", avatar="⚠️"):
            st.warning("Please provide your **Gemini API Key** in the sidebar settings.")
        st.stop()
    if df is None:
        with st.chat_message("assistant", avatar="⚠️"):
            st.error("No data loaded. **Upload a CSV** in the sidebar.")
        st.stop()

    context = build_context(df, csv_filename)

    with st.chat_message("assistant", avatar="✨"):
        st.markdown('<div class="agent-card engineer"><div class="agent-title eng">⚙️ Data Engineer Process</div>', unsafe_allow_html=True)
        with st.spinner("Processing data structure..."):
            try:
                eng_response = call_gemini(api_key, ENGINEER_PROMPT, context, user_query, selected_model)
                st.markdown(eng_response)
            except Exception as e:
                eng_response = f"❌ Error: {e}"
                st.error(eng_response)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="agent-card consultant"><div class="agent-title cons">💡 Business Consultant Analysis</div>', unsafe_allow_html=True)
        with st.spinner("Synthesizing business insights..."):
            try:
                cons_response = call_gemini(api_key, CONSULTANT_PROMPT, context, user_query, selected_model)
                st.markdown(cons_response)
            except Exception as e:
                cons_response = f"❌ Error: {e}"
                st.error(cons_response)
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": f'<div class="agent-card engineer"><div class="agent-title eng">⚙️ Data Engineer Output</div>\n\n{eng_response}\n</div><div class="agent-card consultant"><div class="agent-title cons">💡 Business Consultant Analysis</div>\n\n{cons_response}\n</div>',
        "avatar": "✨",
    })
    st.rerun()
