import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Voz Inteligente - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ RECONOCIMIENTO DE VOZ EN TIEMPO REAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Habla libremente: si dices el comando correcto, la mascota reaccionará</p>", unsafe_allow_html=True)

# Componente web con transcripción de voz real y filtrado de palabras clave
voice_transcription_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <style>
        .voice-card {
            background: rgba(26, 0, 51, 0.9);
            border: 2px solid #00ffcc;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-family: monospace;
            box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.3);
            margin-top: 20px;
        }
        .speak-btn {
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
        .speak-btn:hover {
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
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.8); }
            70% { box-shadow: 0 0 0 20px rgba(0, 255, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
        #transcripcion {
            margin-top: 20px;
            font-size: 20px;
            color: #ffff00;
            font-weight: bold;
            min-height: 30px;
        }
        #estado {
            margin-top: 15px;
            font-size: 16px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="voice-card">
    <button id="btnVoz" class="speak-btn" onclick="iniciarReconocimiento()">🎙️ Hablar con la Mascota</button>
    <div id="estado">Haz clic y di cualquier palabra (ej. 'hola', 'alimentar', 'jugar')</div>
    <div id="transcripcion">🗣️ Transcripción: (esperando voz...)</div>
</div>

<script>
    function iniciarReconocimiento() {
        const estadoDiv = document.getElementById('estado');
        const transcripcionDiv = document.getElementById('transcripcion');
        const boton = document.getElementById('btnVoz');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            estadoDiv.innerHTML = "❌ Tu navegador no soporta reconocimiento de voz. Usa Google Chrome.";
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            boton.className = "speak-btn listening";
            boton.innerHTML = "🔴 Escuchando tu voz...";
            estadoDiv.innerHTML = "🎧 Te escucho con atención...";
            transcripcionDiv.innerHTML = "🗣️ Transcripción: ...";
        };

        recognition.onresult = function(event) {
            // Captura EXACTAMENTE lo que dijiste en texto plano
            const textoTranscrito = event.results[0][0].transcript.toLowerCase().trim();
            
            // Muestra abajo la transcripción exacta de lo que dijiste
            transcripcionDiv.innerHTML = "🗣️ Transcripción: \"" + textoTranscrito + "\"";

            // Filtramos el contenido como lo pediste
            let comandoFinal = "";
            if (textoTranscrito.includes("alimentar") || textoTranscrito.includes("comer")) {
                comandoFinal = "alimentar";
            } else if (textoTranscrito.includes("saludar") || textoTranscrito.includes("jugar")) {
                comandoFinal = "saludar";
            }

            if (comandoFinal) {
                estadoDiv.innerHTML = "✅ ¡Comando válido detectado ('" + comandoFinal + "')! Enviando a Wokwi...";
                enviarOrdenMQTT(comandoFinal);
            } else {
                estadoDiv.innerHTML = "⚠️ Dijiste \"" + textoTranscrito + "\", pero no es un comando válido. Wokwi no hará nada.";
            }
        };

        recognition.onerror = function(event) {
            estadoDiv.innerHTML = "❌ Error en el micrófono: " + event.error;
            restaurarBoton();
        };

        recognition.onend = function() {
            restaurarBoton();
        };

        recognition.start();
    }

    function restaurarBoton() {
        const boton = document.getElementById('btnVoz');
        if(boton) {
            boton.className = "speak-btn";
            boton.innerHTML = "🎙️ Hablar con la Mascota";
        }
    }

    function enviarOrdenMQTT(accion) {
        // Conexión estable por WebSockets al puerto 8000 del broker para accionar el Wokwi al instante
        var client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "client_voz_" + Math.floor(Math.random() * 100000));
        
        client.connect({
            onSuccess: function () {
                var message = new Paho.MQTT.Message(accion);
                message.destinationName = "cyberpet/accion";
                client.send(message);
                document.getElementById('estado').innerHTML = "🚀 ¡Orden '" + accion + "' ejecutada en el circuito con éxito!";
                setTimeout(function(){ client.disconnect(); }, 500);
            },
            onFailure: function (e) {
                document.getElementById('estado').innerHTML = "❌ Error de conexión MQTT con Wokwi.";
            }
        });
    }
</script>

</body>
</html>
"""

components.html(voice_transcription_html, height=270)
