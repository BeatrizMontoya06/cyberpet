import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.client as paho
import random

st.set_page_config(
    page_title="Cyber-Pet // Control de Voz",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ffaa00;'>🎙️ AMBIENTE 2: CONTROL VOCAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff99ff;'>Habla con tu mascota virtual para que mueva sus actuadores físicos.</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
PORT = 1883

stt_button = Button(label="🎙️ HABLAR A LA MASCOTA", width=280, button_type="success")

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="voice_pet",
    refresh_on_update=False,
    override_height=85,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        texto = result.get("GET_TEXT").strip().lower()
        st.success(f"🗣️ Orden detectada: **{texto}**")
        
        try:
            client_id = f"voice_{random.randint(1000,9999)}"
            client = paho.Client(client_id=client_id, protocol=paho.MQTTv311)
            client.connect(BROKER, PORT, 60)
            client.publish("cyberpet/accion", texto)
            client.disconnect()
            st.info("📡 ¡Comando de voz transmitido por MQTT a Wokwi!")
        except Exception as e:
            st.error(f"Error MQTT: {e}")
