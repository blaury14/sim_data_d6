import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt

# Generar datos simulados iniciales
def generate_random_data():
    num_choferes = 15
    num_registros = 100
    choferes = [f'chofer_{i+1}' for i in range(num_choferes)]
    material_types = ['A-SBL', 'LBLM', 'OXI', 'SME', 'SBL', 'LOX', 'LSU', 'A-LOX']
    crew_groups = ['Grupo 1', 'Grupo 2', 'Grupo 3', 'Grupo 4']
    
    data = {
        'Año': np.full(num_registros, 2024),
        'Mes': np.random.choice(['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'], num_registros),
        'Día': np.random.randint(1, 29, num_registros),
        'Crew': np.random.choice(crew_groups, num_registros),
        'Suma de EmptyTravelDuration': np.random.uniform(0, 500, num_registros),
        'Suma de TotalDistance': np.random.uniform(500, 10000, num_registros),
        'Suma de TruckIdleTime': np.random.uniform(0, 1000, num_registros),
        'Suma de Tonnage': np.random.uniform(300, 400, num_registros),
        'MaterialType': np.random.choice(material_types, num_registros),
        'TruckOperatorName': np.random.choice(choferes, num_registros)
    }
    return pd.DataFrame(data)

# Función de simulación continua
def simulate_data():
    while True:
        new_data = generate_random_data()
        yield new_data

data_gen = simulate_data()

# Título de la aplicación
st.title('Simulación de Operaciones Mineras en Tiempo Real')

# Descripción de la aplicación
st.markdown("""
Esta aplicación muestra una simulación en tiempo real de operaciones mineras. Los datos se actualizan continuamente para reflejar las condiciones actuales de la mina.
""")

# Inicializar gráficos y dataframes vacíos
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('datos_simulados.csv')

# Gráfico de Tonelaje Total por Día
st.subheader('Tonelaje Total por Día')
tonnage_por_dia = st.session_state.df.groupby(['Mes', 'Día'])['Suma de Tonnage'].sum().reset_index()
tonnage_chart = alt.Chart(tonnage_por_dia).mark_line().encode(
    x='Día',
    y='Suma de Tonnage',
    color='Mes'
).properties(width=700, height=400)
st.altair_chart(tonnage_chart)

# Gráfico de Tiempo de Inactividad por Grupo
st.subheader('Tiempo de Inactividad por Grupo')
idle_time_por_grupo = st.session_state.df.groupby('Crew')['Suma de TruckIdleTime'].mean().reset_index()
idle_chart = alt.Chart(idle_time_por_grupo).mark_bar().encode(
    x='Crew',
    y='Suma de TruckIdleTime',
    color='Crew'
).properties(width=700, height=400)
st.altair_chart(idle_chart)

# Gráfico de Distancia Total Recorrida por Tipo de Material
st.subheader('Distancia Total Recorrida por Tipo de Material')
distance_por_material = st.session_state.df.groupby('MaterialType')['Suma de TotalDistance'].sum().reset_index()
distance_chart = alt.Chart(distance_por_material).mark_bar().encode(
    x='MaterialType',
    y='Suma de TotalDistance',
    color='MaterialType'
).properties(width=700, height=400)
st.altair_chart(distance_chart)

# Simulación en tiempo real
st.subheader('Actualización en Tiempo Real')
st.write("Actualización de datos en tiempo real:")

# Mostrar datos simulados en tiempo real
for _ in range(5):
    new_df = next(data_gen)
    st.write(new_df)
    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
    time.sleep(5)

# Refrescar gráficos con datos actualizados
tonnage_por_dia = st.session_state.df.groupby(['Mes', 'Día'])['Suma de Tonnage'].sum().reset_index()
tonnage_chart = alt.Chart(tonnage_por_dia).mark_line().encode(
    x='Día',
    y='Suma de Tonnage',
    color='Mes'
).properties(width=700, height=400)
st.altair_chart(tonnage_chart)

idle_time_por_grupo = st.session_state.df.groupby('Crew')['Suma de TruckIdleTime'].mean().reset_index()
idle_chart = alt.Chart(idle_time_por_grupo).mark_bar().encode(
    x='Crew',
    y='Suma de TruckIdleTime',
    color='Crew'
).properties(width=700, height=400)
st.altair_chart(idle_chart)

distance_por_material = st.session_state.df.groupby('MaterialType')['Suma de TotalDistance'].sum().reset_index()
distance_chart = alt.Chart(distance_por_material).mark_bar().encode(
    x='MaterialType',
    y='Suma de TotalDistance',
    color='MaterialType'
).properties(width=700, height=400)
st.altair_chart(distance_chart)
