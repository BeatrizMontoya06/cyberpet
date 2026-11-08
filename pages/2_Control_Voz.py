import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ DEL CYBER-PET</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Habla con tu mascota virtual para controlarla en tiempo real</p>", unsafe_allow_html=True)

st.markdown("""
### 📋 Comandos de voz disponibles:
* 🍎 **"Alimentar"** (o *"comer"*): Activa la comida de la mascota.
* 🎾 **"Saludar"** (o *"jugar"*): Activa la interacción de juego.
""")

voice_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <style>
        .voice-container {
            text-align: center;
            margin-top: 25px;
            font-family: monospace;
        }
        .voice-btn {
            background-color: #ff007f;
            color: #ffffff;
            border: 2px solid #00ffcc;
            padding: 16px 32px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0px 0px 15px #ff007f;
            transition: all 0.3s ease;
        }
        .voice-btn:hover {
            background-color: #00ffcc;
            color: #1a0033;
            box-shadow: 0px 0px 25px #00ffcc;
        }
        #transcript {
            margin-top: 15px;
            font-size: 16px;
            color: #ffff00;
        }
        #status-voz {
            margin-top: 12px;
            font-size: 15px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="voice-container">
    <button class="voice-btn" onclick="startListening()">🎙️ Presionar para Hablar</button>
    <div id="status-voz">Haz clic en el botón y da una orden...</div>
    <div id="transcript"></div>
</div>

<script>
    function startListening() {
        const statusDiv = document.getElementById('status-voz');
        const transcriptDiv = document.getElementById('transcript');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            statusDiv.innerHTML = "❌ Tu navegador no soporta reconocimiento de voz. Usa Google Chrome.";
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            statusDiv.innerHTML = "🎧 Escuchando... Di 'alimentar' o 'saludar'";
            transcriptDiv.innerHTML = "";
        };

        recognition.onresult = function(event) {
            const speechResult = event.results[0][0].transcript.toLowerCase();
            transcriptDiv.innerHTML = "🗣️ Reconocido: <b>" + speechResult + "</b>";
            
            let comandoFinal = "";
            if (speechResult.includes("alimentar") || speechResult.includes("comer")) {
                comandoFinal = "alimentar";
            } else if (speechResult.includes("saludar") || speechResult.includes("jugar")) {
                comandoFinal = "saludar";
            }

            if (comandoFinal) {
                enviarMQTT(comandoFinal);
            } else {
                statusDiv.innerHTML = "⚠️ No reconocido. Prueba diciendo 'alimentar' o 'saludar'.";
            }
        };

        recognition.onerror = function(event) {
            statusDiv.innerHTML = "❌ Error en el micrófono: " + event.error;
        };

        recognition.start();
    }

    function enviarMQTT(accion) {
        var statusDiv = document.getElementById('status-voz');
        statusDiv.innerHTML = "📡 Enviando orden de voz (" + accion + ") a Wokwi...";
        
        var client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "voice_client_" + Math.floor(Math.random() * 100000));
        
        client.connect({
            onSuccess: function () {
                var message = new Paho.MQTT.Message(accion);
                message.destinationName = "cyberpet/accion";
                client.send(message);
                statusDiv.innerHTML = "✅ ¡Orden por voz '" + accion + "' enviada a Wokwi!";
                setTimeout(function(){ client.disconnect(); }, 500);
            },
            onFailure: function (e) {
                statusDiv.innerHTML = "❌ Error MQTT: " + e.errorMessage;
            }
        });
    }
</script>

</body>
</html>
"""

# IMPORTANTE: Añadimos allow="microphone" para que el navegador permita el acceso al hardware
components.html(voice_html, height=240, allow="microphone")
