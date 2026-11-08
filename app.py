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

# --- ENCABEZADO Y DESCRIPCIÓN ---
st.markdown("<h1 class='main-title'>👾 CYBER-PET: VIRTUAL COMPANION</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='description-box'>
    ¡Bienvenido a tu dispositivo virtual! Cuida a tu gatito cibernético gestionando 
    su Hambre, Felicidad y Energía. ¡Vigila sus barras para evitar que colapse!
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
if "energia" not in st.session_state:
    st.session_state.energia = 100
if "estado_mascota" not in st.session_state:
    st.session_state.estado_mascota = "normal"
if "expiracion_animacion" not in st.session_state:
    st.session_state.expiracion_animacion = 0
if "ultimo_refresco" not in st.session_state:
    st.session_state.ultimo_refresco = time.time()

# --- GESTIÓN DE TIEMPO Y ANIMACIONES TEMPORALES ---
tiempo_actual = time.time()
tiempo_transcurrido = tiempo_actual - st.session_state.ultimo_refresco
st.session_state.ultimo_refresco = tiempo_actual

# Si la mascota está haciendo una acción temporal (comer, medicina, jugar) y ya pasaron 3 segundos, regresa a normal
if tiempo_actual > st.session_state.expiracion_animacion and st.session_state.estado_mascota in ["alimentar", "medicina", "saludar"]:
    st.session_state.estado_mascota = "normal"

# --- LÓGICA DE SUPERVIVENCIA Y BARRAS ---
if st.session_state.estado_mascota != "muerto":
    if st.session_state.estado_mascota == "durmiendo":
        # Durmiendo recupera energía y gasta poco hambre
        st.session_state.energia = min(100, st.session_state.energia + (tiempo_transcurrido * 2.0))
        st.session_state.hambre = max(0, st.session_state.hambre - (tiempo_transcurrido * 0.2))
    else:
        # Despierto gasta estadísticas
        tasa = 0.4
        st.session_state.hambre = max(0, st.session_state.hambre - (tiempo_transcurrido * tasa))
        st.session_state.felicidad = max(0, st.session_state.felicidad - (tiempo_transcurrido * (tasa * 0.8)))
        st.session_state.energia = max(0, st.session_state.energia - (tiempo_transcurrido * (tasa * 0.6)))

    # Muerte si alguna estadística llega a 0
    if st.session_state.hambre <= 0 or st.session_state.felicidad <= 0 or st.session_state.energia <= 0:
        st.session_state.estado_mascota = "muerto"

# --- INTERFAZ PRINCIPAL (PANTALLA TAMAGOTCHI) ---
with st.container():
    st.markdown("<div class='tamagotchi-shell'>", unsafe_allow_html=True)
    
    # Carga segura de la imagen actual en formato .jpeg
    avatar_path = f"assets/{st.session_state.estado_mascota}.jpeg"
    
    col_pantalla_centro = st.columns([1, 4, 1])
    with col_pantalla_centro[1]:
        try:
            st.image(avatar_path, width=350)
        except:
            st.markdown(f"### 🐾 Estado Actual: {st.session_state.estado_mascota.upper()}")
            st.caption(f"Falta el archivo '{st.session_state.estado_mascota}.jpeg' en assets/")

    st.markdown("---")
    
    # 3 ESTADÍSTICAS VITALES
    st.markdown("### 📊 ESTADÍSTICAS VITALES")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"🍎 **Hambre:** {int(st.session_state.hambre)}%")
        st.progress(int(st.session_state.hambre))
        
    with col_stat2:
        st.markdown(f"🎾 **Felicidad:** {int(st.session_state.felicidad)}%")
        st.progress(int(st.session_state.felicidad))

    with col_stat3:
        st.markdown(f"⚡ **Energía:** {int(st.session_state.energia)}%")
        st.progress(int(st.session_state.energia))

    # MUERTE Y REGENERACIÓN
    if st.session_state.estado_mascota == "muerto":
        st.error("💀 ¡ALERTA CRÍTICA! TU CYBER-PET HA COLAPSADO Y HA MUERTO.")
        if st.button("🔄 REGENERAR / REVIVIR MASCOTA", use_container_width=True):
            st.session_state.hambre = 100
            st.session_state.felicidad = 100
            st.session_state.energia = 100
            st.session_state.estado_mascota = "normal"
            st.session_state.expiracion_animacion = 0
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANEL DE CONTROL (BOTONES) ---
st.markdown("### 🎮 PANEL DE CONTROL")

if st.session_state.estado_mascota == "muerto":
    st.warning("⚠️ Dispositivo bloqueado. Debes revivir a tu mascota para ejecutar comandos.")
else:
    bcol1, bcol2 = st.columns(2)
    
    with bcol1:
        # 1. Alimentar
        if st.button("🍎 Dar de Comer", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="alimentar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "alimentar"
                st.session_state.expiracion_animacion = time.time() + 3  # Muestra la imagen de comer durante 3 segundos exactos
                st.session_state.hambre = min(100, st.session_state.hambre + 30)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        # 2. Medicina
        if st.button("💊 Dar Medicina", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="saludar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "medicina"
                st.session_state.expiracion_animacion = time.time() + 3  # Muestra la imagen de medicina durante 3 segundos exactos
                st.session_state.energia = min(100, st.session_state.energia + 20)
                st.session_state.felicidad = min(100, st.session_state.felicidad + 15)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with bcol2:
        # 3. Jugar
        if st.button("🎾 Jugar con Mascota", use_container_width=True):
            try:
                publish.single(topic=TOPIC, payload="saludar", hostname=BROKER, port=1883, client_id=f"st_{random.randint(1000,9999)}")
                st.session_state.estado_mascota = "saludar"
                st.session_state.expiracion_animacion = time.time() + 3  # Muestra la imagen de saludar durante 3 segundos exactos
                st.session_state.felicidad = min(100, st.session_state.felicidad + 30)
                st.session_state.energia = max(0, st.session_state.energia - 10)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        # 4. Dormir / Durmiendo (Alterna el modo de suspensión)
        if st.button("🌙 Dormir / Descansar", use_container_width=True):
            if st.session_state.estado_mascota == "durmiendo":
                st.session_state.estado_mascota = "normal"
            else:
                st.session_state.estado_mascota = "durmiendo"
                st.session_state.expiracion_animacion = 0  # Sin límite de tiempo, duerme hasta que lo despierten
            st.rerun()
