<p align="center">
  <img src="https://raw.githubusercontent.com/AltairaGroup/habitamatch/main/assets/habitamatch_logo.png" width="200" alt="HabitaMatch Logo">
</p>

<h1 align="center">🏠 Calculadora de Capacidad de Pago · HabitaMatch</h1>

<p align="center">
  <strong>Evalúa tu capacidad hipotecaria al instante.</strong><br>
  Automatiza flujo → genera PDF → envía al CRM → todo con IA y Make ⚙️📤
</p>

<p align="center">
  <img src="https://img.shields.io/badge/streamlit-ready-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/make.com-integrated-blueviolet?style=for-the-badge&logo=webhooks&logoColor=white">
  <img src="https://img.shields.io/badge/pdf-auto_generated-orange?style=for-the-badge&logo=adobeacrobatreader">
</p>

---

## 🧠 ¿Qué hace esta calculadora?

Esta aplicación en Streamlit calcula la capacidad de compra de una persona con base en su:

- Ingreso mensual
- Plazo del crédito
- Porcentaje destinado
- Tasa de interés

Y permite:

✅ Descargar un PDF con los resultados  
✅ Enviar los datos al CRM vía [Make.com](https://www.make.com/)  
✅ Limpiar el formulario con un botón especial de "Finalizar"

---

## 🚀 Cómo usar

1. Clona este repositorio:
   ```bash
   git clone https://github.com/AltairaGroup/habitamatch.git
   cd habitamatch
   ```

2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura el archivo `.streamlit/secrets.toml` con tu webhook personalizado:

   ```toml
   make_webhook_url = "https://hook.us2.make.com/tu-webhook-url"
   ```

4. Ejecuta la app:
   ```bash
   streamlit run calculadora_capacidad_pago.py
   ```

---

## 🧱 Estructura del proyecto

```
HabitaMatch_Calculadora/
├── calculadora_capacidad_pago.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

---

## 💡 Ideal para:

- Portales inmobiliarios inteligentes
- Brokers o asesores hipotecarios
- CRM automatizados con Make
- Integración con recomendadores de vivienda

---

## 🤖 Powered by

<div align="center">
  <img src="https://raw.githubusercontent.com/AltairaGroup/assets/main/logos/altaira_black.png" height="40">
  <img src="https://raw.githubusercontent.com/AltairaGroup/assets/main/logos/corevia_white.png" height="40">
</div>

---

📩 ¿Dudas o mejoras?  
Contáctanos vía [Altaira Group](https://altairagroup.mx) o [Corevia AI](https://corevia.ai) 🚀