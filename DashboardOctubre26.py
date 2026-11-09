
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard de Clientes y Productos", layout="wide")

st.title("🎯 Dashboard Analítico: Clientes, Productos y Descuentos")
st.markdown("Esta aplicación permite evaluar el comportamiento de los clientes, los productos más vendidos y el impacto de las reglas de descuento.")

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'SalidaVentas.xlsx'
    df = pd.read_excel(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

try:
    df = load_data()

    # Filtro lateral por Categoría
    st.sidebar.header("Filtros")
    categoria_seleccionada = st.sidebar.multiselect(
        "Selecciona Categorías:",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    # Filtrar datos
    df_filtrado = df[df['Category'].isin(categoria_seleccionada)]

    # Pestañas
    tab1, tab2, tab3 = st.tabs(["👥 Análisis de Clientes", "📦 Rendimiento de Productos", "💸 Impacto de Descuentos"])

    with tab1:
        st.header("Análisis de los Mejores Clientes")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Clientes por Ventas")
            top_clientes_sales = df_filtrado.groupby('Customer Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
            fig1, ax1 = plt.subplots()
            sns.barplot(data=top_clientes_sales, x='Sales', y='Customer Name', palette='Blues_r', ax=ax1)
            st.pyplot(fig1)
            
        with col2:
            st.subheader("Top 10 Clientes por Ganancia")
            top_clientes_profit = df_filtrado.groupby('Customer Name')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False).head(10)
            fig2, ax2 = plt.subplots()
            sns.barplot(data=top_clientes_profit, x='Profit', y='Customer Name', palette='Greens_r', ax=fig2.gca())
            st.pyplot(fig2)

    with tab2:
        st.header("Rendimiento de Productos y Subcategorías")
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Ventas por Subcategoría")
            subcat_sales = df_filtrado.groupby('Sub-Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
            fig3, ax3 = plt.subplots()
            sns.barplot(data=subcat_sales, x='Sales', y='Sub-Category', palette='viridis', ax=ax3)
            st.pyplot(fig3)
            
        with col4:
            st.subheader("Productos más vendidos (Top 10 por Cantidad)")
            top_prod_qty = df_filtrado.groupby('Product Name')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=False).head(10)
            fig4, ax4 = plt.subplots()
            # Acortar nombres largos de productos para la visualización
            top_prod_qty['Product Name Short'] = top_prod_qty['Product Name'].str[:30] + '...'
            sns.barplot(data=top_prod_qty, x='Quantity', y='Product Name Short', palette='rocket', ax=ax4)
            st.pyplot(fig4)

    with tab3:
        st.header("Análisis Financiero de Descuentos")
        st.markdown("Evalúa cómo el porcentaje de descuento afecta directamente el margen neto de ganancia.")
        
        col5, col6 = st.columns(2)
        
        with col5:
            st.subheader("Relación entre Descuento y Ganancias")
            fig5, ax5 = plt.subplots()
            sns.scatterplot(data=df_filtrado, x='Discount', y='Profit', alpha=0.5, hue='Category', ax=ax5)
            st.pyplot(fig5)
            
        with col6:
            st.subheader("Ganancia Promedio según Nivel de Descuento")
            discount_profit = df_filtrado.groupby('Discount')['Profit'].mean().reset_index()
            fig6, ax6 = plt.subplots()
            sns.lineplot(data=discount_profit, x='Discount', y='Profit', marker='o', color='red', ax=ax6)
            ax6.set_ylabel("Ganancia Promedio ($)")
            st.pyplot(fig6)

except Exception as e:
    st.error(f"Error al procesar el dashboard: {e}")
