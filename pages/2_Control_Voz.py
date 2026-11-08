import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import imageio_ffmpeg
import io

# Configuramos pydub para que use el ffmpeg empaquetado en Python automáticamente
AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

st.set_page_config(
    page_title="Transcriptor de Voz Real",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ EN TIEMPO REAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Validar activación real del micrófono del dispositivo</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Control de Micrófono:")
st.markdown("Haz clic en el botón de abajo para activar el micrófono de tu PC o celular.")

# Grabador nativo que abre el micrófono real
audio_data = mic_recorder(
    start_prompt="🔴 Iniciar Micrófono (Hablar)",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_nativo_real'
)

if audio_data:
    st.info("🔄 Convirtiendo y procesando tu voz en texto...")
    
    try:
        audio_bytes = audio_data['bytes']
        
        # Convertimos los bytes de WebM (navegador) a WAV PCM estándar usando pydub + imageio-ffmpeg
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        
        # Procesamos el WAV limpio con SpeechRecognition
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_leido = r.record(source)
            texto_transcrito = r.recognize_google(audio_leido, language="es-ES")
            
        # Mostramos el resultado exitoso en pantalla
        st.success("¡Transcripción exitosa!")
        st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Transcribiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
            
    except sr.UnknownValueError:
        st.warning("⚠️ El micrófono grabó con éxito, pero no se entendió ninguna palabra clara. Intenta hablar más cerca.")
    except Exception as e:
        st.error(f"❌ Error al procesar el audio: {e}")
