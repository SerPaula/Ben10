import streamlit as st
import pandas as pd

# Configuración de la interfaz
st.set_page_config(
    page_title="Omnitrix Database OS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SISTEMA DE ESTILOS (CSS) ---
# He forzado el renderizado de las barras con sombras y degradados
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
        background-image: radial-gradient(circle at center, #051a05 0%, #0a0a0a 100%);
        color: #e0e0e0;
    }
    
    .main-title {
        font-family: 'Courier New', Courier, monospace;
        color: #00ff00;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.8);
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0px;
    }

    .card {
        background: rgba(15, 15, 15, 0.9);
        border: 2px solid #00ff00;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }

    .glow-text {
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.7);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Contenedor de cada barra */
    .stat-container {
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .stat-label {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: bold;
        color: #00ff00;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    /* Fondo de la barra */
    .bar-bg {
        background: #111;
        height: 14px;
        border-radius: 7px;
        width: 100%;
        border: 1px solid #333;
        overflow: hidden;
        position: relative;
    }

    /* Relleno de la barra con animación y brillo */
    .bar-fill {
        height: 100%;
        border-radius: 7px;
    }

    /* Colores Neón */
    .f-power { background: linear-gradient(90deg, #ffaa00, #ffff00); box-shadow: 0 0 10px #ffff00; }
    .f-combat { background: linear-gradient(90deg, #008000, #00ff00); box-shadow: 0 0 10px #00ff00; }
    .f-speed { background: linear-gradient(90deg, #0044ff, #00d4ff); box-shadow: 0 0 10px #00d4ff; }
    .f-intel { background: linear-gradient(90deg, #6b21a8, #a855f7); box-shadow: 0 0 10px #a855f7; }
    .f-durability { background: linear-gradient(90deg, #990000, #ff4b4b); box-shadow: 0 0 10px #ff4b4b; }

    /* Ocultar basura de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">OMNITRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#00ff00; font-size:12px; letter-spacing:8px; opacity:0.8; margin-bottom:30px;">DATABASE ACCESS: GALVAN PRIME</p>', unsafe_allow_html=True)

# Subida de archivos
uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()

        search = st.text_input("🧬 ESCANEAR ADN (Nombre del Alien):", placeholder="Ejemplo: Heatblast, XLR8...")

        if search:
            results = df[df['name'].str.contains(search, case=False, na=False)]
        else:
            results = df.head(4)

        if not results.empty:
            cols = st.columns(2)
            for idx, (_, row) in enumerate(results.iterrows()):
                
                # Función para limpiar números
                def val(c):
                    try: return int(float(row.get(c, 0)))
                    except: return 0

                name = str(row.get('name', 'N/A')).upper()
                series = str(row.get('series', 'N/A'))
                home = str(row.get('home_world', 'Desconocido'))
                powers = str(row.get('power', 'No descritos'))

                # Variables de poder
                p_tot = val('total_power')
                p_com = val('combat')
                p_spe = val('speed')
                p_int = val('intelligence')
                p_dur = val('durability')

                with cols[idx % 2]:
                    # Usamos una sola cadena HTML gigante para que Streamlit no "rompa" el código
                    card_html = f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 class="glow-text">{name}</h2>
                            <span style="background:#00ff00; color:black; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;">{series}</span>
                        </div>
                        <p style="color:#666; font-size:11px; margin: 0;">PLANETA: <span style="color:#aaa;">{home}</span></p>
                        
                        <div style="background: rgba(0,255,0,0.05); padding: 10px; border-radius: 8px; margin: 15px 0; border: 1px solid rgba(0,255,0,0.1);">
                            <span style="color:#00ff00; font-size:10px; font-weight:bold; display:block; margin-bottom:5px;">HABILIDADES:</span>
                            <span style="color:#ccc; font-size:12px; font-style:italic;">{powers}</span>
                        </div>

                        <div class="stat-container">
                            <div class="stat-label"><span>PODER TOTAL</span><span>{p_tot}%</span></div>
                            <div class="bar-bg"><div class="bar-fill f-power" style="width:{min(p_tot, 100)}%;"></div></div>
                        </div>

                        <div class="stat-container">
                            <div class="stat-label"><span>COMBATE</span><span>{p_com}%</span></div>
                            <div class="bar-bg"><div class="bar-fill f-combat" style="width:{min(p_com, 100)}%;"></div></div>
                        </div>

                        <div class="stat-container">
                            <div class="stat-label"><span>VELOCIDAD</span><span>{p_spe}%</span></div>
                            <div class="bar-bg"><div class="bar-fill f-speed" style="width:{min(p_spe, 100)}%;"></div></div>
                        </div>

                        <div class="stat-container">
                            <div class="stat-label"><span>INTELIGENCIA</span><span>{p_int}%</span></div>
                            <div class="bar-bg"><div class="bar-fill f-intel" style="width:{min(p_int, 100)}%;"></div></div>
                        </div>

                        <div class="stat-container">
                            <div class="stat-label"><span>DURABILIDAD</span><span>{p_dur}%</span></div>
                            <div class="bar-bg"><div class="bar-fill f-durability" style="width:{min(p_dur, 100)}%;"></div></div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.error("ADN NO IDENTIFICADO. Por favor, verifique el nombre.")
    except Exception as e:
        st.error(f"Error en el sistema central: {e}")
else:
    st.info("SISTEMA OMNITRIX OFFLINE. Cargue el archivo CSV para iniciar el escaneo.")
