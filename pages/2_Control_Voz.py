import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile
import os

st.set_page_config(
    page_title="Transcriptor de Voz Real",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ EN TIEMPO REAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Transcripción especializada de audio</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Control de Micrófono:")
st.markdown("Haz clic en el botón para activar el micrófono de tu dispositivo.")

# Grabador nativo del navegador
audio_data = mic_recorder(
    start_prompt="🔴 Iniciar Micrófono (Hablar)",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_nativo_real'
)

if audio_data:
    st.info("🔄 Procesando audio con motor especializado...")
    
    try:
        audio_bytes = audio_data['bytes']
        
        # Guardamos los bytes en un archivo temporal real en disco (.webm/.wav)
        # para que SpeechRecognition lo lea de forma nativa sin requerir pydub ni ffprobe
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name

        try:
            r = sr.Recognizer()
            with sr.AudioFile(tmp_file_path) as source:
                audio_leido = r.record(source)
                # Usamos el motor de reconocimiento web especializado
                texto_transcrito = r.recognize_google(audio_leido, language="es-ES")
                
            st.success("¡Transcripción exitosa!")
            st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Transcribiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
        except Exception as inner_err:
            st.error(f"❌ Error en la lectura del archivo de audio: {inner_err}")
            
        finally:
            # Limpiamos el archivo temporal del servidor
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
                
    except Exception as e:
        st.error(f"❌ Error general en el proceso: {e}")
