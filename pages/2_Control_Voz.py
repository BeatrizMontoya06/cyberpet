import streamlit as st
import paho.mqtt.publish as publish
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ INTELIGENTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Habla con tu mascota y observa el comando reconocido en tiempo real</p>", unsafe_allow_html=True)

BROKER = "broker.hivemq.com"
TOPIC = "cyberpet/accion"

# Si el navegador detectó la voz y recargó con el comando, lo enviamos a Wokwi
if "cmd" in st.query_params:
    comando_recibido = st.query_params["cmd"]
    try:
        publish.single(
            topic=TOPIC,
            payload=comando_recibido,
            hostname=BROKER,
            port=1883,
            client_id=f"voice_py_{random.randint(1000,9999)}"
        )
        st.success(f"🚀 ¡Orden por voz enviada a Wokwi con éxito: **{comando_recibido}**!")
    except Exception as e:
        st.error(f"Error al enviar MQTT: {e}")
    
    # Limpiamos el parámetro para evitar envíos repetidos al refrescar
    st.query_params.clear()

st.markdown("""
### 📋 Comandos de voz admitidos:
* 🍎 **"Alimentar"** (o *"comer"*)
* 🎾 **"Saludar"** (o *"jugar"*)
""")

# Componente HTML con solicitud forzada de permisos y reconocimiento de voz nativo
voice_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .voice-box {
            background: rgba(26, 0, 51, 0.85);
            border: 2px solid #ff007f;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            font-family: monospace;
            box-shadow: 0px 0px 20px rgba(255, 0, 127, 0.4);
            margin-top: 20px;
        }
        .mic-btn {
            background-color: #ff007f;
            color: #ffffff;
            border: 2px solid #00ffcc;
            padding: 16px 32px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0px 0px 15px #ff007f;
            transition: all 0.2s ease;
        }
        .mic-btn:hover {
            background-color: #00ffcc;
            color: #1a0033;
            box-shadow: 0px 0px 25px #00ffcc;
            transform: scale(1.05);
        }
        .listening {
            animation: pulse 1.2s infinite;
            background-color: #00ffcc !important;
            color: #1a0033 !important;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(0, 255, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
        #transcript {
            margin-top: 18px;
            font-size: 19px;
            color: #ffff00;
            font-weight: bold;
        }
        #status-msg {
            margin-top: 12px;
            font-size: 15px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="voice-box">
    <button id="micButton" class="mic-btn" onclick="startListening()">🎙️ Activar Micrófono</button>
    <div id="status-msg">Haz clic para solicitar permisos y hablar...</div>
    <div id="transcript">Dijiste: (esperando voz)</div>
</div>

<script>
    async function startListening() {
        const statusDiv = document.getElementById('status-msg');
        const transcriptDiv = document.getElementById('transcript');

        // 1. Forzamos la solicitud nativa de permisos del micrófono al navegador
        try {
            statusDiv.innerHTML = "🔒 Solicitando permisos de micrófono...";
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop()); // Liberamos el stream temporal
        } catch (err) {
            statusDiv.innerHTML = "❌ Permiso de micrófono denegado. Habilítalo en el navegador.";
            return;
        }

        // 2. Iniciamos el reconocimiento de voz en español
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            statusDiv.innerHTML = "❌ Tu navegador no soporta reconocimiento de voz. Usa Google Chrome.";
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = function() {
            document.getElementById('micButton').className = "mic-btn listening";
            document.getElementById('micButton').innerHTML = "🔴 Escuchando voz...";
            statusDiv.innerHTML = "🎧 Te escucho... Di 'alimentar' o 'saludar'";
            transcriptDiv.innerHTML = "Dijiste: ...";
        };

        recognition.onresult = function(event) {
            const speech = event.results[0][0].transcript.toLowerCase().trim();
            
            // Abajo muestra exactamente lo que dijiste
            transcriptDiv.innerHTML = "🗣️ Dijiste: \"" + speech + "\"";
            
            let comando = "";
            if (speech.includes("alimentar") || speech.includes("comer")) {
                comando = "alimentar";
            } else if (speech.includes("saludar") || speech.includes("jugar")) {
                comando = "saludar";
            } else {
                comando = speech; // Envia el texto libre si coincide
            }

            statusDiv.innerHTML = "✅ Detectado: <b>" + comando + "</b>. Enviando al circuito...";
            
            // Envía el comando recargando hacia Streamlit para gestionar el envío MQTT de forma segura
            setTimeout(function() {
                window.location.href = window.location.pathname + "?cmd=" + encodeURIComponent(comando);
            }, 900);
        };

        recognition.onerror = function(event) {
            statusDiv.innerHTML = "❌ Error de reconocimiento: " + event.error;
            resetBtn();
        };

        recognition.onend = function() {
            resetBtn();
        };

        recognition.start();
    }

    function resetBtn() {
        const btn = document.getElementById('micButton');
        if(btn) {
            btn.className = "mic-btn";
            btn.innerHTML = "🎙️ Activar Micrófono";
        }
    }
</script>

</body>
</html>
"""

components.html(voice_html, height=250)
