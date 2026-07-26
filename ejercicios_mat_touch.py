import random
import tempfile
import os
import streamlit as st
import streamlit.components.v1 as components

# Configuración de página optimizada para móviles
st.set_page_config(page_title="Ejercicios Interactivos", page_icon="🧮", layout="centered")

st.title("🧮 Ejercicios de Matemática")

# ---------------------------------------------------------
# 1. Configuración de Niveles y Metas
# ---------------------------------------------------------
nivel = st.sidebar.radio("Selecciona el Nivel:", ["Fácil (1-10)", "Medio (10-50)", "Difícil (50-100)"])

metas_nivel = {
    "Fácil (1-10)": 20,
    "Medio (10-50)": 15,
    "Difícil (50-100)": 10
}

meta_actual = metas_nivel[nivel]

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
if "aciertos_nivel" not in st.session_state:
    st.session_state.aciertos_nivel = 0
if "intentos" not in st.session_state:
    st.session_state.intentos = 0

def generar_nuevo_ejercicio():
    st.session_state.num1 = random.randint(rango_min, rango_max)
    st.session_state.num2 = random.randint(rango_min, rango_max)
    st.session_state.intentos += 1

if "num1" not in st.session_state or st.session_state.get("nivel_actual") != nivel:
    st.session_state.nivel_actual = nivel
    st.session_state.aciertos_nivel = 0
    generar_nuevo_ejercicio()

# Resetear aciertos si cambia de nivel
if st.session_state.get("nivel_previo") != nivel:
    st.session_state.nivel_previo = nivel
    st.session_state.aciertos_nivel = 0

# ---------------------------------------------------------
# 3. Barra de Progreso Superior
# ---------------------------------------------------------
progreso = min(st.session_state.aciertos_nivel / meta_actual, 1.0)

st.write(f"**Progreso del nivel:** {st.session_state.aciertos_nivel} de {meta_actual} resueltos")
st.progress(progreso)

col_m1, col_m2 = st.columns(2)
col_m1.metric("Aciertos seguidos", st.session_state.racha)
col_m2.metric("Meta del nivel", f"{meta_actual} ej.")

st.markdown("---")

# ---------------------------------------------------------
# 4. Pantalla de Meta Cumplida
# ---------------------------------------------------------
if st.session_state.aciertos_nivel >= meta_actual:
    st.balloons()
    st.success(f"🎉 ¡Felicidades! Has completado la meta de {meta_actual} ejercicios del Nivel {nivel}.")
    if st.button("🔄 Volver a jugar este nivel", use_container_width=True):
        st.session_state.aciertos_nivel = 0
        st.session_state.racha = 0
        generar_nuevo_ejercicio()
        st.rerun()
    st.stop()

# ---------------------------------------------------------
# 5. Componente Nativo Bidireccional
# ---------------------------------------------------------
@st.cache_resource
def crear_componente_arrastre():
    temp_dir = tempfile.mkdtemp()
    html_file = os.path.join(temp_dir, "index.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 5px; user-select: none; }
    .problema { font-size: 2.1rem; font-weight: bold; margin-bottom: 15px; color: #1E293B; }
    .zona-soltar { display: inline-block; width: 85px; height: 60px; border: 3px dashed #3B82F6; border-radius: 12px; background-color: #EFF6FF; vertical-align: middle; line-height: 60px; font-size: 1.8rem; color: #1D4ED8; }
    .fichas-container { display: flex; justify-content: center; gap: 15px; margin-top: 15px; }
    .ficha { width: 70px; height: 70px; background-color: #F59E0B; color: white; font-size: 1.8rem; font-weight: bold; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.15); touch-action: none; cursor: grab; position: relative; z-index: 100; }
    .ficha:active { cursor: grabbing; }
    #feedback { font-size: 1.2rem; font-weight: bold; height: 30px; margin-top: 10px; }
</style>
</head>
<body>
<div id="content"></div>
<script>
    function sendMessage(type, data) {
        window.parent.postMessage(Object.assign({isStreamlitMessage: true, type: type}, data), "*");
    }
    
    window.addEventListener("message", function(event) {
        if (event.data.type === "streamlit:render") {
            const args = event.data.args;
            renderApp(args.n1, args.n2, args.opciones, args.respuesta);
            sendMessage("streamlit:setFrameHeight", {height: 280});
        }
    });

    function renderApp(n1, n2, opciones, respuestaCorrecta) {
        document.getElementById("content").innerHTML = `
            <div class="problema">
                ${n1} + ${n2} = <div class="zona-soltar" id="destino">?</div>
            </div>
            <p style="color: #64748B; margin: 0; font-size: 0.95rem;">Arrastra la respuesta correcta:</p>
            <div class="fichas-container">
                <div class="ficha" data-valor="${opciones[0]}">${opciones[0]}</div>
                <div class="ficha" data-valor="${opciones[1]}">${opciones[1]}</div>
                <div class="ficha" data-valor="${opciones[2]}">${opciones[2]}</div>
            </div>
            <div id="feedback"></div>
        `;

        const destino = document.getElementById('destino');
        const feedback = document.getElementById('feedback');
        let bloqueado = false;

        document.querySelectorAll('.ficha').forEach(ficha => {
            let isDragging = false;
            let startX, startY;

            ficha.addEventListener('pointerdown', (e) => {
                if (bloqueado) return;
                isDragging = true;
                startX = e.clientX;
                startY = e.clientY;
                ficha.setPointerCapture(e.pointerId);
            });

            ficha.addEventListener('pointermove', (e) => {
                if (!isDragging || bloqueado) return;
                const deltaX = e.clientX - startX;
                const deltaY = e.clientY - startY;
                ficha.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
            });

            ficha.addEventListener('pointerup', (e) => {
                if (!isDragging) return;
                isDragging = false;
                ficha.releasePointerCapture(e.pointerId);

                const rect = destino.getBoundingClientRect();
                const dentro = (
                    e.clientX >= rect.left &&
                    e.clientX <= rect.right &&
                    e.clientY >= rect.top &&
                    e.clientY <= rect.bottom
                );

                if (dentro && !bloqueado) {
                    const valor = parseInt(ficha.getAttribute('data-valor'));
                    destino.textContent = valor;

                    if (valor === respuestaCorrecta) {
                        bloqueado = true;
                        destino.style.backgroundColor = "#C6F6D5";
                        destino.style.borderColor = "#38A169";
                        feedback.textContent = "¡Excelente! 🎉";
                        feedback.style.color = "#2F855A";
                        setTimeout(() => { sendMessage("streamlit:setComponentValue", {value: "ACIERTO"}); }, 500);
                    } else {
                        bloqueado = true;
                        destino.style.backgroundColor = "#FED7D7";
                        destino.style.borderColor = "#E53E3E";
                        feedback.textContent = "Inténtalo de nuevo ❌";
                        feedback.style.color = "#C53030";
                        setTimeout(() => { sendMessage("streamlit:setComponentValue", {value: "FALLO"}); }, 700);
                    }
                }
                ficha.style.transform = "translate(0px, 0px)";
            });
        });
    }
    
    sendMessage("streamlit:componentReady", {apiVersion: 1});
</script>
</body>
</html>""")
    return components.declare_component("math_drag_drop", path=temp_dir)

drag_drop_component = crear_componente_arrastre()

# ---------------------------------------------------------
# 6. Generación de Problema y Opciones
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
# 7. Ejecución y Validación Automática
# ---------------------------------------------------------
clave_unica = f"ejercicio_{st.session_state.aciertos_nivel}_{st.session_state.intentos}"

resultado = drag_drop_component(
    n1=n1, 
    n2=n2, 
    opciones=opciones, 
    respuesta=respuesta_correcta, 
    key=clave_unica
)

if resultado == "ACIERTO":
    st.session_state.racha += 1
    st.session_state.aciertos_nivel += 1
    generar_nuevo_ejercicio()
    st.rerun()

elif resultado == "FALLO":
    st.session_state.racha = 0
    st.session_state.intentos += 1
    st.rerun()

st.markdown("---")

if st.button("🔄 Saltar este Ejercicio", use_container_width=True):
    st.session_state.racha = 0
    generar_nuevo_ejercicio()
    st.rerun()
