import random
import streamlit as st
import streamlit.components.v1 as components

# Configuración inicial de la página
st.set_page_config(page_title="Ejercicios Interactivos", page_icon="🧮", layout="centered")

st.title("🧮 Ejercicios de Matemática Interactivos")

# ---------------------------------------------------------
# 1. Selector de Nivel y Configuración
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
if "num1" not in st.session_state or st.session_state.get("nivel_actual") != nivel:
    st.session_state.nivel_actual = nivel
    st.session_state.num1 = random.randint(rango_min, rango_max)
    st.session_state.num2 = random.randint(rango_min, rango_max)
    st.session_state.racha = 0
    st.session_state.total_completados = 0

def generar_nuevo_ejercicio():
    st.session_state.num1 = random.randint(rango_min, rango_max)
    st.session_state.num2 = random.randint(rango_min, rango_max)

# ---------------------------------------------------------
# 3. Lógica del Problema y Opciones
# ---------------------------------------------------------
n1 = st.session_state.num1
n2 = st.session_state.num2
respuesta_correcta = n1 + n2

# Generar opciones distractoras únicas
opciones = [respuesta_correcta]
while len(opciones) < 3:
    distractor = respuesta_correcta + random.choice([-3, -2, -1, 1, 2, 3, 5, -5])
    if distractor > 0 and distractor not in opciones:
        opciones.append(distractor)

random.shuffle(opciones)

# Mostrar estadísticas del alumno
col1, col2 = st.columns(2)
col1.metric("Aciertos seguidos (Racha)", st.session_state.racha)
col2.metric("Ejercicios resueltos", st.session_state.total_completados)

st.markdown("---")

# ---------------------------------------------------------
# 4. Componente Interactivo de Arrastrar (HTML/JS)
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
        padding: 10px;
    }}
    .problema {{
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 20px;
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
        margin-top: 25px;
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
        user-select: none;
        touch-action: none;
        cursor: grab;
    }}
</style>
</head>
<body>

<div class="problema">
    {n1} + {n2} = <div class="zona-soltar" id="destino">?</div>
</div>

<p style="color: #64748B;">Arrastra el número correcto hasta la casilla azul con tu dedo:</p>

<div class="fichas-container">
    <div class="ficha" data-valor="{opciones[0]}">{opciones[0]}</div>
    <div class="ficha" data-valor="{opciones[1]}">{opciones[1]}</div>
    <div class="ficha" data-valor="{opciones[2]}">{opciones[2]}</div>
</div>

<script>
    const destino = document.getElementById('destino');
    const respuestaCorrecta = "{respuesta_correcta}";

    document.querySelectorAll('.ficha').forEach(ficha => {{
        let startX, startY;

        ficha.addEventListener('touchstart', (e) => {{
            const touch = e.touches[0];
            startX = touch.clientX;
            startY = touch.clientY;
        }});

        ficha.addEventListener('touchmove', (e) => {{
            e.preventDefault();
            const touch = e.touches[0];
            const deltaX = touch.clientX - startX;
            const deltaY = touch.clientY - startY;
            ficha.style.transform = `translate(${{deltaX}}px, ${{deltaY}}px)`;
        }});

        ficha.addEventListener('touchend', (e) => {{
            const touch = e.changedTouches[0];
            const rect = destino.getBoundingClientRect();

            const dentro = (
                touch.clientX >= rect.left &&
                touch.clientX <= rect.right &&
                touch.clientY >= rect.top &&
                touch.clientY <= rect.bottom
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

components.html(drag_html, height=280)

# ---------------------------------------------------------
# 5. Botones de Control de Flujo (Consecutivos)
# ---------------------------------------------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("✅ Verificar Acierto / Siguiente", type="primary", use_container_width=True):
        st.session_state.racha += 1
        st.session_state.total_completados += 1
        generar_nuevo_ejercicio()
        st.rerun()

with col_btn2:
    if st.button("🔄 Cambiar Ejercicio", use_container_width=True):
        generar_nuevo_ejercicio()
        st.rerun()