import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import paho.mqtt.publish as publish
import random
import av
import io
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

# --- AUTO-REFRESH EN TIEMPO REAL ---
count = st_autorefresh(interval=2000, limit=None, key="voice_tamagotchi_refresher")

# --- ESTILOS VISUALES RETRO / CYBERPUNK ---
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #ff007f;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-shadow: 0px 0px 10px rgba(255, 0, 127, 0.6);
    }
    .description-box {
        text-align: center;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        margin-bottom: 15px;
    }
    .commands-guide {
        background: #1a0033;
        border: 2px dashed #00ffcc;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        text-align: center;
    }
    .tamagotchi-shell {
        background: #0d001a;
        border: 5px solid #ff007f;
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        box-shadow: 0px 0px 50px rgba(255, 0, 127, 0.4);
        margin-bottom: 20px;
    }
    .pet-name-banner {
        color: #00ffcc;
        font-family: 'Courier New', monospace;
        font-size: 26px;
        font-weight: bold;
        text-shadow: 0px 0px 8px rgba(0, 255, 204, 0.6);
        margin-bottom: 15px;
        letter-spacing: 2px;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff007f , #00ffcc);
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 class='main-title'>🎙️ CONTROL POR VOZ - CYBER-PET</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='description-box'>
    Controla a tu mascota virtual exclusivamente mediante tu voz. ¡Habla claro para enviar comandos al Wokwi!
</div>
""", unsafe_allow_html=True)

# --- GUÍA DE COMANDOS PERMITIDOS ---
st.markdown("""
<div class='commands-guide'>
    <b>📌 COMANDOS DE VOZ VÁLIDOS:</b><br>
    • Para alimentar: <i>"alimentar"</i> o <i>"comer"</i><br>
    • Para jugar: <i>"saludar"</i> o <i>"jugar"</i><br>
    • Para curar: <i>"medicina"</i> o <i>"curar"</i><br>
    • Para descansar: <i>"dormir"</i>, <i>"descansar"</i> o <i>"apagar"</i>
</div>
""", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

# --- SINCRONIZACIÓN DE ESTADOS (SESSION STATE) ---
if "pet_name" not in st.session_state:
    st.session_state.pet_name = "CyberKitty"
if "hambre" not in st.session_state:
    st.session_state.hambre = 100
if "felicidad" not in st.session_state:
    st.session_state.felicidad = 100
if "energia" not in st.session_state:
    st.session_state.energia = 100
if "estado_mascota" not in st.session_state:
    st.session_state.estado_mascota = "normal"
if "expiracion_animacion" not in st.session_state:
    st.session_state.expiracion_animacion = 0
if "ultimo_audio_procesado" not in st.session_state:
    st.session_state.ultimo_audio_procesado = None
if "ultimo_refresco" not in st.session_state:
    st.session_state.ultimo_refresco = time.time()

# --- LÓGICA DE TIEMPO REAL (ESTADÍSTICAS Y ANIMACIONES) ---
tiempo_actual = time.time()
tiempo_transcurrido = tiempo_actual - st.session_state.ultimo_refresco
st.session_state.ultimo_refresco = tiempo_actual

# Restablecer estado normal si expiraron los 3 segundos de animación temporal
if tiempo_actual > st.session_state.expiracion_animacion and st.session_state.estado_mascota in ["alimentar", "medicina", "saludar"]:
    st.session_state.estado_mascota = "normal"

if st.session_state.estado_mascota != "muerto":
    if st.session_state.estado_mascota == "durmiendo":
        st.session_state.energia = min(100, st.session_state.energia + (tiempo_transcurrido * 2.0))
        st.session_state.hambre = max(0, st.session_state.hambre - (tiempo_transcurrido * 0.2))
    else:
        tasa = 0.4
        st.session_state.hambre = max(0, st.session_state.hambre - (tiempo_transcurrido * tasa))
        st.session_state.felicidad = max(0, st.session_state.felicidad - (tiempo_transcurrido * (tasa * 0.8)))
        st.session_state.energia = max(0, st.session_state.energia - (tiempo_transcurrido * (tasa * 0.6)))

    if st.session_state.hambre <= 0 or st.session_state.felicidad <= 0 or st.session_state.energia <= 0:
        st.session_state.estado_mascota = "muerto"

# --- INTERFAZ VISUAL TIPO TAMAGOTCHI ---
with st.container():
    st.markdown("<div class='tamagotchi-shell'>", unsafe_allow_html=True)
    
    nombre_mostrado = st.session_state.pet_name.strip() if st.session_state.pet_name else "Cyber-Pet"
    st.markdown(f"<div class='pet-name-banner'>🐾 {nombre_mostrado.upper()} 🐾</div>", unsafe_allow_html=True)
    
    avatar_path = f"assets/{st.session_state.estado_mascota}.jpeg"
    
    col_pantalla_centro = st.columns([1, 4, 1])
    with col_pantalla_centro[1]:
        try:
            st.image(avatar_path, width=350)
        except:
            st.markdown(f"### 🐾 Estado Actual: {st.session_state.estado_mascota.upper()}")
            st.caption(f"Falta el archivo '{st.session_state.estado_mascota}.jpeg' en assets/")

    st.markdown("---")
    
    # 3 ESTADÍSTICAS VITALES
    st.markdown("### 📊 ESTADÍSTICAS VITALES")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"🍎 **Hambre:** {int(st.session_state.hambre)}%")
        st.progress(int(st.session_state.hambre))
        
    with col_stat2:
        st.markdown(f"🎾 **Felicidad:** {int(st.session_state.felicidad)}%")
        st.progress(int(st.session_state.felicidad))

    with col_stat3:
        st.markdown(f"⚡ **Energía:** {int(st.session_state.energia)}%")
        st.progress(int(st.session_state.energia))

    if st.session_state.estado_mascota == "muerto":
        st.error(f"💀 ¡ALERTA CRÍTICA! {nombre_mostrado} HA COLAPSADO Y HA MUERTO.")
        if st.button("🔄 REGENERAR / REVIVIR MASCOTA", use_container_width=True):
            st.session_state.hambre = 100
            st.session_state.felicidad = 100
            st.session_state.energia = 100
            st.session_state.estado_mascota = "normal"
            st.session_state.expiracion_animacion = 0
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔴 Control de Micrófono:")

# Componente de grabación
audio_data = mic_recorder(
    start_prompt="🔴 Iniciar Micrófono (Hablar)",
    stop_prompt="⏹️ Detener y Transcribir",
    just_once=False,
    key='transcriptor_nativo_real'
)

if audio_data:
    webm_bytes = audio_data['bytes']
    
    # Creamos un identificador único (hash simple) para este audio exacto
    audio_id = hash(webm_bytes)
    
    # Verificamos si este audio ya fue procesado antes para evitar bucles o ejecuciones repetidas
    if st.session_state.ultimo_audio_procesado != audio_id:
        st.session_state.ultimo_audio_procesado = audio_id  # Lo marcamos como procesado inmediatamente
        
        st.info("🔄 Procesando y transcribiendo tu voz...")
        
        try:
            # Conversión intacta con PyAV
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
            
            # Filtrado de comandos por única vez
            texto_lower = texto_transcrito.lower().strip()
            comando = ""
            
            if st.session_state.estado_mascota == "muerto":
                st.warning("⚠️ Mascota inactiva. Debes revivirla en el panel superior antes de usar comandos de voz.")
            else:
                if "alimentar" in texto_lower or "comer" in texto_lower:
                    comando = "alimentar"
                    st.session_state.estado_mascota = "alimentar"
                    st.session_state.expiracion_animacion = time.time() + 3
                    st.session_state.hambre = min(100, st.session_state.hambre + 30)
                elif "saludar" in texto_lower or "jugar" in texto_lower:
                    comando = "saludar"
                    st.session_state.estado_mascota = "saludar"
                    st.session_state.expiracion_animacion = time.time() + 3
                    st.session_state.felicidad = min(100, st.session_state.felicidad + 30)
                    st.session_state.energia = max(0, st.session_state.energia - 10)
                elif "medicina" in texto_lower or "curar" in texto_lower:
                    comando = "saludar"
                    st.session_state.estado_mascota = "medicina"
                    st.session_state.expiracion_animacion = time.time() + 3
                    st.session_state.energia = min(100, st.session_state.energia + 20)
                    st.session_state.felicidad = min(100, st.session_state.felicidad + 15)
                elif "dormir" in texto_lower or "descansar" in texto_lower or "apagar" in texto_lower:
                    comando = "alimentar"
                    if st.session_state.estado_mascota == "durmiendo":
                        st.session_state.estado_mascota = "normal"
                    else:
                        st.session_state.estado_mascota = "durmiendo"
                        st.session_state.expiracion_animacion = 0

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
                        st.success(f"🚀 ¡Señal '{comando}' enviada con éxito al Wokwi!")
                    except Exception as mqtt_err:
                        st.error(f"❌ Error al enviar la señal MQTT: {mqtt_err}")
                else:
                    st.warning(f"⚠️ Dijiste '{texto_transcrito}', pero no es un comando válido. No se envió ninguna señal.")
                
        except sr.UnknownValueError:
            st.warning("⚠️ El micrófono se activó, pero no se entendió ninguna palabra clara. Intenta hablar más cerca.")
        except Exception as e:
            st.error(f"❌ Error al procesar el audio: {e}")
