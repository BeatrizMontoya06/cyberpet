import streamlit as st
import paho.mqtt.publish as publish
import random

st.title("👾 Cyber-Pet IoT")

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

if st.button("🍎 Dar de Comer", use_container_width=True):
    try:
        publish.single(
            topic=TOPIC,
            payload="alimentar",
            hostname=BROKER,
            port=1883,
            client_id=f"streamlit_{random.randint(1000,9999)}"
        )
        st.success("¡Mensaje enviado al puerto 1883!")
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("🎾 Jugar", use_container_width=True):
    try:
        publish.single(
            topic=TOPIC,
            payload="saludar",
            hostname=BROKER,
            port=1883,
            client_id=f"streamlit_{random.randint(1000,9999)}"
        )
        st.success("¡Mensaje enviado al puerto 1883!")
    except Exception as e:
        st.error(f"Error: {e}")
