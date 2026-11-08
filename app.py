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

# --- AUTO-REFRESH EN TIEMPO REAL ---
# Refresca la página cada 2 segundos para actualizar las estadísticas de hambre y felicidad
count = st_autorefresh(interval=2000, limit=None, key="frefresher")

# --- ESTILOS VISUALES CYBERPUNK ---
st.markdown("""
<style>
    .tamagotchi-container {
        background: #0d001a;
        border: 4px solid #00ffcc;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 0px 40px rgba(0, 255, 204, 0.5);
        margin-bottom: 25px;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff007f , #00ffcc);
    }
    h1, h2, h3 { color: #ff007f !important; font-family: 'Courier New', monospace; }
    .stButton>button {
        background-color: #0d001a; color: #00ffcc; border: 2px solid #00ffcc;
        font-family: 'Courier New', monospace; font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #ff007f; color: white; border-color: #ff007f; scale: 1.02; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>👾 CYBER-PET VIRTUAL TAMAGOTCHI</h1>", unsafe_allow_html=True)

# --- CONFIGURACIÓN MQTT ---
BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

# --- INICIALIZACIÓN DE ESTADOS (SESSION STATE) ---
if "hambre" not in st.session_state:
    st.session_state.hambre = 100  # Empieza lleno
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

# Solo bajan las estadísticas si la mascota está viva
if st.session_state.estado_mascota != "muerto":
    tasa_reduccion = 0.5  # Velocidad a la que baja el hambre
    puntos_a_bajar = tiempo_transcurrido * tasa_reduccion
    
    st.session_state.hambre = max(0, st.session_state.hambre - puntos_a_bajar)
    st.session_state.felicidad = max(0, st.session_state.felicidad - (puntos_a_bajar * 0.7))

    # Verificar si la mascota muere
    if st.session_state.hambre <= 0 or st.session_state.felicidad <= 0:
        st.session_state.estado_mascota = "muerto"

# --- CONTENEDOR VISUAL TIPO TAMAGOTCHI ---
with st.container():
    st.markdown("<div class='tamagotchi-container'>", unsafe_allow_html=True)
    
    # Carga de imágenes dinámicas en formato .jpeg
    avatar_path = f"assets/{st.session_state.estado_mascota}.jpeg"
    
    col_img, col_stats = st.columns([1, 1])
    
    with col_img:
        try:
            st.image(avatar_path, width=250)
        except:
            st.markdown(f"### 🐾 Estado: {st.session_state.estado_mascota.upper()}")
            st.caption("Faltan las imágenes .jpeg en la carpeta assets/")

    with col_stats:
        st.markdown("### 📊 Signos Vitales")
        st.write("")
        st.markdown(f"🍎 **Hambre:** {int(st.session_state.hambre)}%")
        st.progress(int(st.session_state.hambre))
        
        st.write("")
        st.markdown(f"🎾 **Felicidad:** {int(st.session_state.felicidad)}%")
        st.progress(int(st.session_state.felicidad))

    # --- LÓGICA DE SUPERVIVENCIA Y REGENERACIÓN ---
    if st.session_state.estado_mascota == "muerto":
        st.error("💀 ¡OH NO! TU CYBER-PET HA MUERTO POR NEGLIGENCIA.")
        if st.button("🔄 PROCESO DE REGENERACIÓN (REVIVIR)", use_container_width=True):
            st.session_state.hambre = 100
            st.session_state.felicidad = 100
            st.session_state.estado_mascota = "normal"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANEL DE CONTROL MANUAL (MQTT) ---
st.markdown("### 🎮 PANEL DE ACCIONES (ENVÍO MQTT)")

if st.session_state.estado_mascota == "muerto":
    st.warning("⚠️ Mascota inactiva. Procede a la regeneración arriba.")
else:
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🍎 Dar de Comer", use_container_width=True):
            try:
                publish.single(
                    topic=TOPIC,
                    payload="alimentar",
                    hostname=BROKER,
                    port=1883,
                    client_id=f"streamlit_{random.randint(1000,9999)}"
                )
                st.session_state.estado_mascota = "alimentar"
                st.session_state.hambre = min(100, st.session_state.hambre + 30)
                st.success("¡Mensaje 'alimentar' enviado al puerto 1883!")
                time.sleep(1)
                st.session_state.estado_mascota = "normal"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with col_btn2:
        if st.button("🎾 Jugar / Saludar", use_container_width=True):
            try:
                publish.single(
                    topic=TOPIC,
                    payload="saludar",
                    hostname=BROKER,
                    port=1883,
                    client_id=f"streamlit_{random.randint(1000,9999)}"
                )
                st.session_state.estado_mascota = "saludar"
                st.session_state.felicidad = min(100, st.session_state.felicidad + 30)
                st.success("¡Mensaje 'saludar' enviado al puerto 1883!")
                time.sleep(1)
                st.session_state.estado_mascota = "normal"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
