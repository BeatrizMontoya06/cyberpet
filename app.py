import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="~*~ Cyber-Pet Virtual ~*~",
    page_icon="👾",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #ffff00;'>👾 CYBER-PET VIRTUAL IoT 👾</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff99ff;'>Panel de Control y Alimentación Táctil</p>", unsafe_allow_html=True)

st.subheader("🐾 Estado de la Mascota: Conectada")
st.write("Haz clic en los botones para controlar el circuito físico en Wokwi:")

# Componente web que envía las órdenes por MQTT a través del navegador
mqtt_js_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js" type="text/javascript"></script>
    <style>
        .btn-container {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 15px;
        }
        .cyber-btn {
            background-color: #1a0033;
            color: #00ffcc;
            border: 2px solid #ff007f;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0px 0px 12px #ff007f;
            transition: all 0.2s ease;
        }
        .cyber-btn:hover {
            background-color: #ff007f;
            color: #ffffff;
            box-shadow: 0px 0px 22px #00ffcc;
        }
    </style>
</head>
<body style="background-color: transparent;">

<div class="btn-container">
    <button class="cyber-btn" onclick="enviarComando('alimentar')">🍎 Dar de Comer</button>
    <button class="cyber-btn" onclick="enviarComando('saludar')">🎾 Jugar con Mascota</button>
</div>

<div id="status" style="color: #00ffcc; text-align: center; margin-top: 20px; font-family: monospace; font-size: 14px;"></div>

<script>
    function enviarComando(accion) {
        var statusDiv = document.getElementById('status');
        statusDiv.innerHTML = "📡 Enviando orden de " + accion + "...";
        
        var client = new Paho.MQTT.Client("broker.hivemq.com", 8000, "web_client_" + Math.floor(Math.random() * 100000));
        
        client.connect({
            onSuccess: function () {
                var message = new Paho.MQTT.Message(accion);
                message.destinationName = "cyberpet/accion";
                client.send(message);
                statusDiv.innerHTML = "✅ ¡Orden '" + accion + "' ejecutada con éxito en Wokwi!";
                setTimeout(function(){ client.disconnect(); }, 800);
            },
            onFailure: function (e) {
                statusDiv.innerHTML = "❌ Error de conexión: " + e.errorMessage;
            }
        });
    }
</script>

</body>
</html>
"""

components.html(mqtt_js_code, height=160)
