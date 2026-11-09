%%writefile app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análisis de Ventas y Ganancias", layout="wide")

st.title("📊 Dashboard de Análisis de Ventas y Ganancias (Streamlit)")
st.markdown("Este dashboard interactivo replica el análisis exploratorio realizado sobre los datos de ventas.")

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'SalidaVentas.xlsx'
    df = pd.read_excel(file_path)
    return df

try:
    df_ventas = load_data()
    
    # Métrica principal
    st.sidebar.header("Filtros de Datos")
    
    # KPI principales en el Dashboard
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total Ventas (Sales)", f"${df_ventas['Sales'].sum():,.2f}")
    with col_kpi2:
        st.metric("Total Ganancias (Profit)", f"${df_ventas['Profit'].sum():,.2f}")
    with col_kpi3:
        st.metric("Total Registros", f"{len(df_ventas):,}")

    # Sección 1: Distribución
    st.header("📈 Distribución de Sales y Profit")
    col1, col2 = st.columns(2)
    
    with col1:
        fig1, ax1 = plt.subplots()
        sns.histplot(df_ventas['Sales'], bins=50, kde=True, ax=ax1, color='blue')
        ax1.set_title('Distribución de Ventas (Escala Log)')
        ax1.set_yscale('log')
        st.pyplot(fig1)
        
    with col2:
        fig2, ax2 = plt.subplots()
        sns.histplot(df_ventas['Profit'], bins=50, kde=True, ax=ax2, color='green')
        ax2.set_title('Distribución de Ganancias (Escala Log)')
        ax2.set_yscale('log')
        st.pyplot(fig2)

    # Sección 2: Correlación
    st.header("🔍 Correlación entre Ventas y Ganancias")
    correlacion = df_ventas['Sales'].corr(df_ventas['Profit'])
    st.write(f"El coeficiente de correlación de Pearson es: **{correlacion:.4f}**")
    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.regplot(data=df_ventas, x='Sales', y='Profit', 
                scatter_kws={'alpha':0.3, 'color': 'blue'},
                line_kws={'color': 'red', 'linewidth': 2}, ax=ax3)
    ax3.set_title('Gráfico de Dispersión: Ventas vs Ganancias')
    st.pyplot(fig3)

    # Sección 3: Análisis Regional
    st.header("🌍 Análisis por Región")
    
    col_reg1, col_reg2 = st.columns(2)
    
    with col_reg1:
        st.subheader("Total de Ventas por Región")
        ventas_por_region = df_ventas.groupby('Region')['Sales'].sum().reset_index()
        fig4, ax4 = plt.subplots()
        ax4.pie(ventas_por_region['Sales'], labels=ventas_por_region['Region'], autopct='%1.1f%%', startangle=140)
        st.pyplot(fig4)
        
    with col_reg2:
        st.subheader("Total de Ganancias (Profit) por Región")
        profit_por_region = df_ventas.groupby('Region')['Profit'].sum().reset_index()
        fig5, ax5 = plt.subplots()
        ax5.pie(profit_por_region['Profit'], labels=profit_por_region['Region'], autopct='%1.1f%%', startangle=140)
        st.pyplot(fig5)

    # Sección 4: Filtro Interactivo por Región para Estados
    st.header("📍 Análisis Detallado por Estado")
    region_seleccionada = st.selectbox("Selecciona una Región para ver el detalle de sus Estados:", df_ventas['Region'].unique(), index=list(df_ventas['Region'].unique()).index('West') if 'West' in df_ventas['Region'].unique() else 0)
    
    df_filtrado = df_ventas[df_ventas['Region'] == region_seleccionada]
    
    col_est1, col_est2 = st.columns(2)
    
    with col_est1:
        st.subheader(f"Ventas por Estado en {region_seleccionada}")
        ventas_estado = df_filtrado.groupby('State')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
        fig6, ax6 = plt.subplots()
        sns.barplot(data=ventas_estado, x='State', y='Sales', palette='viridis', ax=ax6)
        plt.xticks(rotation=45)
        st.pyplot(fig6)
        
    with col_est2:
        st.subheader(f"Ganancias por Estado en {region_seleccionada}")
        profit_estado = df_filtrado.groupby('State')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False)
        fig7, ax7 = plt.subplots()
        sns.barplot(data=profit_estado, x='State', y='Profit', palette='magma', ax=ax7)
        plt.xticks(rotation=45)
        st.pyplot(fig7)

except Exception as e:
    st.error(f"Error al cargar el archivo de Excel: {e}")
    st.info("Asegúrate de tener montado Google Drive y que la ruta del archivo sea la correcta.")
