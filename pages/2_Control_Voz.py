import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io

st.set_page_config(
    page_title="Transcriptor de Voz Real",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ EN TIEMPO REAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Validar activación real del micrófono del dispositivo</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Control de Micrófono:")
st.markdown("Haz clic en el botón de abajo. **Este componente sí solicita el permiso nativo del navegador/sistema operativo** para encender el micrófono de tu PC o celular.")

# Usamos el grabador nativo que dispara el permiso real del navegador fuera de iframes
audio_data = mic_recorder(
    start_prompt="🔴 Iniciar Micrófono (Hablar)",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_nativo_real'
)

if audio_data:
    st.info("🔄 Procesando tu voz en texto...")
    
    try:
        r = sr.Recognizer()
        # Leemos los bytes del audio capturado por el micrófono real
        audio_file = sr.AudioFile(io.BytesIO(audio_data['bytes']))
        
        with audio_file as source:
            audio_leido = r.record(source)
            # Transcribimos usando el servicio de Google en español
            texto_transcrito = r.recognize_google(audio_leido, language="es-ES")
            
            # Mostramos el resultado en pantalla tal como lo pediste
            st.success("¡Transcripción exitosa!")
            st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Transcribiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
    except sr.UnknownValueError:
        st.warning("⚠️ El micrófono se activó y grabó, pero no se entendió ninguna palabra clara. Intenta hablar más cerca.")
    except Exception as e:
        st.error(f"❌ Error al procesar el audio: {e}")
