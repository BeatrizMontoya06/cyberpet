import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Voz - Cyber-Pet",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ CONTROL POR VOZ INTELIGENTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Habla con tu mascota virtual: el sistema filtrará tu voz y accionará el Wokwi</p>", unsafe_allow_html=True)

# Componente web directo con la API de Reconocimiento de Voz del navegador
voz_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <style>
        .box {
            background: rgba(26, 0, 51, 0.95);
            border: 2px solid #ff007f;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-family: monospace;
            box-shadow: 0px 0px 30px rgba(255, 0, 127, 0.5);
            margin-top: 20px;
        }
        .mic-btn {
            background-color: #ff007f;
            color: #ffffff;
            border: 2px solid #00ffcc;
            padding: 20px 40px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0px 0px 20px #ff007f;
            transition: all 0.3s ease;
        }
        .mic-btn:hover {
            background-color: #00ffcc;
            color: #1a0033;
            box-shadow: 0px 0px 35px #00ffcc;
            transform: scale(1.05);
        }
        .listening {
            animation: pulse 1.2s infinite;
            background-color: #00ffcc !important;
            color: #1a0033 !important;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.9); }
            70% { box-shadow: 0 0 0 25px rgba(0, 255, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
        #transcripcion {
            margin-top: 25px;
            font-size: 20px;
            color: #ffff00;
            font-weight: bold;
        }
        #estado {
            margin-top: 15px;
            font-size: 16px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="box">
    <button id="btnHablar" class="mic-btn" onclick="iniciarEscucha()">🎙️ Toca para Hablar</button>
    <div id="estado">Haz clic en el botón, acepta el micrófono y da una orden...</div>
    <div id="transcripcion">🗣️ Dijiste: (esperando voz...)</div>
</div>

<script>
    function iniciarEscucha() {
        const estadoDiv = document.getElementById('estado');
        const transDiv = document.getElementById('transcripcion');
        const boton = document.getElementById('btnHablar');

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
            boton.className = "mic-btn listening";
            boton.innerHTML = "🔴 Escuchando...";
            estadoDiv.innerHTML = "🎧 Te escucho... Di 'alimentar' o 'saludar'";
            transDiv.innerHTML = "🗣️ Dijiste: ...";
        };

        recognition.onresult = function(event) {
            const dicho = event.results[0][0].transcript.toLowerCase().trim();
            
            // Muestra exactamente lo que dijiste abajo en pantalla
            transDiv.innerHTML = "🗣️ Dijiste: \"" + dicho + "\"";

            let comando = "";
            if (dicho.includes("alimentar") || dicho.includes("comer")) {
                comando = "alimentar";
            } else if (dicho.includes("saludar") || dicho.includes("jugar")) {
                comando = "saludar";
            }

            if (comando) {
                estadoDiv.innerHTML = "✅ Comando detectado ('" + comando + "'). Enviando a Wokwi...";
                enviarMQTT(comando);
            } else {
                estadoDiv.innerHTML = "⚠️ Dijiste \"" + dicho + "\". No es un comando válido, Wokwi no hace nada.";
            }
        };

        recognition.onerror = function(event) {
            estadoDiv.innerHTML = "❌ Error en el micrófono: " + event.error;
            resetearBoton();
        };

        recognition.onend = function() {
            resetearBoton();
        };

        recognition.start();
    }

    function resetearBoton() {
        const boton = document.getElementById('btnHablar');
        if(boton) {
            boton.className = "mic-btn";
            boton.innerHTML = "🎙️ Toca para Hablar";
        }
    }

    function enviarMQTT(accion) {
        var client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "client_voz_real_" + Math.floor(Math.random() * 100000));
        
        client.connect({
            onSuccess: function () {
                var message = new Paho.MQTT.Message(accion);
                message.destinationName = "cyberpet/accion";
                client.send(message);
                document.getElementById('estado').innerHTML = "🚀 ¡Orden '" + accion + "' enviada al circuito con éxito!";
                setTimeout(function(){ client.disconnect(); }, 500);
            },
            onFailure: function (e) {
                document.getElementById('estado').innerHTML = "❌ Error de conexión MQTT.";
            }
        });
    }
</script>

</body>
</html>
"""

components.html(voz_html, height=280)
