import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURACIÓN INICIAL Y CARGA DE DATOS ---
st.header('Análisis Exploratorio de Datos de Vehículos Usados')

# Mensaje de depuración: indica que la aplicación comenzó a ejecutarse
st.write('¡Aplicación inicializada correctamente!')

# Ruta del archivo (asumiendo que está en la misma carpeta o la raíz)
FILE_PATH = 'vehicles_us.csv'

@st.cache_data
def load_data(path):
    """Carga los datos y realiza la limpieza inicial de tipos de datos."""
    try:
        df = pd.read_csv(path)
        # Convertir a minúsculas y reemplazar espacios por guiones bajos para facilitar el análisis
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        return df
    except FileNotFoundError:
        st.error(f"Error: El archivo {path} no fue encontrado. Asegúrate de que esté en la misma carpeta.")
        return pd.DataFrame() # Devuelve un DataFrame vacío en caso de error

df = load_data(FILE_PATH)

# Si el DataFrame está vacío debido a un error de carga, detenemos la ejecución
if df.empty:
    st.stop()

# --- 2. LIMPIEZA Y PRE-PROCESAMIENTO DE DATOS ---

# Imputación de columnas numéricas (model_year, cylinders, odometer) con la MEDIANA
median_model_year = df['model_year'].median()
median_cylinders = df['cylinders'].median()
median_odometer = df['odometer'].median()

df['model_year'].fillna(median_model_year, inplace=True)
df['cylinders'].fillna(median_cylinders, inplace=True)
df['odometer'].fillna(median_odometer, inplace=True)

# Imputación de columnas categóricas ('paint_color') con 'unknown'
df['paint_color'].fillna('unknown', inplace=True)

# Imputación de columna binaria ('is_4wd') con 0 y conversión a entero
df['is_4wd'].fillna(0, inplace=True)

# Conversión de tipos de datos a enteros
df['model_year'] = df['model_year'].astype(int)
df['cylinders'] = df['cylinders'].astype(int)
df['is_4wd'] = df['is_4wd'].astype(int)


# --- MOSTRAR DATOS AL INICIO ---
st.subheader('Datos Limpios (Primeras 5 Filas)')
st.dataframe(df.head())


# --- 3. FUNCIONALIDAD INTERACTIVA (CHECKBOXES) ---

st.subheader('Seleccione el Gráfico a Visualizar')

# Crear casillas de verificación para histograma
build_histogram = st.checkbox('Construir Histograma de Kilometraje')

# Crear casillas de verificación para gráfico de dispersión
build_scatter = st.checkbox('Construir Gráfico de Dispersión (Precio vs. Kilometraje)')

# --- 4. LÓGICA DE VISUALIZACIÓN ---

if build_histogram:
    st.write('### Distribución de Kilometraje (Odómetro)')
    
    # Usaremos plotly.graph_objects (go) como se sugirió en la tarea
    fig_hist = go.Figure(data=[go.Histogram(x=df['odometer'])])

    fig_hist.update_layout(
        title_text='Distribución del Odómetro',
        xaxis_title_text='Kilometraje (Millas)',
        yaxis_title_text='Conteo de Vehículos'
    )
    st.plotly_chart(fig_hist, use_container_width=True)

if build_scatter:
    st.write('### Relación entre Precio y Kilometraje')

    # Configuración de los parámetros en variables separadas
    x_col = "odometer"
    y_col = "price"
    color_col = "condition"
    hover_cols = ['model_year', 'model']
    title_text = 'Precio vs. Kilometraje por Condición del Vehículo'

    # Llamada a px.scatter con la sintaxis simplificada para evitar errores
    fig_scatter = px.scatter(df, x=x_col, y=y_col, 
                             color=color_col, 
                             hover_data=hover_cols,
                             title=title_text)
    st.plotly_chart(fig_scatter, use_container_width=True)