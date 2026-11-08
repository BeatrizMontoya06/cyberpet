import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Voz Real - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ REAL Y DIRECTO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Habla para activar la mascota y controlar el circuito al instante</p>", unsafe_allow_html=True)

# Componente HTML con reconocimiento de voz real (SpeechRecognition) y envío MQTT vía WebSocket
voice_recognition_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <style>
        .container {
            background: rgba(26, 0, 51, 0.9);
            border: 2px solid #ff007f;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-family: monospace;
            box-shadow: 0px 0px 25px rgba(255, 0, 127, 0.5);
            margin-top: 20px;
        }
        .mic-btn {
            background-color: #ff007f;
            color: #ffffff;
            border: 2px solid #00ffcc;
            padding: 18px 36px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0px 0px 15px #ff007f;
            transition: all 0.2s ease;
        }
        .mic-btn:hover {
            background-color: #00ffcc;
            color: #1a0033;
            box-shadow: 0px 0px 30px #00ffcc;
            transform: scale(1.05);
        }
        .listening {
            animation: pulse 1.2s infinite;
            background-color: #00ffcc !important;
            color: #1a0033 !important;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.8); }
            70% { box-shadow: 0 0 0 25px rgba(0, 255, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
        #transcript {
            margin-top: 20px;
            font-size: 20px;
            color: #ffff00;
            font-weight: bold;
        }
        #status {
            margin-top: 15px;
            font-size: 16px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="container">
    <button id="micBtn" class="mic-btn" onclick="activarMicrofono()">🎙️ Presionar para Hablar</button>
    <div id="status">Haz clic en el botón y di 'alimentar' o 'saludar'</div>
    <div id="transcript">🗣️ Dijiste: (esperando voz...)</div>
</div>

<script>
    function activarMicrofono() {
        const statusDiv = document.getElementById('status');
        const transcriptDiv = document.getElementById('transcript');
        const btn = document.getElementById('micBtn');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            statusDiv.innerHTML = "❌ Tu navegador no soporta voz. Usa Google Chrome.";
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            btn.className = "mic-btn listening";
            btn.innerHTML = "🔴 Escuchando...";
            statusDiv.innerHTML = "🎧 Te escucho claramente... Di tu comando.";
            transcriptDiv.innerHTML = "🗣️ Dijiste: ...";
        };

        recognition.onresult = function(event) {
            const textoVoz = event.results[0][0].transcript.toLowerCase().trim();
            
            // Muestra exactamente lo que dijiste abajo en pantalla
            transcriptDiv.innerHTML = "🗣️ Dijiste: \"" + textoVoz + "\"";
            
            let comando = "";
            if (textoVoz.includes("alimentar") || textoVoz.includes("comer") || textoVoz.includes("comida")) {
                comando = "alimentar";
            } else if (textoVoz.includes("saludar") || textoVoz.includes("jugar") || textoVoz.includes("hola")) {
                comando = "saludar";
            }

            if (comando) {
                statusDiv.innerHTML = "✅ Comando detectado: <b>" + comando + "</b>. Enviando a Wokwi...";
                enviarMQTT(comando);
            } else {
                statusDiv.innerHTML = "⚠️ No reconocido. Di 'alimentar' o 'saludar'.";
            }
        };

        recognition.onerror = function(event) {
            statusDiv.innerHTML = "❌ Error en el micrófono: " + event.error;
            resetButton();
        };

        recognition.onend = function() {
            resetButton();
        };

        recognition.start();
    }

    function resetButton() {
        const btn = document.getElementById('micBtn');
        if(btn) {
            btn.className = "mic-btn";
            btn.innerHTML = "🎙️ Presionar para Hablar";
        }
    }

    function enviarMQTT(accion) {
        // Conexión por WebSocket directa al broker para mover el circuito al instante
        var client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "voice_real_" + Math.floor(Math.random() * 100000));
        
        client.connect({
            onSuccess: function () {
                var message = new Paho.MQTT.Message(accion);
                message.destinationName = "cyberpet/accion";
                client.send(message);
                document.getElementById('status').innerHTML = "🚀 ¡Orden '" + accion + "' enviada con éxito al circuito!";
                setTimeout(function(){ client.disconnect(); }, 600);
            },
            onFailure: function (e) {
                document.getElementById('status').innerHTML = "❌ Error al enviar al broker MQTT.";
            }
        });
    }
</script>

</body>
</html>
"""

components.html(voice_recognition_code, height=270)
