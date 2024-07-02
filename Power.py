import streamlit as st
import pandas as pd
import plotly.express as px

# Leer el archivo CSV
datos = "openipf-2024-06-01-5839592a.csv"
datos_csv = pd.read_csv(datos)

# Convertir la columna 'Date' a tipo datetime
datos_csv['Date'] = pd.to_datetime(datos_csv['Date'])

# Título de la página
st.set_page_config(page_title="Power Pro Metrics", layout="wide")
st.title('Power Pro Metrics')


# Creaar dos columnas separadas para la imagen y el texto
col1, col2 = st.columns(2)

# En la primera columna colocar la imagen
col1.image("Agata.jpg", caption='Agata Sitko : Female winner of the 2024 SBD Sheffield Powerlifting Championships', width=300)

# En la segunda columna colocar el texto
texto = """
¡Bienvenido a Power Pro Metrics!

Esta plataforma te permite explorar las estadísticas y métricas más relevantes del mundo del powerlifting. Utiliza los filtros a tu izquierda para seleccionar el año, la federación y la categoría de peso de tu interés. Aquí encontrarás una distribución detallada por sexo, así como los datos de los top 10 atletas con los máximos pesos en squat, bench y deadlift.

¡Explora y descubre los logros más impresionantes del powerlifting!

"""

# Mostramos el texto
col2.markdown(f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>", unsafe_allow_html=True)


# Sidebar para seleccionar parámetros
st.sidebar.header('Filtros')
# Selector de año
selected_year = st.sidebar.selectbox('Selecciona un año', sorted(datos_csv['Date'].dt.year.unique()))

# Selector de federación
selected_fed = st.sidebar.selectbox('Selecciona una federación', datos_csv['Federation'].unique())

# Selector de categoría de peso con opción 'Todas las categorías'
categorias_peso = ['Todas las categorías'] + list(datos_csv['WeightClassKg'].unique())
selected_weightclass = st.sidebar.selectbox('Selecciona una categoría de peso', categorias_peso)

# Filtrar datos por año, federación y categoría de peso seleccionados
if selected_weightclass == 'Todas las categorías':
    datos_filtrados = datos_csv[(datos_csv['Date'].dt.year == selected_year) &
                                (datos_csv['Federation'] == selected_fed)]
else:
    datos_filtrados = datos_csv[(datos_csv['Date'].dt.year == selected_year) &
                                (datos_csv['Federation'] == selected_fed) &
                                (datos_csv['WeightClassKg'] == selected_weightclass)]

# Verificar si hay datos filtrados antes de generar gráficos
if datos_filtrados.empty:
    st.warning("No hay datos disponibles para los criterios seleccionados.")
else:
    # Verificar si la columna 'Sex' está presente en datos_filtrados
    if 'Sex' in datos_filtrados.columns:
        # Gráfico de pie: Distribución por Sexo
        datos_sexo = datos_filtrados["Sex"].value_counts()
        fig_sexo = px.pie(datos_sexo, values=datos_sexo.values, names=datos_sexo.index, title='Distribución por Sexo', color_discrete_sequence=['blue','red'])
        #Mostrar gráfico de pie 
        st.plotly_chart(fig_sexo, use_container_width=True)

        # Gráfico de barras: Top 10 Personas con Máximo Peso en Squat
        if 'Best3SquatKg' in datos_filtrados.columns:
            top_10_squat = datos_filtrados.sort_values(by='Best3SquatKg', ascending=False).head(10)[['Name', 'Best3SquatKg']]
            fig_top_10_squat = px.bar(top_10_squat, x='Name', y='Best3SquatKg', title='Top 10 Personas con Máximo Peso en Squat',
                                      labels={'Name': 'Nombre del atleta', 'Best3SquatKg': 'Máximo Peso en Squat (kg)'},
                                       color_discrete_sequence=['blue'])

            # Mostrar gráfico de barras de Squat
            st.plotly_chart(fig_top_10_squat, use_container_width=True)

        else:
            st.error("No se encontró la columna 'Best3SquatKg' en los datos filtrados.")

        # Gráfico de barras: Top 10 Personas con Máximo Peso en Bench Press
        if 'Best3BenchKg' in datos_filtrados.columns:
            top_10_bench = datos_filtrados.sort_values(by='Best3BenchKg', ascending=False).head(10)[['Name', 'Best3BenchKg']]
            fig_top_10_bench = px.bar(top_10_bench, x='Name', y='Best3BenchKg', title='Top 10 Personas con Máximo Peso en Bench Press',
                                      labels={'Name': 'Nombre del atleta', 'Best3BenchKg': 'Máximo Peso en Bench Press (kg)'},
                                       color_discrete_sequence=['red'])

            # Mostrar gráfico de barras de Bench Press
            st.plotly_chart(fig_top_10_bench, use_container_width=True)

        else:
            st.error("No se encontró la columna 'Best3BenchKg' en los datos filtrados.")

        # Gráfico de barras: Top 10 Personas con Máximo Peso en Deadlift
        if 'Best3DeadliftKg' in datos_filtrados.columns:
            top_10_deadlift = datos_filtrados.sort_values(by='Best3DeadliftKg', ascending=False).head(10)[['Name', 'Best3DeadliftKg']]
            fig_top_10_deadlift = px.bar(top_10_deadlift, x='Name', y='Best3DeadliftKg', title='Top 10 Personas con Máximo Peso en Deadlift',
                                         labels={'Name': 'Nombre del atleta', 'Best3DeadliftKg': 'Máximo Peso en Deadlift (kg)'},
                                          color_discrete_sequence=['blue'])

            # Mostrar gráfico de barras de Deadlift
            st.plotly_chart(fig_top_10_deadlift, use_container_width=True)

        else:
            st.error("No se encontró la columna 'Best3DeadliftKg' en los datos filtrados.")

    else:
        st.error("No se encontró la columna 'Sex' en los datos filtrados.")
