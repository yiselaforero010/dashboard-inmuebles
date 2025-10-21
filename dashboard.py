import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Análisis de Inmuebles en Bogotá",
    page_icon="🏠",
    layout="wide"
)

# --- Funciones (Caché para optimizar rendimiento) ---

@st.cache_data # Esta función solo se ejecutará una vez para cargar los datos
def load_data(uploaded_file):
    """Carga y limpia los datos del archivo CSV."""
    df = pd.read_csv(uploaded_file)
    df_predictivo = df[['Habitaciones', 'Area', 'Valor']].copy()
    
    # Limpieza de datos
    df_predictivo['Valor'] = df_predictivo['Valor'].astype(str).str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.strip()
    df_predictivo['Valor'] = pd.to_numeric(df_predictivo['Valor'], errors='coerce')
    df_predictivo['Area'] = pd.to_numeric(df_predictivo['Area'], errors='coerce')
    df_predictivo.dropna(inplace=True)
    df_predictivo['Valor_Millones'] = df_predictivo['Valor'] / 1000000
    
    # Filtrado de outliers para un modelo y visualizaciones más robustas
    Q1 = df_predictivo[['Area', 'Valor_Millones']].quantile(0.25)
    Q3 = df_predictivo[['Area', 'Valor_Millones']].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    df_filtrado = df_predictivo[
        (df_predictivo['Area'] >= limite_inferior['Area']) & (df_predictivo['Area'] <= limite_superior['Area']) &
        (df_predictivo['Valor_Millones'] >= limite_inferior['Valor_Millones']) & (df_predictivo['Valor_Millones'] <= limite_superior['Valor_Millones'])
    ]
    return df_filtrado

@st.cache_resource # Esta función entrena y guarda el modelo
def train_model(df):
    """Entrena un modelo de Regresión Lineal."""
    X = df[['Habitaciones', 'Area']]
    y = df['Valor_Millones']
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo

# --- Interfaz Principal ---

st.title("🏠 Dashboard de Análisis y Predicción de Inmuebles en Bogotá")
st.markdown("Sube tu archivo `inmuebles_bogota.csv` para comenzar el análisis.")

# Widget para subir el archivo
uploaded_file = st.file_uploader("Selecciona tu archivo CSV", type="csv")

if uploaded_file is not None:
    # Cargar y entrenar
    df_inmuebles = load_data(uploaded_file)
    modelo = train_model(df_inmuebles)

    # --- Sidebar de Filtros ---
    st.sidebar.header("Filtros Interactivos")
    
    # Filtro por número de habitaciones
    hab_seleccionadas = st.sidebar.multiselect(
        "Número de Habitaciones",
        options=sorted(df_inmuebles['Habitaciones'].unique()),
        default=sorted(df_inmuebles['Habitaciones'].unique())
    )

    # Filtro por rango de Área
    area_min, area_max = st.sidebar.slider(
        "Rango de Área (m²)",
        min_value=int(df_inmuebles['Area'].min()),
        max_value=int(df_inmuebles['Area'].max()),
        value=(int(df_inmuebles['Area'].min()), int(df_inmuebles['Area'].max()))
    )

    # Aplicar filtros al DataFrame
    df_filtrado_ui = df_inmuebles[
        (df_inmuebles['Habitaciones'].isin(hab_seleccionadas)) &
        (df_inmuebles['Area'] >= area_min) &
        (df_inmuebles['Area'] <= area_max)
    ]

    st.header("Análisis Exploratorio de Datos")
    
    # --- Métricas Clave (KPIs) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Inmuebles", f"{df_filtrado_ui.shape[0]:,}")
    with col2:
        st.metric("Precio Promedio (Millones)", f"${df_filtrado_ui['Valor_Millones'].mean():,.2f}")
    with col3:
        st.metric("Área Promedio (m²)", f"{df_filtrado_ui['Area'].mean():,.2f}")

    # --- Visualizaciones Interactivas ---
    st.subheader("Relación entre Área y Valor del Inmueble")
    fig_scatter = px.scatter(
        df_filtrado_ui,
        x="Area",
        y="Valor_Millones",
        color="Habitaciones",
        hover_data=['Habitaciones', 'Area', 'Valor_Millones'],
        title="Área vs. Valor (coloreado por N° de Habitaciones)",
        labels={'Area': 'Área (m²)', 'Valor_Millones': 'Valor (Millones $)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.subheader("Distribución de Precios")
    fig_hist = px.histogram(
        df_filtrado_ui,
        x="Valor_Millones",
        nbins=50,
        title="Frecuencia de Inmuebles por Rango de Precios",
        labels={'Valor_Millones': 'Valor (Millones $)'}
    )
    st.plotly_chart(fig_hist, use_container_width=True)


    # --- Herramienta de Predicción ---
    st.header("Predice el Valor de un Inmueble")
    
    with st.form("prediction_form"):
        st.write("Introduce las características del inmueble para obtener una estimación de su valor.")
        
        # Inputs para el usuario
        input_habitaciones = st.number_input("Número de Habitaciones", min_value=1, max_value=10, value=3, step=1)
        input_area = st.number_input("Área del Inmueble (m²)", min_value=20, max_value=500, value=100, step=5)
        
        # Botón para enviar el formulario
        submitted = st.form_submit_button("Predecir Valor")

        if submitted:
            # Crear DataFrame para la predicción
            datos_nuevos = pd.DataFrame([[input_habitaciones, input_area]], columns=['Habitaciones', 'Area'])
            
            # Realizar la predicción
            precio_predicho = modelo.predict(datos_nuevos)[0]
            precio_mostrado = max(0, precio_predicho) # Asegurarse de no mostrar valores negativos
            
            st.success(f"**El valor estimado del inmueble es de: ${precio_mostrado:,.2f} millones de pesos.**")
            st.info("Nota: Esta es una estimación basada en un modelo de regresión lineal y los datos proporcionados.")

else:
    st.info("Esperando a que se cargue el archivo `inmuebles_bogota.csv`...")

