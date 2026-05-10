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
        min-height: 450px;
    }

    .glow-text {
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.7);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
        font-size: 24px;
    }

    .stat-container {
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .stat-label {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        font-weight: bold;
        color: #00ff00;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    .bar-bg {
        background: #111;
        height: 12px;
        border-radius: 6px;
        width: 100%;
        border: 1px solid #333;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        border-radius: 6px;
    }

    .f-power { background: linear-gradient(90deg, #ffaa00, #ffff00); }
    .f-combat { background: linear-gradient(90deg, #008000, #00ff00); }
    .f-speed { background: linear-gradient(90deg, #0044ff, #00d4ff); }
    .f-intel { background: linear-gradient(90deg, #6b21a8, #a855f7); }
    .f-durability { background: linear-gradient(90deg, #990000, #ff4b4b); }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Input personalizado */
    .stTextInput input {
        background-color: #111 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">OMNITRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#00ff00; font-size:12px; letter-spacing:8px; opacity:0.8; margin-bottom:30px;">ACCESO A BASE DE DATOS: GALVAN PRIME</p>', unsafe_allow_html=True)

# --- LÓGICA DE CARGA DE ARCHIVO ---
# Intentamos obtener la ruta absoluta para evitar errores en la nube
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'ben10_aliens_dataset.csv')

@st.cache_data
def load_data():
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path)
            data.columns = data.columns.str.strip().str.lower()
            return data
        except Exception as e:
            st.error(f"Error al leer el CSV: {e}")
            return None
    return None

df = load_data()

if df is not None:
    search = st.text_input("🧬 ESCANEAR ADN (Nombre del Alien):", placeholder="Ejemplo: Heatblast, XLR8...")

    if search:
        # Busqueda más flexible (quita espacios y no importa mayúsculas)
        results = df[df['name'].str.contains(search.strip(), case=False, na=False)]
    else:
        results = df.head(4)

    if not results.empty:
        cols = st.columns(2)
        for idx, (_, row) in enumerate(results.iterrows()):
            
            # Función para limpiar valores y evitar que se vea código HTML crudo
            def clean_val(val_orig):
                import re
                text = str(val_orig)
                # Si el texto parece contener HTML, intentamos extraer solo el texto plano
                clean = re.compile('<.*?>')
                return re.sub(clean, '', text)

            def get_num(col_name):
                try: 
                    # Intentamos limpiar el número por si tiene etiquetas
                    v = clean_val(row.get(col_name, 0))
                    return int(float(v))
                except: return 0

            name = clean_val(row.get('name', 'N/A')).upper()
            series = clean_val(row.get('series', 'N/A'))
            home = clean_val(row.get('home_world', 'Desconocido'))
            powers = clean_val(row.get('power', 'No registradas'))

            # Construcción de la tarjeta
            card_html = f'''
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <h2 class="glow-text">{name}</h2>
                    <span style="background:#00ff00; color:black; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:bold;">{series}</span>
                </div>
                <p style="color:#666; font-size:11px; margin: 0;">PLANETA: <span style="color:#aaa;">{home}</span></p>
                
                <div style="background: rgba(0,255,0,0.05); padding: 10px; border-radius: 8px; margin: 15px 0; border: 1px solid rgba(0,255,0,0.1);">
                    <span style="color:#00ff00; font-size:10px; font-weight:bold; display:block; margin-bottom:5px;">HABILIDADES:</span>
                    <span style="color:#ccc; font-size:12px; font-style:italic;">{powers}</span>
                </div>
            '''
            
            # Mapeo de estadísticas
            stats = [
                ("PODER TOTAL", get_num('total_power'), "f-power"),
                ("COMBATE", get_num('combat'), "f-combat"),
                ("VELOCIDAD", get_num('speed'), "f-speed"),
                ("INTELIGENCIA", get_num('intelligence'), "f-intel"),
                ("DURABILIDAD", get_num('durability'), "f-durability")
            ]
            
            for label, v, color_class in stats:
                width = min(v, 100)
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
        st.warning("SECUENCIA DE ADN NO ENCONTRADA EN LA BASE DE DATOS")
else:
    st.error("⚠️ ERROR DE CONEXIÓN: No se pudo localizar el núcleo de datos 'ben10_aliens_dataset.csv'.")
    st.info("Verifica que el archivo CSV esté en la raíz de tu repositorio junto a app.py.")
