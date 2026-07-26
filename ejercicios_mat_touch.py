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
# 3. Métricas
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
# 5. Componente Interactivo (Mouse + Táctil)
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
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 15px;
        color: #1E293B;
    }}
    .zona-soltar {{
        display: inline-block;
        width: 90px;
        height: 60px;
        border: 3px dashed #3B82F6;
        border-radius: 12px;
        background-color: #EFF6FF;
        vertical-align: middle;
        line-height: 60px;
        font-size: 1.8rem;
        color: #1D4ED8;
    }}
    .fichas-container {{
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
    }}
    .ficha {{
        width: 70px;
        height: 70px;
        background-color: #F59E0B;
        color: white;
        font-size: 1.8rem;
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
</style>
</head>
<body>

<div class="problema">
    {n1} + {n2} = <div class="zona-soltar" id="destino">?</div>
</div>

<p style="color: #64748B;">Arrastra el número correcto a la casilla azul:</p>

<div class="fichas-container">
    <div class="ficha" data-valor="{opciones[0]}">{opciones[0]}</div>
    <div class="ficha" data-valor="{opciones[1]}">{opciones[1]}</div>
    <div class="ficha" data-valor="{opciones[2]}">{opciones[2]}</div>
</div>

<script>
    const destino = document.getElementById('destino');
    const respuestaCorrecta = "{respuesta_correcta}";

    document.querySelectorAll('.ficha').forEach(ficha => {{
        let isDragging = false;
        let startX, startY;

        ficha.addEventListener('pointerdown', (e) => {{
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            ficha.setPointerCapture(e.pointerId);
        }});

        ficha.addEventListener('pointermove', (e) => {{
            if (!isDragging) return;
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

            if (dentro) {{
                const valor = ficha.getAttribute('data-valor');
                destino.textContent = valor;
                if (valor === respuestaCorrecta) {{
                    destino.style.backgroundColor = "#C6F6D5";
                    destino.style.borderColor = "#38A169";
                }} else {{
                    destino.style.backgroundColor = "#FED7D7";
                    destino.style.borderColor = "#E53E3E";
                }}
            }}
            ficha.style.transform = "translate(0px, 0px)";
        }});
    }});
</script>
</body>
</html>
"""

components.html(drag_html, height=250)

# ---------------------------------------------------------
# 6. Selección Directa de Respuesta (Manejo Robusto de Estado)
# ---------------------------------------------------------
st.markdown("#### Selecciona el número que arrastraste:")
cols = st.columns(3)

for idx, opc in enumerate(opciones):
    if cols[idx].button(f"👉 {opc}", use_container_width=True, key=f"btn_{opc}"):
        if opc == respuesta_correcta:
            st.session_state.racha += 1
            st.session_state.total_completados += 1
            st.success("¡Excelente! 🎉")
            generar_nuevo_ejercicio()
            st.rerun()
        else:
            st.session_state.racha = 0
            st.error("Inténtalo de nuevo ❌")

st.markdown("---")
if st.button("🔄 Saltar Ejercicio", use_container_width=True):
    generar_nuevo_ejercicio()
    st.rerun()
