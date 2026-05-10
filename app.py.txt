import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(
    page_title="Omnitrix Database OS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS (Inyectamos el diseño que te gusta) ---
st.markdown("""
    <style>
    /* Fondo y Base */
    .stApp {
        background-color: #0a0a0a;
        background-image: radial-gradient(circle at center, #051a05 0%, #0a0a0a 100%);
        color: #e0e0e0;
    }
    
    .main-title {
        font-family: 'Courier New', Courier, monospace;
        color: #00ff00;
        text-align: center;
        text-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 5px;
    }

    /* Estilo de la Tarjeta */
    .card {
        background: rgba(34, 34, 34, 0.9);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: #00ff00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }

    .glow-text {
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        text-transform: uppercase;
        font-weight: 900;
    }

    /* Bloque de Poderes Visuales */
    .power-box {
        background: rgba(0, 0, 0, 0.5);
        padding: 12px;
        border-left: 3px solid #00ff00;
        border-radius: 4px;
        margin: 15px 0;
    }

    /* Barras de Progreso Custom */
    .stat-row {
        margin-top: 8px;
    }
    .stat-header {
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        font-weight: bold;
        color: #888;
        margin-bottom: 2px;
    }
    .bar-bg {
        background: #222;
        height: 6px;
        border-radius: 10px;
        width: 100%;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        border-radius: 10px;
    }

    /* Colores de Barras */
    .bg-total { background: #ffcc00; box-shadow: 0 0 8px #ffcc00; }
    .bg-combat { background: #00ff00; box-shadow: 0 0 8px #00ff00; }
    .bg-speed { background: #00d4ff; box-shadow: 0 0 8px #00d4ff; }
    .bg-intel { background: #a855f7; box-shadow: 0 0 8px #a855f7; }
    .bg-durability { background: #ff4b4b; box-shadow: 0 0 8px #ff4b4b; }
    .bg-stealth { background: #ffffff; box-shadow: 0 0 8px #ffffff; opacity: 0.7; }
    .bg-element { background: #ff8c00; box-shadow: 0 0 8px #ff8c00; }

    /* Ocultar basura de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Título Principal
st.markdown('<h1 class="main-title">OMNITRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#006400; font-weight:bold; letter-spacing:3px;">PROTOCOLO DE ACCESO A DATOS</p>', unsafe_allow_html=True)

# --- CARGA DE ARCHIVO ---
uploaded_file = st.file_uploader("📂 CARGAR BASE DE DATOS (CSV)", type=["csv"])

if uploaded_file is not None:
    # Leer datos
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower() # Limpiar nombres de columnas

    # Buscador
    search_query = st.text_input("🔍 ESCANEAR ADN:", placeholder="Escribe el nombre del alien...")

    if search_query:
        results = df[df['name'].str.contains(search_query, case=False, na=False)]
    else:
        results = df.head(6)

    # Mostrar Resultados en columnas (2 por fila)
    if not results.empty:
        cols = st.columns(2)
        for idx, (_, row) in enumerate(results.iterrows()):
            with cols[idx % 2]:
                # Datos Descriptivos
                name = row.get('name', 'N/A').upper()
                series = row.get('series', 'Original')
                home = row.get('home_world', 'Desconocido')
                powers_text = row.get('power', 'No identificado')
                
                # Estadísticas Principales
                tp = int(row.get('total_power', 0))
                c = int(row.get('combat', 0))
                s = int(row.get('speed', 0))
                i = int(row.get('intelligence', 0))
                
                # Nuevas Estadísticas Visuales (Poderes convertidos a gráficas)
                dur = int(row.get('durability', 0))
                stl = int(row.get('stealth', 0))
                # Calculamos un "Nivel Elemental" promedio basado en heat, water, electricity
                ele = int((int(row.get('heat', 0)) + int(row.get('water', 0)) + int(row.get('electricity', 0))) / 3)

                # Renderizar Tarjeta
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h2 class="glow-text" style="margin:0; font-size: 1.5rem;">{name}</h2>
                            <span style="background:#052e05; color:#00ff00; font-size:10px; padding:2px 8px; border-radius:4px; font-weight:bold;">{series}</span>
                        </div>
                        <div style="text-align:right;">
                            <small style="color:#555; display:block; font-size:9px; font-weight:bold;">ORIGEN</small>
                            <small style="color:#fff;">{home}</small>
                        </div>
                    </div>

                    <div class="power-box">
                        <small style="color:#00ff00; font-weight:bold; font-size:10px; display:block; margin-bottom:8px; letter-spacing:1px;">ANÁLISIS DE HABILIDADES SECUNDARIAS</small>
                        
                        <div class="stat-row">
                            <div class="stat-header"><span>DURABILIDAD / RESISTENCIA</span><span>{dur}%</span></div>
                            <div class="bar-bg"><div class="bar-fill bg-durability" style="width:{min(dur, 100)}%;"></div></div>
                        </div>

                        <div class="stat-row">
                            <div class="stat-header"><span>SIGILO / CAMUFLAJE</span><span>{stl}%</span></div>
                            <div class="bar-bg"><div class="bar-fill bg-stealth" style="width:{min(stl, 100)}%;"></div></div>
                        </div>

                        <div class="stat-row">
                            <div class="stat-header"><span>POTENCIAL ELEMENTAL</span><span>{ele}%</span></div>
                            <div class="bar-bg"><div class="bar-fill bg-element" style="width:{min(ele, 100)}%;"></div></div>
                        </div>
                    </div>

                    <div style="padding: 0 5px;">
                        <div class="stat-row" style="margin-bottom:12px;">
                            <div class="stat-header"><span style="color:#ffcc00;">NIVEL DE AMENAZA (TOTAL)</span><span style="color:#ffcc00;">{tp}</span></div>
                            <div class="bar-bg" style="height:8px;"><div class="bar-fill bg-total" style="width:{min(tp, 100)}%;"></div></div>
                        </div>

                        <div class="stat-row">
                            <div class="stat-header"><span>FUERZA FÍSICA</span><span>{c}</span></div>
                            <div class="bar-bg"><div class="bar-fill bg-combat" style="width:{min(c, 100)}%;"></div></div>
                        </div>
                        
                        <div class="stat-row">
                            <div class="stat-header"><span>VELOCIDAD</span><span>{s}</span></div>
                            <div class="bar-bg"><div class="bar-fill bg-speed" style="width:{min(s, 100)}%;"></div></div>
                        </div>

                        <div class="stat-row">
                            <div class="stat-header"><span>INTELIGENCIA</span><span>{i}</span></div>
                            <div class="bar-bg"><div class="bar-fill bg-intel" style="width:{min(i, 100)}%;"></div></div>
                        </div>
                    </div>
                    
                    <div style="margin-top:15px; border-top:1px solid #222; padding-top:10px;">
                        <p style="color:#666; font-size:10px; line-height:1; margin:0;"><b>NOTAS DE CAMPO:</b> {powers_text[:80]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("⚠️ ADN NO ENCONTRADO EN LA BASE DE DATOS")
else:
    st.info("👋 BIENVENIDO, AZMUTH. Por favor, sube el archivo 'ben10_aliens_dataset.csv' para comenzar el escaneo.")

st.markdown("<p style='text-align:center; color:#222; font-size: 10px; margin-top:50px;'>Omnitrix OS v6.0 | Galván Prime Tech</p>", unsafe_allow_html=True)