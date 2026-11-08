import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io

st.set_page_config(
    page_title="Transcriptor de Voz",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ A TEXTO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Transcripción directa sin dependencias externas</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Haz clic en el botón para hablar:")

# Configuramos el grabador para intentar forzar formato WAV si el navegador lo permite
audio_info = mic_recorder(
    start_prompt="🎙️ Iniciar Grabación",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_voz_limpio'
)

if audio_info:
    st.audio(audio_info['bytes'])
    st.info("🔄 Procesando transcripción...")
    
    try:
        r = sr.Recognizer()
        # Leemos los bytes directamente usando AudioFile con un objeto BytesIO
        with sr.AudioFile(io.BytesIO(audio_info['bytes'])) as source:
            audio_data = r.record(source)
            texto_transcrito = r.recognize_google(audio_data, language="es-ES")
            
            st.success("¡Transcripción exitosa!")
            st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Dijiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
    except Exception as e:
        # Si el navegador grabó en WebM y SpeechRecognition nativo no lo lee sin ffmpeg,
        # te damos la alternativa de texto simulado inmediato para avanzar al control del Wokwi
        st.warning("⚠️ El navegador envió el audio en contenedor comprimido (WebM). Para evitar depender de FFmpeg en el servidor, usa esta consola de prueba rápida de voz:")
        
        texto_manual = st.text_input("Simula o ingresa lo que dijiste con tu voz:", placeholder="ej. alimentar, saludar, hola...")
        if st.button("Procesar Texto Transcrito"):
            if texto_manual:
                st.markdown(f"<h3 style='color: #00ffcc; text-align: center;'>✅ Texto procesado: \"{texto_manual.lower().strip()}\"</h3>", unsafe_allow_html=True)
