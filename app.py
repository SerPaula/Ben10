import streamlit as st
import pandas as pd
import os

# Configuración de la interfaz estilo Omnitrix
st.set_page_config(
    page_title="Omnitrix Database OS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SISTEMA DE ESTILOS (CSS) ---
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
        background: rgba(15, 15, 15, 0.95);
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
        margin: 0;
    }

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

    .bar-bg {
        background: #111;
        height: 14px;
        border-radius: 7px;
        width: 100%;
        border: 1px solid #333;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 7px;
    }

    .f-power { background: linear-gradient(90deg, #ffaa00, #ffff00); box-shadow: 0 0 10px #ffff00; }
    .f-combat { background: linear-gradient(90deg, #008000, #00ff00); box-shadow: 0 0 10px #00ff00; }
    .f-speed { background: linear-gradient(90deg, #0044ff, #00d4ff); box-shadow: 0 0 10px #00d4ff; }
    .f-intel { background: linear-gradient(90deg, #6b21a8, #a855f7); box-shadow: 0 0 10px #a855f7; }
    .f-durability { background: linear-gradient(90deg, #990000, #ff4b4b); box-shadow: 0 0 10px #ff4b4b; }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">OMNITRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#00ff00; font-size:12px; letter-spacing:8px; opacity:0.8; margin-bottom:30px;">ACCESO A BASE DE DATOS: GALVAN PRIME</p>', unsafe_allow_html=True)

# --- CONFIGURACIÓN DE RUTA ABSOLUTA ---
# Obtenemos la ruta del directorio donde está este script (app.py)
base_path = os.path.dirname(__file__)
file_name = "ben10_aliens_dataset.csv"
full_path = os.path.join(base_path, file_name)

@st.cache_data
def load_data_from_repo():
    """Carga la base de datos buscando la ruta absoluta para evitar errores de despliegue."""
    if os.path.exists(full_path):
        try:
            data = pd.read_csv(full_path)
            data.columns = data.columns.str.strip().str.lower()
            return data
        except Exception as e:
            st.error(f"Error al procesar la base de datos: {e}")
            return None
    else:
        return None

# Carga automática de los datos
df = load_data_from_repo()

if df is not None:
    try:
        search = st.text_input("🧬 ESCANEAR ADN (Nombre del Alien):", placeholder="Ejemplo: Heatblast, XLR8...")

        if search:
            results = df[df['name'].str.contains(search, case=False, na=False)]
        else:
            results = df.head(4)

        if not results.empty:
            cols = st.columns(2)
            for idx, (_, row) in enumerate(results.iterrows()):
                
                def val(c):
                    try: return int(float(row.get(c, 0)))
                    except: return 0

                name = str(row.get('name', 'N/A')).upper()
                series = str(row.get('series', 'N/A'))
                home = str(row.get('home_world', 'Desconocido'))
                powers = str(row.get('power', 'Habilidades no registradas'))

                p_tot = val('total_power')
                p_com = val('combat')
                p_spe = val('speed')
                p_int = val('intelligence')
                p_dur = val('durability')

                card_html = f'''
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
                '''
                
                stats_config = [
                    ("PODER TOTAL", p_tot, "f-power"),
                    ("COMBATE", p_com, "f-combat"),
                    ("VELOCIDAD", p_spe, "f-speed"),
                    ("INTELIGENCIA", p_int, "f-intel"),
                    ("DURABILIDAD", p_dur, "f-durability")
                ]
                
                for label, v, color_class in stats_config:
                    width = str(min(v, 100))
                    card_html += f'''
                    <div class="stat-container">
                        <div class="stat-label"><span>{label}</span><span>{v}%</span></div>
                        <div class="bar-bg"><div class="bar-fill {color_class}" style="width:{width}%;"></div></div>
                    </div>
                    '''
                
                card_html += '</div>'

                with cols[idx % 2]:
                    st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("SECUENCIA DE ADN NO ENCONTRADA EN LOS ARCHIVOS")
            
    except Exception as e:
        st.error(f"ERROR DE PROCESAMIENTO: {e}")
else:
    st.error(f"⚠️ ERROR DE SISTEMA: El archivo '{file_name}' no se encuentra en el directorio raíz.")
    st.info(f"Ruta intentada: {full_path}")
    st.info("Asegúrate de que el CSV esté en la misma carpeta que este script en tu repositorio de GitHub.")
