import streamlit as st
import paho.mqtt.publish as publish
import random
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ REAL</h1>", stylesheet=None)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Usa el micrófono de tu dispositivo para ordenar acciones a la mascota</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

st.markdown("""
### 🎯 Elige el comando y habla:
Haz clic en el botón correspondiente. El navegador te pedirá **permiso para usar el micrófono** (dale a *Permitir*), di tu orden y al detener la grabación se enviará al instante a Wokwi.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🍎 Orden: Alimentar")
    # Este componente SÍ abre la ventana nativa de permisos del navegador
    audio_comer = mic_recorder(
        start_prompt="🔴 Hablar: Alimentar",
        stop_prompt="⏹️ Enviar a Wokwi",
        key='mic_alimentar'
    )
    
    if audio_comer:
        try:
            publish.single(
                topic=TOPIC,
                payload="alimentar",
                hostname=BROKER,
                port=1883,
                client_id=f"voice_ali_{random.randint(1000,9999)}"
            )
            st.success("🚀 ¡Orden 'alimentar' enviada a Wokwi por voz!")
        except Exception as e:
            st.error(f"Error MQTT: {e}")

with col2:
    st.markdown("#### 🎾 Orden: Saludar")
    audio_jugar = mic_recorder(
        start_prompt="🔴 Hablar: Saludar",
        stop_prompt="⏹️ Enviar a Wokwi",
        key='mic_saludar'
    )
    
    if audio_jugar:
        try:
            publish.single(
                topic=TOPIC,
                payload="saludar",
                hostname=BROKER,
                port=1883,
                client_id=f"voice_sal_{random.randint(1000,9999)}"
            )
            st.success("🚀 ¡Orden 'saludar' enviada a Wokwi por voz!")
        except Exception as e:
            st.error(f"Error MQTT: {e}")
