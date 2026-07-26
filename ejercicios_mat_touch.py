# ---------------------------------------------------------
# 1. Definición de Metas por Nivel
# ---------------------------------------------------------
nivel = st.sidebar.radio("Selecciona el Nivel:", ["Fácil (1-10)", "Medio (10-50)", "Difícil (50-100)"])

metas_nivel = {
    "Fácil (1-10)": 20,
    "Medio (10-50)": 15,
    "Difícil (50-100)": 10
}

meta_actual = metas_nivel[nivel]

# Inicializar aciertos del nivel actual en la sesión
if "aciertos_nivel" not in st.session_state:
    st.session_state.aciertos_nivel = 0

# ---------------------------------------------------------
# 2. Barra de Progreso Superior (Móvil)
# ---------------------------------------------------------
progreso = min(st.session_state.aciertos_nivel / meta_actual, 1.0)

st.write(f"**Progreso del Nivel:** {st.session_state.aciertos_nivel} / {meta_actual} ejercicios")
st.progress(progreso)

# ---------------------------------------------------------
# 3. Pantalla de Meta Cumplida
# ---------------------------------------------------------
if st.session_state.aciertos_nivel >= meta_actual:
    st.balloons()  # Animación de globos en Streamlit
    st.success(f"🏆 ¡Felicidades! Has completado los {meta_actual} ejercicios del nivel {nivel}.")
    if st.button("🔄 Reiniciar Nivel o Elegir Otro", use_container_width=True):
        st.session_state.aciertos_nivel = 0
        st.rerun()
