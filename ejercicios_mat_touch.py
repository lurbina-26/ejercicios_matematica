import random
import streamlit as st
import streamlit.components.v1 as components

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
# 5. Componente Interactivo (Arrastrar + Auto-Validación)
# ---------------------------------------------------------
drag_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        font-family: Arial, sans-serif;
        text-align: center;
        background-color: transparent;
        margin: 0;
        padding: 5px;
        user-select: none;
    }}
    .problema {{
        font-size: 2.3rem;
        font-weight: bold;
        margin-bottom: 20px;
        color: #1E293B;
    }}
    .zona-soltar {{
        display: inline-block;
        width: 95px;
        height: 65px;
        border: 3px dashed #3B82F6;
        border-radius: 12px;
        background-color: #EFF6FF;
        vertical-align: middle;
        line-height: 65px;
        font-size: 2rem;
        color: #1D4ED8;
    }}
    .fichas-container {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
    }}
    .ficha {{
        width: 75px;
        height: 75px;
        background-color: #F59E0B;
        color: white;
        font-size: 1.9rem;
        font-weight: bold;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        touch-action: none;
        cursor: grab;
        position: relative;
        z-index: 100;
    }}
    .ficha:active {{ cursor: grabbing; }}
    #feedback {{
        font-size: 1.3rem;
        font-weight: bold;
        height: 35px;
        margin-top: 15px;
    }}
</style>
</head>
<body>

<div class="problema">
    {n1} + {n2} = <div class="zona-soltar" id="destino">?</div>
</div>

<p style="color: #64748B; margin: 0;">Arrastra el número correcto con el dedo o mouse:</p>

<div class="fichas-container">
    <div class="ficha" data-valor="{opciones[0]}">{opciones[0]}</div>
    <div class="ficha" data-valor="{opciones[1]}">{opciones[1]}</div>
    <div class="ficha" data-valor="{opciones[2]}">{opciones[2]}</div>
</div>

<div id="feedback"></div>

<script>
    const destino = document.getElementById('destino');
    const feedback = document.getElementById('feedback');
    const respuestaCorrecta = "{respuesta_correcta}";
    let bloqueado = false;

    document.querySelectorAll('.ficha').forEach(ficha => {{
        let isDragging = false;
        let startX, startY;

        ficha.addEventListener('pointerdown', (e) => {{
            if (bloqueado) return;
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            ficha.setPointerCapture(e.pointerId);
        }});

        ficha.addEventListener('pointermove', (e) => {{
            if (!isDragging || bloqueado) return;
            const deltaX = e.clientX - startX;
            const deltaY = e.clientY - startY;
            ficha.style.transform = `translate(${{deltaX}}px, ${{deltaY}}px)`;
        }});

        ficha.addEventListener('pointerup', (e) => {{
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

            if (dentro && !bloqueado) {{
                const valor = ficha.getAttribute('data-valor');
                destino.textContent = valor;

                if (valor === respuestaCorrecta) {{
                    bloqueado = true;
                    destino.style.backgroundColor = "#C6F6D5";
                    destino.style.borderColor = "#38A169";
                    feedback.textContent = "¡Excelente! 🎉";
                    feedback.style.color = "#2F855A";

                    // Enviar evento de acierto a Streamlit
                    setTimeout(() => {{
                        window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "ACIERTO" }}, "*");
                    }}, 700);
                }} else {{
                    destino.style.backgroundColor = "#FED7D7";
                    destino.style.borderColor = "#E53E3E";
                    feedback.textContent = "Inténtalo de nuevo ❌";
                    feedback.style.color = "#C53030";

                    // Enviar evento de fallo a Streamlit
                    setTimeout(() => {{
                        window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "FALLO" }}, "*");
                    }}, 900);
                }}
            }}

            ficha.style.transform = "translate(0px, 0px)";
        }});
    }});
</script>
</body>
</html>
"""

# Renderizar el componente interactivo
resultado_arrastre = components.html(drag_html, height=330)

# ---------------------------------------------------------
# 6. Procesar Eventos de Arrastre Automáticamente
# ---------------------------------------------------------
if resultado_arrastre == "ACIERTO":
    st.session_state.racha += 1
    st.session_state.total_completados += 1
    generar_nuevo_ejercicio()
    st.rerun()
elif resultado_arrastre == "FALLO":
    st.session_state.racha = 0  # Reiniciar racha al fallar
    st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 7. Control Secundario
# ---------------------------------------------------------
if st.button("🔄 Saltar este Ejercicio", use_container_width=True):
    st.session_state.racha = 0
    generar_nuevo_ejercicio()
    st.rerun()
