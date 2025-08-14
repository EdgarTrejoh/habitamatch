import streamlit as st
from fpdf import FPDF
import datetime
import tempfile
import requests

# Inicialización segura
if "ingreso_mensual" not in st.session_state:
    st.session_state["ingreso_mensual"] = 0
if "nombre" not in st.session_state:
    st.session_state["nombre"] = ""
if "correo" not in st.session_state:
    st.session_state["correo"] = ""
if "tasa_anual" not in st.session_state:
    st.session_state["tasa_anual"] = 10.0

st.set_page_config(page_title="Calculadora de Capacidad de Pago - HabitaMatch", layout="centered")
st.title("🏠 Calculadora de Capacidad de Pago")

# Entradas
ingreso_mensual = st.number_input("💰 Ingreso mensual neto (MXN)", min_value=0, step=1000, key="ingreso_mensual")
porcentaje_destinado = st.slider("📊 Porcentaje destinado al pago de vivienda", 10, 40, 30)
plazo = st.selectbox("⏳ Plazo estimado de crédito (años)", [10, 15, 20, 25, 30])
tasa_anual = st.number_input("📈 Tasa de interés anual estimada (%)", min_value=0.0, max_value=20.0, step=0.05, key="tasa_anual")
nombre = st.text_input("🧑 Tu nombre", key="nombre")
correo = st.text_input("📧 Tu correo electrónico", key="correo")

st.caption("Tu información se usa solo para generar el reporte y envío al CRM.")

if st.button("Calcular capacidad de pago"):
    mensualidad = ingreso_mensual * (porcentaje_destinado / 100)
    factor = (tasa_anual / 100) / 12
    n = plazo * 12
    try:
        capacidad_credito = mensualidad * ((1 - (1 + factor) ** -n) / factor)
    except ZeroDivisionError:
        capacidad_credito = 0
    st.success(f"📌 Capacidad de compra estimada: ${capacidad_credito:,.2f}")

if st.button("Enviar y generar reporte"):
    mensualidad = ingreso_mensual * (porcentaje_destinado / 100)
    factor = (tasa_anual / 100) / 12
    n = plazo * 12
    capacidad_credito = mensualidad * ((1 - (1 + factor) ** -n) / factor)

    payload = {
        "nombre": nombre,
        "correo": correo,
        "ingreso_mensual": ingreso_mensual,
        "porcentaje": porcentaje_destinado,
        "plazo": plazo,
        "tasa": tasa_anual,
        "capacidad_credito": round(capacidad_credito, 2),
        "mensualidad": round(mensualidad, 2)
    }

    webhook_url = st.secrets.get("make_webhook_url", "").strip()
    try:
        r = requests.post(webhook_url, json=payload)
        if r.status_code == 200:
            st.success("🎯 Datos enviados al CRM correctamente")
        else:
            st.warning(f"Error al enviar datos: {r.status_code}")
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Reporte de Capacidad de Pago", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Ingreso mensual: ${ingreso_mensual:,.2f}", ln=True)
    pdf.cell(200, 10, f"Porcentaje destinado: {porcentaje_destinado}%", ln=True)
    pdf.cell(200, 10, f"Plazo seleccionado: {plazo} años", ln=True)
    pdf.cell(200, 10, f"Tasa anual: {tasa_anual}%", ln=True)
    pdf.cell(200, 10, f"Mensualidad estimada: ${mensualidad:,.2f}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Capacidad de compra estimada: ${capacidad_credito:,.2f}", ln=True)
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    pdf.set_font("Arial", "I", 10)
    pdf.ln(10)
    pdf.cell(200, 10, f"Generado por HabitaMatch · {fecha}", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        with open(tmpfile.name, "rb") as f:
            st.balloons()
            st.download_button("📄 Descargar reporte PDF", f, file_name="capacidad_pago.pdf")

# Reset manual
if st.button("🔁 Finalizar y limpiar formulario"):
    st.session_state.clear()
    st.rerun()