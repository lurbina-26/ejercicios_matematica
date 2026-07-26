import random
import tempfile
import os
import streamlit as st
import streamlit.components.v1 as components

# Configuración de página optimizada para móviles
st.set_page_config(page_title="Ejercicios de Suma y Resta", page_icon="🧮", layout="centered")

# ---------------------------------------------------------
# 1. Catálogo de Avatares
# ---------------------------------------------------------
AVATARES = {
    "🦄 Unicornio": {"emoji": "🦄", "nombre": "Unicornio Mágico", "acierto": "¡Súper mágico! ✨", "fallo": "¡Casi! Inténtalo otra vez 💫"},
    "🐱 Gatita": {"emoji": "🐱", "nombre": "Gatita Astuta", "acierto": "¡Miau-avilloso! 🐾", "fallo": "¡Sigue intentando! 🐾"},
    "🦸‍♀️ Súper Niña": {"emoji": "🦸‍♀️", "nombre": "Súper Heroína", "acierto": "¡Poder matemático! ⚡", "fallo": "¡Los héroes no se rinden! 💪"},
    "👩‍🔬 Científica": {"emoji": "👩‍🔬", "nombre": "Científica Explorer", "acierto": "¡Cálculo perfecto! 🔬", "fallo": "¡Revisemos de nuevo! 📐"},
    "🐼 Panda": {"emoji": "🐼", "nombre": "Panda Amigable", "acierto": "¡Genial, lo lograste! 🎋", "fallo": "¡Tú puedes, dale otra vez! 🌿"},
    "🦊 Zorro": {"emoji": "🦊", "nombre": "Zorro Listo", "acierto": "¡Qué inteligente! 🦊", "fallo": "¡Un paso más! 🐾"},
    "🤖 Robot": {"emoji": "🤖", "nombre": "Bot Matemático", "acierto": "¡Procesado con éxito! ⚙️", "fallo": "¡Recalculando... prueba de nuevo! 🔄"}
}

# ---------------------------------------------------------
# 2. Registro de Nombre y Selección de Avatar
# ---------------------------------------------------------
if "nombre_estudiante" not in st.session_state:
    st.session_state.nombre_estudiante = ""
if "avatar_key" not in st.session_state:
    st.session_state.avatar_key = "🦄 Unicornio"

if not st.session_state.nombre_estudiante:
    st.title("🧮 ¡Bienvenido!")
    st.write("Ingresa tu nombre y elige a tu compañero de juego:")
    
    nombre_input = st.text_input("Tu nombre:", placeholder="Escribe tu nombre aquí...")
    
    st.write("**Elige tu Avatar:**")
    avatar_seleccionado = st.selectbox("Compañero de juego:", list(AVATARES.keys()))
    
    info_av = AVATARES[avatar_seleccionado]
    st.info(f"Seleccionaste a **{info_av['nombre']}** {info_av['emoji']}")

    if st.button("🚀 ¡Comenzar a Jugar!", use_container_width=True, type="primary"):
        if nombre_input.strip():
            st.session_state.nombre_estudiante = nombre_input.strip()
            st.session_state.avatar_key = avatar_seleccionado
            st.rerun()
        else:
            st.warning("Por favor ingresa un nombre válido.")
    st.stop()

avatar_actual = AVATARES.get(st.session_state.avatar_key, AVATARES["🦄 Unicornio"])

# ---------------------------------------------------------
# 3. Configuración de Niveles y Metas
# ---------------------------------------------------------
st.title("🧮 Ejercicios de Suma y Resta")
st.caption(f"¡Hola, **{st.session_state.nombre_estudiante}**! Jugando con {avatar_actual['emoji']}")

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

if st.sidebar.button("👤 Cambiar de estudiante / Avatar"):
    st.session_state.nombre_estudiante = ""
    st.session_state.aciertos_nivel = 0
    st.session_state.racha = 0
    st.rerun()

# ---------------------------------------------------------
# 4. Generación Dinámica de Operación (Suma o Resta)
# ---------------------------------------------------------
if "racha" not in st.session_state:
    st.session_state.racha = 0
if "aciertos_nivel" not in st.session_state:
    st.session_state.aciertos_nivel = 0
if "intentos" not in st.session_state:
    st.session_state.intentos = 0

def generar_nuevo_ejercicio():
    st.session_state.operacion = random.choice(["+", "-"])
    n1 = random.randint(rango_min, rango_max)
    n2 = random.randint(rango_min, rango_max)
    
    if st.session_state.operacion == "-":
        if n1 < n2:
            n1, n2 = n2, n1
            
    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.intentos += 1

if "num1" not in st.session_state or st.session_state.get("nivel_actual") != nivel:
    st.session_state.nivel_actual = nivel
    st.session_state.aciertos_nivel = 0
    generar_nuevo_ejercicio()

if st.session_state.get("nivel_previo") != nivel:
    st.session_state.nivel_previo = nivel
    st.session_state.aciertos_nivel = 0

# ---------------------------------------------------------
# 5. Barra de Progreso Compacta (Con Meta Completa a la Derecha)
# ---------------------------------------------------------
progreso = min(st.session_state.aciertos_nivel / meta_actual, 1.0)

st.progress(progreso)

# Layout de 2 columnas para el texto inferior de la barra de progreso
col_prog_izq, col_prog_der = st.columns([1, 1])
with col_prog_izq:
    st.caption(f"🔥 Racha: **{st.session_state.racha}** | Resueltos: **{st.session_state.aciertos_nivel}**")
with col_prog_der:
    st.markdown(f"<div style='text-align: right; color: #64748B; font-size: 0.85rem;'><b>Meta:</b> {meta_actual} ejercicios</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. Pantalla de Meta Cumplida
# ---------------------------------------------------------
if st.session_state.aciertos_nivel >= meta_actual:
    st.balloons()
    st.success(f"🏆 ¡MUCHAS FELICIDADES, **{st.session_state.nombre_estudiante.upper()}**! 🎉\n\nJunto a {avatar_actual['emoji']} **{avatar_actual['nombre']}** has completado los {meta_actual} ejercicios del **Nivel {nivel}**.")
    
    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        if st.button("🔄 Jugar de nuevo", use_container_width=True):
            st.session_state.aciertos_nivel = 0
            st.session_state.racha = 0
            generar_nuevo_ejercicio()
            st.rerun()
    with col_fin2:
        if st.button("👤 Cambiar alumno", use_container_width=True):
            st.session_state.nombre_estudiante = ""
            st.session_state.aciertos_nivel = 0
            st.session_state.racha = 0
            st.rerun()
            
    st.stop()

# ---------------------------------------------------------
# 7. Componente Nativo Bidireccional (Arrastrar y Soltar)
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
    body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 2px; user-select: none; }
    .avatar-box { font-size: 2.2rem; margin-bottom: 2px; }
    .problema { font-size: 2rem; font-weight: bold; margin-bottom: 10px; color: #1E293B; }
    .zona-soltar { display: inline-block; width: 80px; height: 55px; border: 3px dashed #3B82F6; border-radius: 12px; background-color: #EFF6FF; vertical-align: middle; line-height: 55px; font-size: 1.7rem; color: #1D4ED8; }
    .fichas-container { display: flex; justify-content: center; gap: 12px; margin-top: 10px; }
    .ficha { width: 65px; height: 65px; background-color: #F59E0B; color: white; font-size: 1.7rem; font-weight: bold; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.15); touch-action: none; cursor: grab; position: relative; z-index: 100; }
    .ficha:active { cursor: grabbing; }
    #feedback { font-size: 1.1rem; font-weight: bold; height: 25px; margin-top: 6px; }
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
            renderApp(args.n1, args.n2, args.operacion, args.opciones, args.respuesta, args.avatarEmoji, args.txtAcierto, args.txtFallo);
            sendMessage("streamlit:setFrameHeight", {height: 280});
        }
    });

    function renderApp(n1, n2, operacion, opciones, respuestaCorrecta, avatarEmoji, txtAcierto, txtFallo) {
        document.getElementById("content").innerHTML = `
            <div class="avatar-box" id="avatarDisplay">${avatarEmoji}</div>
            <div class="problema">
                ${n1} ${operacion} ${n2} = <div class="zona-soltar" id="destino">?</div>
            </div>
            <p style="color: #64748B; margin: 0; font-size: 0.85rem;">Arrastra la respuesta correcta:</p>
            <div class="fichas-container">
                <div class="ficha" data-valor="${opciones[0]}">${opciones[0]}</div>
                <div class="ficha" data-valor="${opciones[1]}">${opciones[1]}</div>
                <div class="ficha" data-valor="${opciones[2]}">${opciones[2]}</div>
            </div>
            <div id="feedback"></div>
        `;

        const destino = document.getElementById('destino');
        const feedback = document.getElementById('feedback');
        const avatarDisplay = document.getElementById('avatarDisplay');
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
                        feedback.textContent = txtAcierto;
                        feedback.style.color = "#2F855A";
                        avatarDisplay.style.transform = "scale(1.2)";
                        setTimeout(() => { sendMessage("streamlit:setComponentValue", {value: "ACIERTO"}); }, 500);
                    } else {
                        bloqueado = true;
                        destino.style.backgroundColor = "#FED7D7";
                        destino.style.borderColor = "#E53E3E";
                        feedback.textContent = txtFallo;
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
# 8. Cálculo de Respuesta y Opciones
# ---------------------------------------------------------
n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operacion

respuesta_correcta = (n1 + n2) if op == "+" else (n1 - n2)

clave_problema = f"{n1}{op}{n2}"
if "opciones" not in st.session_state or st.session_state.get("problema_actual") != clave_problema:
    st.session_state.problema_actual = clave_problema
    opciones = [respuesta_correcta]
    while len(opciones) < 3:
        distractor = respuesta_correcta + random.choice([-3, -2, -1, 1, 2, 3, 5, -5])
        if distractor >= 0 and distractor not in opciones:
            opciones.append(distractor)
    random.shuffle(opciones)
    st.session_state.opciones = opciones
else:
    opciones = st.session_state.opciones

# ---------------------------------------------------------
# 9. Ejecución y Auto-Validación
# ---------------------------------------------------------
clave_unica = f"ej_{st.session_state.aciertos_nivel}_{st.session_state.intentos}"

resultado = drag_drop_component(
    n1=n1, 
    n2=n2, 
    operacion=op,
    opciones=opciones, 
    respuesta=respuesta_correcta, 
    avatarEmoji=avatar_actual["emoji"],
    txtAcierto=avatar_actual["acierto"],
    txtFallo=avatar_actual["fallo"],
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

if st.button("🔄 Saltar este Ejercicio", use_container_width=True):
    st.session_state.racha = 0
    generar_nuevo_ejercicio()
    st.rerun()

# ---------------------------------------------------------
# 10. Pie de Página (Créditos)
# ---------------------------------------------------------
st.markdown("<br><hr style='margin: 10px 0;'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 0.8rem; font-weight: 500;'>"
    "Desarrollado por Estefany Urbina"
    "</div>", 
    unsafe_allow_html=True
)
