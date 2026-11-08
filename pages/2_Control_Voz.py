import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import io

st.set_page_config(
    page_title="Transcriptor de Voz",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ A TEXTO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Validar transcripción limpia de voz</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Haz clic en el botón para hablar:")

audio_info = mic_recorder(
    start_prompt="🎙️ Iniciar Grabación",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_voz'
)

if audio_info:
    st.audio(audio_info['bytes'])
    st.info("🔄 Convirtiendo y procesando audio...")
    
    try:
        # Convertimos los bytes de WebM a formato WAV estándar usando pydub
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_info['bytes']))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        
        # Procesamos con SpeechRecognition
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = r.record(source)
            texto_transcrito = r.recognize_google(audio_data, language="es-ES")
            
            st.success("¡Transcripción exitosa!")
            st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Dijiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"⚠️ Error al procesar el audio: {e}")
