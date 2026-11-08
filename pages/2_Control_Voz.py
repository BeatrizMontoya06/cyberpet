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

# Grabador nativo que dispara el permiso real del navegador
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
        audio_bytes = audio_data['bytes']
        
        # Como los bytes vienen directo de la grabación web en formato contenedor compatible con SpeechRecognition usando BytesIO con formato de audio crudo:
        audio_file_obj = io.BytesIO(audio_bytes)
        
        # Usamos el reconocimiento directamente sobre el flujo de bytes de audio abierto por la librería
        with sr.AudioFile(audio_file_obj) as source:
            audio_leido = r.record(source)
            texto_transcrito = r.recognize_google(audio_leido, language="es-ES")
            
        # Mostramos el resultado en pantalla tal como lo pediste
        st.success("¡Transcripción exitosa!")
        st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Transcribiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
    except sr.UnknownValueError:
        st.warning("⚠️ El micrófono se activó y grabó, pero no se entendió ninguna palabra clara. Intenta hablar más cerca.")
    except Exception as e:
        # En caso de que el contenedor requiera lectura directa de Stream crudo por incompatibilidad de cabeceras WAV:
        try:
            r = sr.Recognizer()
            # Forzamos lectura por stream de datos de audio webm nativo
            audio_data_directo = sr.AudioData(audio_data['bytes'], 44100, 2)
            texto_transcrito = r.recognize_google(audio_data_directo, language="es-ES")
            st.success("¡Transcripción exitosa!")
            st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Transcribiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
        except Exception as err_final:
            st.error(f"❌ Error de formato en los bytes de audio: {err_final}")
