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
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Validar que el micrófono funcione y transcriba lo que dices</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Haz clic en el botón para hablar:")

# Este componente activa el micrófono del navegador y graba el audio en bruto
audio_info = mic_recorder(
    start_prompt="🎙️ Iniciar Grabación",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_voz'
)

if audio_info:
    # Mostramos el reproductor para que escuches lo que grabó tu micrófono
    st.audio(audio_info['bytes'])
    st.info("🔄 Procesando audio en el servidor...")
    
    try:
        # Procesamos el audio grabado mediante la API de Google Speech de forma interna
        r = sr.Recognizer()
        audio_file = sr.AudioFile(io.BytesIO(audio_info['bytes']))
        
        with audio_file as source:
            audio_data = r.record(source)
            # Transcribimos en español
            texto_transcrito = r.recognize_google(audio_data, language="es-ES")
            
            # Mostramos el resultado exacto en pantalla
            st.success("¡Transcripción exitosa!")
            st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Dijiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
    except sr.UnknownValueError:
        st.error("⚠️ El micrófono se activó, pero no se alcanzó a entender ninguna palabra clara. Intenta hablar más cerca.")
    except sr.RequestError as e:
        st.error(f"❌ Error de conexión con el servicio de transcripción: {e}")
