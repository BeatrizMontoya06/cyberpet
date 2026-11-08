import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Transcriptor de Voz",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ff007f;'>🎙️ TRANSCRIPTOR DE VOZ DIRECTO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>Paso 1: Habla y observa la transcripción exacta en texto</p>", unsafe_allow_html=True)

# Componente web puro con la API de voz del navegador (SpeechRecognition)
transcriptor_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .card {
            background: rgba(26, 0, 51, 0.9);
            border: 2px solid #ff007f;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-family: monospace;
            box-shadow: 0px 0px 25px rgba(255, 0, 127, 0.4);
            margin-top: 20px;
        }
        .btn-hablar {
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
        .btn-hablar:hover {
            background-color: #00ffcc;
            color: #1a0033;
            box-shadow: 0px 0px 25px #00ffcc;
            transform: scale(1.05);
        }
        .escuchando {
            animation: pulse 1.2s infinite;
            background-color: #00ffcc !important;
            color: #1a0033 !important;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.8); }
            70% { box-shadow: 0 0 0 20px rgba(0, 255, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
        #resultado {
            margin-top: 25px;
            font-size: 22px;
            color: #ffff00;
            font-weight: bold;
        }
        #estado {
            margin-top: 15px;
            font-size: 15px;
            color: #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="card">
    <button id="micBtn" class="btn-hablar" onclick="iniciarTranscripcion()">🎙️ Iniciar Transcripción</button>
    <div id="estado">Haz clic para activar el micrófono y hablar...</div>
    <div id="resultado">🗣️ Texto transcrito: (esperando voz)</div>
</div>

<script>
    function iniciarTranscripcion() {
        const estadoDiv = document.getElementById('estado');
        const resultadoDiv = document.getElementById('resultado');
        const btn = document.getElementById('micBtn');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            estadoDiv.innerHTML = "❌ Tu navegador no soporta esta función. Usa Google Chrome.";
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            btn.className = "btn-hablar escuchando";
            btn.innerHTML = "🔴 Escuchando...";
            estadoDiv.innerHTML = "🎧 Te escucho... Di cualquier palabra.";
            resultadoDiv.innerHTML = "🗣️ Texto transcrito: ...";
        };

        recognition.onresult = function(event) {
            // Captura EXACTAMENTE lo que dijiste en texto plano
            const textoVoz = event.results[0][0].transcript.toLowerCase().trim();
            
            // Muestra abajo el texto exacto
            resultadoDiv.innerHTML = "🗣️ Texto transcrito: \"" + textoVoz + "\"";
            estadoDiv.innerHTML = "✅ ¡Transcripción completada con éxito!";
        };

        recognition.onerror = function(event) {
            estadoDiv.innerHTML = "❌ Error con el micrófono: " + event.error;
            resetearBoton();
        };

        recognition.onend = function() {
            resetearBoton();
        };

        recognition.start();
    }

    function resetearBoton() {
        const btn = document.getElementById('micBtn');
        if(btn) {
            btn.className = "btn-hablar";
            btn.innerHTML = "🎙️ Iniciar Transcripción";
        }
    }
</script>

</body>
</html>
"""

components.html(transcriptor_html, height=270)
