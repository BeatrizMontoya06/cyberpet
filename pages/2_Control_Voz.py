import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import av
import io

st.set_page_config(
    page_title="Transcriptor de Voz Real",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ EN TIEMPO REAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Transcripción directa de voz a texto</p>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Control de Micrófono:")
st.markdown("Haz clic en el botón para activar el micrófono de tu dispositivo y decir una palabra.")

# Componente nativo que abre el micrófono real del navegador
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
        
        # Convertimos el formato WebM del navegador a WAV puro en memoria usando PyAV
        # (Esto evita totalmente el error de 'ffprobe' porque PyAV trae su propio conversor interno)
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
        
        # Procesamos el archivo WAV limpio con SpeechRecognition
        r = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
            audio_leido = r.record(source)
            texto_transcrito = r.recognize_google(audio_leido, language="es-ES")
            
        # Mostramos el resultado exacto en pantalla tal como lo pediste
        st.success("¡Transcripción exitosa!")
        st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Dijiste: \"{texto_transcrito}\"</h3>", unsafe_allow_html=True)
        
        # Validación opcional para el siguiente paso con Wokwi
        texto_lower = texto_transcrito.lower().strip()
        if "alimentar" in texto_lower:
            st.info("🎯 ¡Palabra clave detectada: ALIMENTAR!")
        elif "saludar" in texto_lower:
            st.info("🎯 ¡Palabra clave detectada: SALUDAR!")
        else:
            st.warning(f"⚠️ Dijiste '{texto_transcrito}', pero no es un comando de control válido.")
            
    except sr.UnknownValueError:
        st.warning("⚠️ El micrófono se activó y grabó, pero no se entendió ninguna palabra clara. Intenta hablar más cerca.")
    except Exception as e:
        st.error(f"❌ Error al procesar el audio: {e}")
