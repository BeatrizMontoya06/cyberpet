import streamlit as st
import paho.mqtt.publish as publish
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Cyber-Pet Tamagotchi",
    page_icon="👾",
    layout="centered"
)

# --- AUTO-REFRESH EN TIEMPO REAL (Cada 2 segundos) ---
count = st_autorefresh(interval=2000, limit=None, key="tamagotchi_refresher")

# --- ESTILOS VISUALES RETRO / TAMAGOTCHI ---
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #ff007f;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-shadow: 0px 0px 10px rgba(255, 0, 127, 0.6);
    }
    .description-box {
        text-align: center;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .tamagotchi-shell {
        background: #0d001a;
        border: 5px solid #ff007f;
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        box-shadow: 0px 0px 50px rgba(255, 0, 127, 0.4);
        margin-bottom: 20px;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff007f , #00ffcc);
    }
    .stButton>button {
        background-color: #1a0033; 
        color: #00ffcc; 
        border: 2px solid #00ffcc;
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stButton>button:hover { 
        background-color: #ff007f; 
        color: white; 
        border-color: #ff007f; 
        transform: scale(1.02); 
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO Y DESCRIPCIÓN TIPO TAMAGOTCHI ---
st.markdown("<h1 class='main-title'>👾 CYBER-PET: VIRTUAL COMPANION</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='description-box'>
    ¡Bienvenido a tu dispositivo virtual! Cuida a tu adorable gatito cibernético, 
    mantén sus niveles de hambre y felicidad altos dándole amor y atención para evitar que colapse.
</div>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN MQTT ---
BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

# --- INICIALIZACIÓN DE ESTADOS ---
if "hambre" not in st.session_state:
    st.session_state.hambre = 100
if "felicidad" not in st.session_state:
    st.session_state.felicidad = 100
if "estado_mascota" not in st.session_state:
    st.session_state.estado_mascota = "normal"
if "ultimo_refresco" not in st.session_state:
    st.session_state.ultimo_refresco = time.time()

# --- LÓGICA DE TIEMPO REAL (REDUCCIÓN DE ESTADÍSTICAS) ---
tiempo_actual = time.time()
tiempo_transcurrido = tiempo_actual - st.session_state.ultimo_refresco
st.session_state.ultimo_refresco = tiempo_actual

if st.session_state.estado_mascota != "muerto":
    tasa_reduccion = 0.4  # Velocidad a la que baja el hambre y felicidad
    puntos_a_bajar = tiempo_transcurrido * tasa_reduccion
    
    st.session_state.hambre = max(0, st.session_state.hambre - puntos_a_bajar)
    st.session_state.felicidad = max(0, st.session_state.felicidad - (puntos_a_bajar * 0.8))

    # Control de muerte
    if st.session_state.hambre <= 0 or st.session_state.felicidad <= 0:
        st.session_state.estado_mascota = "muerto"

# --- INTERFAZ PRINCIPAL TIPO CARCASSA TAMAGOTCHI ---
with st.container():
    st.markdown("<div class='tamagotchi-shell'>", unsafe_allow_html=True)
    
    # IMAGEN GRANDE DE LA MASCOTA (Protagonista visual absoluto)
    avatar_path = f"assets/{st.session_state.estado_mascota}.jpeg"
    
    col_pantalla_centro = st.columns([1, 4, 1])
    with col_pantalla_centro[1]:
        try:
            st.image(avatar_path, width=350)
        except:
            st.markdown(f"### 🐾 Estado Actual: {st.session_state.estado_mascota.upper()}")
            st.caption("Asegúrate de tener tus imágenes .jpeg en la carpeta assets/")

    st.markdown("---")
    
    # ESTADÍSTICAS VITALES DEBAJO DE LA PANTALLA
    st.markdown("### 📊 ESTADÍSTICAS VITALES")
    col_stat1, col_stat2 = st.columns(2)
    
    with col_stat1:
        st.markdown(f"🍎 **Hambre:** {int(st.session_state.hambre)}%")
        st.progress(int(st.session_state.hambre))
        
    with col_stat2:
        st.markdown(f"🎾 **Felicidad:** {int(st.session_state.felicidad)}%")
        st.progress(int(st.session_state.felicidad))

    # LÓGICA DE MUERTE Y REGENERACIÓN
    if st.session_state.estado_mascota == "muerto":
        st.error("💀 ¡ALERTA CRÍTICA! TU CYBER-PET HA COLAPSADO Y HA MUERTO.")
        if st.button("🔄 REGENERAR / REVIVIR MASCOTA", use_container_width=True):
            st.session_state.hambre = 100
            st.session_state.felicidad = 100
            st.session_state.estado_mascota = "normal"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANEL DE BOTONES (ACCIONES TÍPICAS DE TAMAGOTCHI) ---
st.markdown("### 🎮 PANEL DE CONTROL")

if st.session_state.estado_mascota == "muerto":
    st.warning("⚠️ Dispositivo bloqueado. Debes revivir a tu mascota para ejecutar comandos.")
else:
    # Creamos 4 botones distribuidos en 2 columnas (Acciones clásicas de Tamagotchi)
    bcol1, bcol2 = st.columns(2)
    
    with bcol1:
        # Botón 1: Alimentar
        if st.button("🍎 Dar de Comer", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="alimentar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "alimentar"
                st.session_state.hambre = min(100, st.session_state.hambre + 25)
                st.success("¡Comando 'alimentar' enviado!")
                time.sleep(1)
                st.session_state.estado_mascota = "normal"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        # Botón 2: Medicina / Curar (Nuevo botón típico)
        if st.button("💊 Dar Medicina", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="saludar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "saludar"
                st.session_state.felicidad = min(100, st.session_state.felicidad + 15)
                st.success("¡Comando 'medicina' enviado!")
                time.sleep(1)
                st.session_state.estado_mascota = "normal"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with bcol2:
        # Botón 3: Jugar / Saludar
        if st.button("🎾 Jugar con Mascota", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="saludar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "saludar"
                st.session_state.felicidad = min(100, st.session_state.felicidad + 25)
                st.success("¡Comando 'saludar' enviado!")
                time.sleep(1)
                st.session_state.estado_mascota = "normal"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        # Botón 4: Dormir / Descansar (Nuevo botón típico)
        if st.button("🌙 Apagar / Dormir", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="alimentar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "normal"
                st.session_state.hambre = min(100, st.session_state.hambre + 10)
                st.session_state.felicidad = min(100, st.session_state.felicidad + 10)
                st.success("¡Comando 'dormir' enviado (Estabilizando stats)!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
