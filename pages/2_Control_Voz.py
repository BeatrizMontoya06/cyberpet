import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ INTERFAZ DE VOZ MULTIMODAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Habla con tu mascota virtual en tiempo real</p>", unsafe_allow_html=True)

# Componente de voz interactivo real con micrófono y efectos visuales de escucha
voice_component = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <style>
        .voice-box {
            background: rgba(26, 0, 51, 0.7);
            border: 2px dashed #ff007f;
            padding: 30px;
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
            padding: 16px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 40px;
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
        #output-text {
            margin-top: 20px;
            font-size: 18px;
            color: #ffff00;
            font-weight: bold;
        }
        #status-msg {
            margin-top: 10px;
            font-size: 14px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="voice-box">
    <button id="micButton" class="mic-btn" onclick="toggleListening()">🎙️ Activar Micrófono</button>
    <div id="status-msg">Haz clic para empezar a hablar con tu mascota</div>
    <div id="output-text">Escuchando: (ninguna orden aún)</div>
</div>

<script>
    let recognition;
    let isListening = false;

    function initSpeech() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            document.getElementById('status-msg').innerHTML = "❌ Tu navegador no soporta reconocimiento de voz nativo. Usa Google Chrome.";
            return null;
        }

        const rec = new SpeechRecognition();
        rec.lang = 'es-ES';
        rec.continuous = false;
        rec.interimResults = false;

        rec.onstart = function() {
            isListening = true;
            document.getElementById('micButton').className = "mic-btn listening";
            document.getElementById('micButton').innerHTML = "🔴 Escuchando voz...";
            document.getElementById('status-msg').innerHTML = "Di un comando: <b>'Alimentar'</b> o <b>'Saludar'</b>";
        };

        rec.onresult = function(event) {
            const speech = event.results[0][0].transcript.toLowerCase().trim();
            document.getElementById('output-text').innerHTML = "🗣️ Dijiste: \"" + speech + "\"";
            
            let accion = "";
            if (speech.includes("alimentar") || speech.includes("comer") || speech.includes("comida")) {
                accion = "alimentar";
            } else if (speech.includes("saludar") || speech.includes("jugar") || speech.includes("hola")) {
                accion = "saludar";
            }

            if (accion) {
                document.getElementById('status-msg').innerHTML = "✅ Comando válido detectado: " + accion;
                enviarMQTT(accion);
            } else {
                document.getElementById('status-msg').innerHTML = "⚠️ Comando no reconocido. Prueba de nuevo.";
            }
        };

        rec.onerror = function(event) {
            document.getElementById('status-msg').innerHTML = "❌ Error de micrófono o red: " + event.error;
            stopListeningVisual();
        };

        rec.onend = function() {
            stopListeningVisual();
        };

        return rec;
    }

    function toggleListening() {
        if (!recognition) {
            recognition = initSpeech();
        }
        if (!recognition) return;

        if (!isListening) {
            try {
                recognition.start();
            } catch(e) {
                recognition.stop();
            }
        } else {
            recognition.stop();
        }
    }

    function stopListeningVisual() {
        isListening = false;
        const btn = document.getElementById('micButton');
        if(btn) {
            btn.className = "mic-btn";
            btn.innerHTML = "🎙️ Activar Micrófono";
        }
    }

    function enviarMQTT(accion) {
        document.getElementById('status-msg').innerHTML = "📡 Transmitiendo orden a Wokwi...";
        var client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "voice_real_" + Math.floor(Math.random() * 100000));
        
        client.connect({
            onSuccess: function () {
                var message = new Paho.MQTT.Message(accion);
                message.destinationName = "cyberpet/accion";
                client.send(message);
                document.getElementById('status-msg').innerHTML = "🚀 ¡Orden '" + accion + "' enviada al circuito!";
                setTimeout(function(){ client.disconnect(); }, 600);
            },
            onFailure: function (e) {
                document.getElementById('status-msg').innerHTML = "❌ Error al conectar al broker MQTT.";
            }
        });
    }
</script>

</body>
</html>
"""

components.html(voice_component, height=230)
