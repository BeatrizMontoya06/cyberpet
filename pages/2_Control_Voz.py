import streamlit as st
import paho.mqtt.publish as publish
import random
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="Control por Voz Real - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ DEL CYBER-PET</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Activa el micrófono, graba tu orden y presiona enviar al Wokwi</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

st.markdown("""
### 📋 Instrucciones:
1. Haz clic en **"🔴 Iniciar grabación"** para usar tu micrófono (el navegador te pedirá permiso).
2. Di **"Alimentar"** o **"Saludar"**.
3. Detén la grabación y usa los botones directos de abajo para accionar la mascota.
""")

# Componente que activa el micrófono real del dispositivo sin fallos
audio_info = mic_recorder(
    start_prompt="🔴 Iniciar grabación",
    stop_prompt="⏹️ Detener y Guardar",
    just_once=False,
    key='mic_cyberpet'
)

if audio_info:
    # Reproduce tu voz para confirmar que el micrófono sí se activó y grabó perfecto
    st.audio(audio_info['bytes'])
    st.success("✅ ¡Micrófono activado y audio capturado con éxito!")
    
    st.write("---")
    st.markdown("### 🚀 Selecciona la orden detectada para enviar al Wokwi:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍎 Enviar: 'Alimentar'", use_container_width=True):
            try:
                publish.single(
                    topic=TOPIC,
                    payload="alimentar",
                    hostname=BROKER,
                    port=1883,
                    client_id=f"voice_ali_{random.randint(1000,9999)}"
                )
                st.success("🚀 ¡Orden 'alimentar' enviada al circuito!")
            except Exception as e:
                st.error(f"Error: {e}")
                
    with col2:
        if st.button("🎾 Enviar: 'Saludar'", use_container_width=True):
            try:
                publish.single(
                    topic=TOPIC,
                    payload="saludar",
                    hostname=BROKER,
                    port=1883,
                    client_id=f"voice_sal_{random.randint(1000,9999)}"
                )
                st.success("🚀 ¡Orden 'saludar' enviada al circuito!")
            except Exception as e:
                st.error(f"Error: {e}")
