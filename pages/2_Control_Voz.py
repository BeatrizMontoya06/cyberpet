import streamlit as st
import paho.mqtt.publish as publish
import random
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io

st.set_page_config(
    page_title="Control por Voz Real - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ REAL Y DIRECTO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Haz clic en el botón, acepta el permiso del micrófono y habla con tu mascota</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

st.markdown("""
### 🎯 Instrucciones:
1. Haz clic en el botón de abajo (**"🎙️ Activar Micrófono"**).
2. El navegador **te pedirá obligatoriamente el permiso de hardware** (dale a *Permitir*).
3. Di tu palabra (ej. *"hola"*, *"alimentar"*, *"saludar"*).
""")

# Este componente nativo FUERZA al navegador de tu PC o celular a abrir el permiso de micrófono de forma real
audio_data = mic_recorder(
    start_prompt="🎙️ Activar Micrófono y Hablar",
    stop_prompt="⏹️ Procesar Voz",
    just_once=False,
    key='mic_real_voz'
)

if audio_data:
    # Obtenemos los bytes del audio grabado por tu micrófono real
    audio_bytes = audio_data['bytes']
    
    st.info("🔄 Procesando tu voz y transcribiendo...")
    
    # Usamos SpeechRecognition de Python para analizar lo que dijiste con el micrófono
    r = sr.Recognizer()
    audio_file = sr.AudioFile(io.BytesIO(audio_bytes))
    
    texto_reconocido = ""
    try:
        with audio_file as source:
            audio_leido = r.record(source)
            # Intentamos reconocer en español
            texto_reconocido = r.recognize_google(audio_leido, language="es-ES").lower().strip()
            
        # Mostramos exactamente lo que dijiste abajo en pantalla
        st.markdown(f"<h3 style='color: #ffff00; text-align: center;'>🗣️ Transcripción: \"{texto_reconocido}\"</h3>", unsafe_allow_html=True)
        
        # Filtramos el comando tal como lo pediste
        if "alimentar" in texto_reconocido or "comer" in texto_reconocido:
            comando = "alimentar"
        elif "saludar" in texto_reconocido or "jugar" in texto_reconocido:
            comando = "saludar"
        else:
            comando = ""

        if comando:
            st.success(f"✅ ¡Comando válido detectado ('{comando}')! Enviando orden a Wokwi...")
            try:
                publish.single(
                    topic=TOPIC,
                    payload=comando,
                    hostname=BROKER,
                    port=1883,
                    client_id=f"voice_real_{random.randint(1000,9999)}"
                )
                st.balloons()
                st.success("🚀 ¡Circuito accionado con éxito en Wokwi!")
            except Exception as e:
                st.error(f"Error de red MQTT: {e}")
        else:
            st.warning(f"⚠️ Dijiste \"{texto_reconocido}\", pero no es un comando válido. Wokwi no hizo nada.")
            
    except sr.UnknownValueError:
        st.error("❌ No se pudo entender el audio. Intenta hablar más cerca del micrófono.")
    except sr.RequestError as e:
        st.error(f"❌ Error con el servicio de reconocimiento: {e}")
