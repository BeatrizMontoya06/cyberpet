import streamlit as st
import paho.mqtt.publish as publish
import random

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ DE LA MASCOTA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Interactúa con tu mascota mediante comandos de voz directos</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

st.markdown("""
### 🎯 Panel de Acciones por Voz:
Selecciona o activa el comando para que la mascota reaccione al instante en Wokwi:
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("🗣️ Decir: '¡Alimentar!'", use_container_width=True):
        try:
            publish.single(
                topic=TOPIC,
                payload="alimentar",
                hostname=BROKER,
                port=1883,
                client_id=f"voz_ali_{random.randint(1000,9999)}"
            )
            st.success("🗣️ Comando reconocido: **'alimentar'** ➔ ¡Enviado a Wokwi!")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    if st.button("🗣️ Decir: '¡Saludar!'", use_container_width=True):
        try:
            publish.single(
                topic=TOPIC,
                payload="saludar",
                hostname=BROKER,
                port=1883,
                client_id=f"voz_sal_{random.randint(1000,9999)}"
            )
            st.success("🗣️ Comando reconocido: **'saludar'** ➔ ¡Enviado a Wokwi!")
        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")

# Sección interactiva estilo consola de comandos de voz
st.markdown("### 💬 Consola de Transmisión por Voz")
comando_input = st.text_input("Escribe o simula el resultado de tu voz:", placeholder="ej. alimentar, comer, jugar...")

if st.button("🚀 Ejecutar Comando de Voz", use_container_width=True):
    if comando_input:
        texto = comando_input.lower().strip()
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
                client_id=f"voz_txt_{random.randint(1000,9999)}"
            )
            st.success(f"🎙️ Voz procesada con éxito. Orden enviada: **{accion}** ➔ ¡Mascota activada!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("⚠️ Por favor ingresa o di un comando válido.")
