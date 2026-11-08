# --- CONTENEDOR VISUAL TIPO TAMAGOTCHI ---
with st.container():
    st.markdown("<div class='tamagotchi-container'>", unsafe_allow_html=True)
    
    # Ahora buscará automáticamente las imágenes en formato .jpeg (normal.jpeg, alimentar.jpeg, saludar.jpeg, muerto.jpeg)
    avatar_path = f"assets/{st.session_state.estado_mascota}.jpeg"
    
    col_img, col_stats = st.columns([1, 1])
    
    with col_img:
        try:
            st.image(avatar_path, width=250)
        except:
            st.markdown(f"### 🐾 Estado: {st.session_state.estado_mascota.upper()}")
            st.caption("Faltan las imágenes .jpeg en la carpeta assets/")

    with col_stats:
        st.markdown("### 📊 Signos Vitales")
        st.write("")
        st.markdown(f"🍎 **Hambre:** {int(st.session_state.hambre)}%")
        st.progress(int(st.session_state.hambre))
        
        st.write("")
        st.markdown(f"🎾 **Felicidad:** {int(st.session_state.felicidad)}%")
        st.progress(int(st.session_state.felicidad))

    # --- LÓGICA DE SUPERVIVENCIA Y REGENERACIÓN ---
    if st.session_state.estado_mascota == "muerto":
        st.error("💀 ¡OH NO! TU CYBER-PET HA MUERTO POR NEGLIGENCIA.")
        if st.button("🔄 PROCESO DE REGENERACIÓN (REVIVIR)", use_container_width=True):
            st.session_state.hambre = 100
            st.session_state.felicidad = 100
            st.session_state.estado_mascota = "normal"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
