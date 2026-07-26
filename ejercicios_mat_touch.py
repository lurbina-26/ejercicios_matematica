import random
import time
import streamlit as st

st.set_page_config(page_title="Ejercicios Interactivos", page_icon="🧮", layout="centered")

st.title("🧮 Ejercicios de Matemática Interactivos")

# ---------------------------------------------------------
# 1. Configuración de Niveles
# ---------------------------------------------------------
nivel = st.sidebar.radio("Selecciona el Nivel:", ["Fácil (1-10)", "Medio (10-50)", "Difícil (50-100)"])

if nivel == "Fácil (1-10)":
    rango_min, rango_max = 1, 10
elif nivel == "Medio (10-50)":
    rango_min, rango_max = 10, 50
else:
    rango_min, rango_max = 50, 100

# ---------------------------------------------------------
# 2. Inicialización del Estado de la Sesión
# ---------------------------------------------------------
if "racha" not in st.session_state:
    st.session_state.racha = 0

if "total_completados" not in st.session_state:
    st.session_state.total_completados = 0

if "num1" not in st.session_state or st.session_state.get("nivel_actual") != nivel:
    st.session_state.nivel_actual = nivel
    st.session_state.num1 = random.randint(rango_min, rango_max)
    st.session_state.num2 = random.randint(rango_min, rango_max)

def generar_nuevo_ejercicio():
    st.session_state.num1 = random.randint(rango_min, rango_max)
    st.session_state.num2 = random.randint(rango_min, rango_max)

# ---------------------------------------------------------
# 3. Métricas de Progreso
# ---------------------------------------------------------
col1, col2 = st.columns(2)
col1.metric("Aciertos seguidos (Racha)", st.session_state.racha)
col2.metric("Ejercicios resueltos", st.session_state.total_completados)

st.markdown("---")

# ---------------------------------------------------------
# 4. Generación de Problema y Opciones
# ---------------------------------------------------------
n1 = st.session_state.num1
n2 = st.session_state.num2
respuesta_correcta = n1 + n2

if "opciones" not in st.session_state or st.session_state.get("problema_actual") != f"{n1}+{n2}":
    st.session_state.problema_actual = f"{n1}+{n2}"
    opciones = [respuesta_correcta]
    while len(opciones) < 3:
        distractor = respuesta_correcta + random.choice([-3, -2, -1, 1, 2, 3, 5, -5])
        if distractor > 0 and distractor not in opciones:
            opciones.append(distractor)
    random.shuffle(opciones)
    st.session_state.opciones = opciones
else:
    opciones = st.session_state.opciones

# ---------------------------------------------------------
# 5. Visualización del Problema
# ---------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <span style="font-size: 3rem; font-weight: bold; color: #1E293B;">
            {n1} + {n2} = 
        </span>
        <span style="display: inline-block; width: 100px; height: 65px; border: 3px dashed #3B82F6; border-radius: 12px; background-color: #EFF6FF; line-height: 65px; font-size: 2.5rem; color: #1D4ED8; text-align: center; vertical-align: middle;">
            ?
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("### Selecciona la respuesta correcta:")

# ---------------------------------------------------------
# 6. Botones de Respuesta con Verificación Estricta
# ---------------------------------------------------------
cols = st.columns(3)

for idx, opc in enumerate(opciones):
    if cols[idx].button(f"🎈 {opc}", use_container_width=True, key=f"btn_{opc}"):
        if opc == respuesta_correcta:
            st.session_state.racha += 1
            st.session_state.total_completados += 1
            st.success("¡Excelente! Respuesta correcta 🎉")
            time.sleep(0.8)
            generar_nuevo_ejercicio()
            st.rerun()
        else:
            st.session_state.racha = 0  # Reiniciar racha por error
            st.error(f"¡Incorrecto! La respuesta no es {opc}. Inténtalo de nuevo ❌")

st.markdown("---")

# ---------------------------------------------------------
# 7. Control Secundario
# ---------------------------------------------------------
if st.button("🔄 Saltar este Ejercicio", use_container_width=True):
    st.session_state.racha = 0  # Saltar penaliza la racha acumulada
    generar_nuevo_ejercicio()
    st.rerun()
