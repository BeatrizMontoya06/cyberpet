import streamlit as st
import paho.mqtt.publish as publish
import random

st.set_page_config(
    page_title="Cyber-Pet Tamagotchi",
    page_icon="👾",
    layout="centered"
)

# Estilo visual Cyberpunk / Tamagotchi
st.markdown("""
<style>
    .tamagotchi-container {
        background: #1a0033;
        border: 3px solid #ff007f;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 0px 30px rgba(255, 0, 127, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>👾 CYBER-PET: VIRTUAL COMPANION</h1>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

# Inicializar estados de la mascota en la sesión de Streamlit
if "hambre" not in st.session_state:
    st.session_state.hambre = 80  # Porcentaje inicial (0 a 100)
if "felicidad" not in st.session_state:
    st.session_state.felicidad = 80
if "estado_mascota" not in st.session_state:
    st.session_state.estado_mascota = "normal"  # Estados: normal, alimentar, saludar, muerto

# --- CONTENEDOR VISUAL TIPO TAMAGOTCHI ---
with st.container():
    st.markdown("<div class='tamagotchi-container'>", unsafe_allow_html=True)
    
    # Carga de imágenes según el estado actual
    avatar_path = f"assets/{st.session_state.estado_mascota}.png"
    
    try:
        st.image(avatar_path, width=220)
    except:
        st.markdown(f"### 🐾 [ Estado actual: **{st.session_state.estado_mascota.upper()}** ]")
        st.caption("Crea una carpeta llamada 'assets/' y coloca tus imágenes: normal.png, alimentar.png, saludar.png, muerto.png")

    st.markdown("---")
    
    # --- BARRAS DE ESTADÍSTICAS ---
    st.markdown("### 📊 Estadísticas Vitales")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"🍎 **Hambre:** {st.session_state.hambre}%")
        st.progress(st.session_state.hambre)
    with col2:
        st.markdown(f"🎾 **Felicidad:** {st.session_state.felicidad}%")
        st.progress(st.session_state.felicidad)
        
    # --- LÓGICA DE SUPERVIVENCIA ---
    if st.session_state.hambre <= 0 or st.session_state.felicidad <= 0:
        st.session_state.estado_mascota = "muerto"
        st.error("💀 ¡Oh no! Tu Cyber-Pet ha muerto por descuido...")
        if st.button("🔄 Regenerar / Revivir Mascota", use_container_width=True):
            st.session_state.hambre = 100
            st.session_state.felicidad = 100
            st.session_state.estado_mascota = "normal"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🎮 Panel de Control Manual")

# Si la mascota está muerta, bloqueamos los comandos hasta que la revivan
if st.session_state.estado_mascota == "muerto":
    st.warning("⚠️ Tu mascota está inactiva. Debes revivirla arriba para poder interactuar.")
else:
    # Botón Dar de Comer (Mantiene tu lógica MQTT exacta)
    if st.button("🍎 Dar de Comer", use_container_width=True):
        try:
            publish.single(
                topic=TOPIC,
                payload="alimentar",
                hostname=BROKER,
                port=1883,
                client_id=f"streamlit_{random.randint(1000,9999)}"
            )
            # Actualizamos estadísticas y cambiamos la imagen a la de comer
            st.session_state.estado_mascota = "alimentar"
            st.session_state.hambre = min(100, st.session_state.hambre + 20)
            st.success("¡Mensaje enviado al puerto 1883!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    # Botón Jugar / Saludar (Mantiene tu lógica MQTT exacta)
    if st.button("🎾 Jugar", use_container_width=True):
        try:
            publish.single(
                topic=TOPIC,
                payload="saludar",
                hostname=BROKER,
                port=1883,
                client_id=f"streamlit_{random.randint(1000,9999)}"
            )
            # Actualizamos estadísticas y cambiamos la imagen a la de saludar
            st.session_state.estado_mascota = "saludar"
            st.session_state.felicidad = min(100, st.session_state.felicidad + 20)
            st.session_state.hambre = max(0, st.session_state.hambre - 5)
            st.success("¡Mensaje enviado al puerto 1883!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
