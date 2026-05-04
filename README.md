# 🏠 Dashboard de Análisis y Predicción de Inmuebles en Bogotá

Aplicación web interactiva para explorar el mercado inmobiliario bogotano y predecir el valor de inmuebles usando Machine Learning.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)

---

## 📌 Descripción

Dashboard construido con Streamlit que permite cargar un CSV de inmuebles, explorar los datos visualmente y predecir el valor de una propiedad según su área y número de habitaciones mediante un modelo de **Regresión Lineal**.

---

## ✨ Funcionalidades

- 📊 KPIs principales: total de inmuebles, precio promedio y área promedio
- 🔍 Filtros interactivos por habitaciones y rango de área
- 📈 Gráfico de dispersión área vs. valor, coloreado por número de habitaciones
- 📉 Histograma de distribución de precios
- 🤖 Predictor de precios con Regresión Lineal
- 🧹 Limpieza automática de datos y eliminación de outliers con método IQR

---

## 🛠️ Tecnologías

| Librería | Uso |
|---|---|
| Streamlit | Interfaz web interactiva |
| Pandas | Carga y limpieza de datos |
| Plotly | Visualizaciones interactivas |
| scikit-learn | Modelo de Regresión Lineal |
| NumPy | Operaciones numéricas |

---

## 📁 Estructura esperada del CSV

El archivo `inmuebles_bogota.csv` debe tener estas columnas:

```
Habitaciones, Area, Valor
3, 85, $250.000.000
```

---

## 🚀 Instalación y uso

```bash
# 1. Clona el repositorio
git clone <url-del-repo>
cd <nombre-carpeta>

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Corre la aplicación
streamlit run app.py
```

---

## 👩‍💻 Desarrollado por

**Yisela Forero**  
[github.com/yiselaforero010](https://github.com/yiselaforero010)
