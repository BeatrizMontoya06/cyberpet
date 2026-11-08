import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import paho.mqtt.publish as publish
import random
import av
import io

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ Y WOKWI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Transcripción en tiempo real y envío de comandos MQTT</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

st.write("---")
st.markdown("### 🔴 Control de Micrófono:")
st.markdown("Haz clic en el botón para activar el micrófono y ordenar una acción.")

# Componente nativo de grabación que ya te funciona perfectamente
audio_data = mic_recorder(
    start_prompt="🔴 Iniciar Micrófono (Hablar)",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_nativo_real'
)

if audio_data:
    st.info("🔄 Procesando y transcribiendo tu voz...")
    
    try:
        webm_bytes = audio_data['bytes']
        
        # Conversión intacta con PyAV que ya te transcribió bien
        input_container = av.open(io.BytesIO(webm_bytes), mode='r')
        output_buffer = io.BytesIO()
        
        output_container = av.open(output_buffer, mode='w', format='wav')
        in_stream = input_container.streams.audio[0]
        out_stream = output_container.add_stream('pcm_s16le', rate=16000, layout='mono')
        
        for frame in input_container.decode(in_stream):
            for packet in out_stream.encode(frame):
                output_container.mux(packet)
                
        for packet in out_stream.encode():
            output_container.mux(packet)
            
        output_container.close()
        wav_bytes = output_buffer.getvalue()
        
        # Reconocimiento de voz
        r = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
            audio_leido = r.record(source)
            texto_transcrito = r.recognize_google(audio_leido, language="es-ES")
            
        st.success("¡Transcripción exitosa!")
        st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Dijiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
        
        # Filtrado de comandos y envío automático a Wokwi vía MQTT
        texto_lower = texto_transcrito.lower().strip()
        comando = ""
        
        if "alimentar" in texto_lower or "comer" in texto_lower:
            comando = "alimentar"
        elif "saludar" in texto_lower or "jugar" in texto_lower:
            comando = "saludar"

        if comando:
            st.info(f"🎯 ¡Comando válido detectado ('{comando}'). Enviando señal a Wokwi...")
            try:
                publish.single(
                    topic=TOPIC,
                    payload=comando,
                    hostname=BROKER,
                    port=1883,
                    client_id=f"voice_client_{random.randint(1000,9999)}"
                )
                st.success(f"🚀 ¡Señál '{comando}' enviada con éxito al Wokwi!")
            except Exception as mqtt_err:
                st.error(f"❌ Error al enviar la señal MQTT: {mqtt_err}")
        else:
            st.warning(f"⚠️ Dijiste '{texto_transcrito}', pero no es un comando válido. No se envió ninguna señal.")
            
    except sr.UnknownValueError:
        st.warning("⚠️ El micrófono se activó, pero no se entendió ninguna palabra clara. Intenta hablar más cerca.")
    except Exception as e:
        st.error(f"❌ Error al procesar el audio: {e}")
