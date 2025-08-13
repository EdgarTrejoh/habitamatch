import streamlit as st
from fpdf import FPDF
import datetime
import tempfile
import requests

WEBHOOK_URL = st.secrets.get("make_webhook_url", "").strip()  # añade esto en .streamlit/secrets.toml

st.set_page_config(page_title="Calculadora de Capacidad de Pago - HabitaMatch", layout="centered")
st.title("🏠 Calculadora de Capacidad de Pago")

def calcular_capacidad(ingreso_mensual, porcentaje, plazo_anios, tasa_anual):
    mensualidad = ingreso_mensual * (porcentaje / 100.0)
    factor = (tasa_anual / 100.0) / 12.0
    n = plazo_anios * 12
    if factor == 0:
        return 0.0, mensualidad  # evita división entre cero
    capacidad_credito = mensualidad * ((1 - (1 + factor) ** -n) / factor)
    return capacidad_credito, mensualidad

def generar_pdf(**datos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Reporte de Capacidad de Pago", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 8, f"Ingreso mensual: ${datos['ingreso_mensual']:,.2f}", ln=True)
    pdf.cell(200, 8, f"Porcentaje destinado: {datos['porcentaje_destinado']}%", ln=True)
    pdf.cell(200, 8, f"Plazo seleccionado: {datos['plazo']} años", ln=True)
    pdf.cell(200, 8, f"Tasa anual: {datos['tasa_anual']}%", ln=True)
    pdf.cell(200, 8, f"Mensualidad estimada: ${datos['mensualidad']:,.2f}", ln=True)
    pdf.ln(6)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Capacidad de compra estimada: ${datos['capacidad_credito']:,.2f}", ln=True)

    fecha = datetime.date.today().strftime("%d/%m/%Y")
    pdf.set_font("Arial", "I", 10)
    pdf.ln(6)
    pdf.cell(200, 8, f"Generado por HabitaMatch · {fecha}", ln=True)

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmpfile.name)
    return tmpfile.name

def send_to_make(payload, max_retries=2):
    if not WEBHOOK_URL:
        st.error("❌ No hay WEBHOOK configurado. Agrega 'make_webhook_url' en st.secrets.")
        return False

    for i in range(max_retries + 1):
        try:
            r = requests.post(WEBHOOK_URL, json=payload, timeout=15)
            if r.status_code == 200:
                st.success("🎯 Datos enviados a CRM correctamente")
                return True
            elif r.status_code == 410:
                st.error("⚠️ Webhook 410: el URL ya no está activo. Genera uno nuevo en Make y actualízalo en st.secrets.")
                return False
            else:
                st.warning(f"⚠️ Error al enviar datos: {r.status_code} – {r.text[:200]}")
                # backoff simple para errores transitorios (5xx)
                if 500 <= r.status_code < 600 and i < max_retries:
                    time.sleep(1.5 * (i + 1))
                    continue
                return False
        except requests.RequestException as e:
            st.error(f"❌ Error de conexión: {e}")
            if i < max_retries:
                time.sleep(1.5 * (i + 1))
                continue
            return False



with st.form("form_capacidad", clear_on_submit=False):
    # --- Entradas del usuario ---
    ingreso_mensual = st.number_input("💰 Ingreso mensual neto (MXN)", min_value=0, step=1000)
    porcentaje_destinado = st.slider("📊 Porcentaje destinado al pago de vivienda", 10, 40, 30)
    plazo = st.selectbox("⏳ Plazo estimado de crédito (años)", [10, 15, 20, 25, 30])
    tasa_anual = st.number_input("📈 Tasa de interés anual estimada (%)", min_value=0.0, max_value=20.0, value=10.0, step=0.05)

    st.markdown("---")
    nombre = st.text_input("🧑 Tu nombre")
    correo = st.text_input("📧 Tu correo electrónico")
    st.caption("Tu información se usa solo para generar el reporte y envío al CRM.")

    col1, col2 = st.columns(2)
    calcular_btn = col1.form_submit_button("Calcular capacidad de pago")
    enviar_btn   = col2.form_submit_button("Enviar y generar reporte")

# --- Lógica post-submit ---
if calcular_btn or enviar_btn:
    capacidad_credito, mensualidad = calcular_capacidad(ingreso_mensual, porcentaje_destinado, plazo, tasa_anual)

    # Validaciones genéricas
    if ingreso_mensual <= 0:
        st.error("❌ El ingreso mensual debe ser mayor a 0.")
    else:
        st.success(f"📌 Capacidad de compra estimada: ${capacidad_credito:,.2f}")
        st.info(f"💵 Mensualidad estimada: ${mensualidad:,.2f}")

if enviar_btn:
    # Validaciones adicionales para envío
    if not nombre or not correo:
        st.error("❌ Ingresa tu nombre y correo para continuar.")
    elif ingreso_mensual <= 0:
        st.error("❌ El ingreso mensual debe ser mayor a 0.")
    else:
        # Enviar al CRM (Make)
        payload = {
            "nombre": nombre,
            "correo": correo,
            "ingreso_mensual": ingreso_mensual,
            "porcentaje": porcentaje_destinado,
            "plazo": plazo,
            "tasa": tasa_anual,
            "capacidad_credito": round(capacidad_credito, 2),
            "mensualidad": round(mensualidad, 2),
            "fuente": "HabitaMatch-Calculadora"
        }
        send_to_make(payload)

        # Generar y descargar PDF
        pdf_path = generar_pdf(
            ingreso_mensual=ingreso_mensual,
            porcentaje_destinado=porcentaje_destinado,
            plazo=plazo,
            tasa_anual=tasa_anual,
            mensualidad=mensualidad,
            capacidad_credito=capacidad_credito,
        )
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Descargar reporte PDF", f, file_name="capacidad_pago.pdf")
