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

st.subheader("🐾 Estado de la Mascota: ¡Activa y Conectada!")
st.write("Usa los botones para enviar comandos físicos a Wokwi:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🍎 Dar de Comer", use_container_width=True):
        try:
            client_id = f"web_client_{random.randint(10000, 99999)}"
            # Usando la sintaxis compatible con Paho MQTT v1 y v2
            client = paho.Client(client_id=client_id)
            client.connect(BROKER, PORT, 60)
            
            # Publicar el mensaje
            resultado = client.publish("cyberpet/accion", "alimentar")
            client.disconnect()
            
            if resultado.rc == paho.MQTT_ERR_SUCCESS:
                st.success("¡Comando 'alimentar' enviado con éxito por MQTT!")
            else:
                st.error("El broker rechazó el mensaje.")
        except Exception as e:
            st.error(f"Error al conectar con MQTT: {e}")

with col2:
    if st.button("🎾 Jugar con Mascota", use_container_width=True):
        try:
            client_id = f"web_client_{random.randint(10000, 99999)}"
            client = paho.Client(client_id=client_id)
            client.connect(BROKER, PORT, 60)
            
            resultado = client.publish("cyberpet/accion", "saludar")
            client.disconnect()
            
            if resultado.rc == paho.MQTT_ERR_SUCCESS:
                st.success("¡Comando 'saludar' enviado con éxito por MQTT!")
            else:
                st.error("El broker rechazó el mensaje.")
        except Exception as e:
            st.error(f"Error al conectar con MQTT: {e}")
