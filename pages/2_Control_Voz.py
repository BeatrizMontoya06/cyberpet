import streamlit as st
import paho.mqtt.publish as publish
import random

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ / COMANDOS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Simulador y panel de comandos por voz para tu mascota virtual</p>", unsafe_allow_html=True)

st.markdown("""
### 📋 Comandos de voz reconocidos:
* 🍎 **"Alimentar"** (o *"comer"*): Activa la comida y felicidad de la mascota.
* 🎾 **"Saludar"** (o *"jugar"*): Activa la interacción de juego.
""")

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

st.write("---")
st.subheader("🗣️ Panel de Activación por Voz Directa")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Decir: 'Alimentar'", use_container_width=True):
        try:
            publish.single(
                topic=TOPIC,
                payload="alimentar",
                hostname=BROKER,
                port=1883,
                client_id=f"voice_client_{random.randint(1000,9999)}"
            )
            st.success("✅ ¡Voz detectada: 'Alimentar' enviado a Wokwi!")
        except Exception as e:
            st.error(f"Error de red MQTT: {e}")

with col2:
    if st.button("🎙️ Decir: 'Saludar'", use_container_width=True):
        try:
            publish.single(
                topic=TOPIC,
                payload="saludar",
                hostname=BROKER,
                port=1883,
                client_id=f"voice_client_{random.randint(1000,9999)}"
            )
            st.success("✅ ¡Voz detectada: 'Saludar' enviado a Wokwi!")
        except Exception as e:
            st.error(f"Error de red MQTT: {e}")

st.write("---")
# Caja de texto alternativa para simular el reconocimiento de voz libre
comando_voz = st.text_input("O dicta / escribe tu comando de voz:", placeholder="Ej: alimentar, comer, jugar...")
if st.button("Transmitir Comando por Voz", use_container_width=True):
    if comando_voz:
        texto = comando_voz.lower().strip()
        if "comer" in texto or "alimentar" in texto:
            accion = "alimentar"
        elif "jugar" in texto or "saludar" in texto:
            accion = "saludar"
        else:
            accion = texto
            
        try:
            publish.single(
                topic=TOPIC,
                payload=accion,
                hostname=BROKER,
                port=1883,
                client_id=f"voice_text_{random.randint(1000,9999)}"
            )
            st.success(f"✅ Comando interpretado y enviado: '{accion}'")
        except Exception as e:
            st.error(f"Error: {e}")
