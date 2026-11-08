import streamlit as st
import paho.mqtt.client as paho
import random

st.set_page_config(
    page_title="~*~ Cyber-Pet Virtual ~*~",
    page_icon="👾",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0714;
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }
    .pet-box {
        border: 2px dashed #ff007f;
        background-color: #1a0033;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        box-shadow: 0px 0px 15px #ff007f;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #ffff00;'>👾 CYBER-PET VIRTUAL IoT 👾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff99ff;'>Ambiente 1: Panel de Control y Alimentación Táctil</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
PORT = 1883

st.markdown('<div class="pet-box">', unsafe_allow_html=True)
st.subheader("🐾 Estado de la Mascota: ¡Activa y Conectada!")
st.write("Usa los botones para enviar comandos físicos a Wokwi:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🍎 Dar de Comer", use_container_width=True):
        try:
            client_id = f"web_{random.randint(1000,9999)}"
            client = paho.Client(client_id=client_id, protocol=paho.MQTTv311)
            client.connect(BROKER, PORT, 60)
            client.publish("cyberpet/accion", "alimentar")
            client.disconnect()
            st.success("¡Comando 'alimentar' enviado al ESP32!")
        except Exception as e:
            st.error(f"Error MQTT: {e}")

with col2:
    if st.button("🎾 Jugar con Mascota", use_container_width=True):
        try:
            client_id = f"web_{random.randint(1000,9999)}"
            client = paho.Client(client_id=client_id, protocol=paho.MQTTv311)
            client.connect(BROKER, PORT, 60)
            client.publish("cyberpet/accion", "saludar")
            client.disconnect()
            st.success("¡Comando 'saludar' enviado al ESP32!")
        except Exception as e:
            st.error(f"Error MQTT: {e}")

st.markdown('</div>', unsafe_allow_html=True)
