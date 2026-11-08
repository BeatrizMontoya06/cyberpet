import streamlit as st
import paho.mqtt.client as paho
import random

st.set_page_config(
    page_title="~*~ Cyber-Pet Virtual ~*~",
    page_icon="👾",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ffff00;'>👾 CYBER-PET VIRTUAL IoT 👾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff99ff;'>Panel de Control y Alimentación Táctil</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "cyberpet/accion"

st.subheader("🐾 Estado de la Mascota: Conectada")
st.write("Haz clic para enviar una orden física a Wokwi:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🍎 Dar de Comer", use_container_width=True):
        try:
            client_id = f"web_{random.randint(10000, 99999)}"
            client = paho.Client(client_id=client_id)
            client.connect(BROKER, PORT, 60)
            
            # Publicamos y guardamos el resultado
            info = client.publish(TOPIC, "alimentar")
            info.wait_for_publish() # Espera confirmación de envío
            client.disconnect()
            
            st.success("✅ Mensaje 'alimentar' enviado al canal: " + TOPIC)
        except Exception as e:
            st.error(f"❌ Error al enviar MQTT: {e}")

with col2:
    if st.button("🎾 Jugar con Mascota", use_container_width=True):
        try:
            client_id = f"web_{random.randint(10000, 99999)}"
            client = paho.Client(client_id=client_id)
            client.connect(BROKER, PORT, 60)
            
            info = client.publish(TOPIC, "saludar")
            info.wait_for_publish()
            client.disconnect()
            
            st.success("✅ Mensaje 'saludar' enviado al canal: " + TOPIC)
        except Exception as e:
            st.error(f"❌ Error al enviar MQTT: {e}")
