from flask import Flask, request, jsonify
from fpdf import FPDF
import datetime
import tempfile
import os

app = Flask(__name__)

def calcular_capacidad(ingreso_mensual, porcentaje, plazo, tasa):
    mensualidad = ingreso_mensual * (porcentaje / 100)
    factor = (tasa / 100) / 12
    n = plazo * 12
    try:
        capacidad_credito = mensualidad * ((1 - (1 + factor) ** -n) / factor)
    except ZeroDivisionError:
        capacidad_credito = 0
    return round(mensualidad, 2), round(capacidad_credito, 2)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()

    ingreso_mensual = float(data.get("ingreso_mensual", 0))
    porcentaje = float(data.get("porcentaje", 30))
    plazo = int(data.get("plazo", 20))
    tasa = float(data.get("tasa", 10))
    nombre = data.get("nombre", "Cliente")
    correo = data.get("correo", "")

    mensualidad, capacidad_credito = calcular_capacidad(ingreso_mensual, porcentaje, plazo, tasa)

    # Generar PDF opcional
    pdf_path = None
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Reporte de Capacidad de Pago", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Ingreso mensual: ${ingreso_mensual:,.2f}", ln=True)
        pdf.cell(200, 10, f"Porcentaje destinado: {porcentaje}%", ln=True)
        pdf.cell(200, 10, f"Plazo: {plazo} años", ln=True)
        pdf.cell(200, 10, f"Tasa anual: {tasa}%", ln=True)
        pdf.cell(200, 10, f"Mensualidad estimada: ${mensualidad:,.2f}", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, f"Capacidad de compra: ${capacidad_credito:,.2f}", ln=True)
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        pdf.set_font("Arial", "I", 10)
        pdf.ln(10)
        pdf.cell(200, 10, f"Generado por HabitaMatch · {fecha}", ln=True)

        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(tmpfile.name)
        pdf_path = tmpfile.name
    except Exception as e:
        print("Error generando PDF:", e)

    return jsonify({
        "nombre": nombre,
        "correo": correo,
        "ingreso_mensual": ingreso_mensual,
        "porcentaje": porcentaje,
        "plazo": plazo,
        "tasa": tasa,
        "mensualidad": mensualidad,
        "capacidad_credito": capacidad_credito,
        "pdf_path": pdf_path
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)