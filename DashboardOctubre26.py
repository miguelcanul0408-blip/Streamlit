import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Análisis de Clientes",
        "📦 Rendimiento de Productos",
        "💸 Impacto de Descuentos",
        "🗺️ Ventas por Estado"
    ])

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
            sns.barplot(data=top_clientes_profit, x='Profit', y='Customer Name', palette='Greens_r', ax=ax2())
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
            top_prod_qty['Product Name Short'] = top_prod_qty['Product Name'].apply(
                lambda nombre: nombre[:30] + '...' if len(nombre) > 30 else nombre
            )
            sns.barplot(data=top_prod_qty, x='Quantity', y='Product Name Short', palette='rocket', ax=ax4)
            st.pyplot(fig4)

        st.subheader("Top 10 productos más vendidos por categoría")
        if df_filtrado.empty:
            st.info("Selecciona al menos una categoría para ver los productos más vendidos.")
        else:
            productos_categoria = (
                df_filtrado.groupby(['Category', 'Product Name'], as_index=False)['Quantity']
                .sum()
                .sort_values(['Category', 'Quantity'], ascending=[True, False])
                .groupby('Category', group_keys=False)
                .head(10)
            )
            productos_categoria['Product Name Short'] = productos_categoria['Product Name'].apply(
                lambda nombre: nombre[:30] + '...' if len(nombre) > 30 else nombre
            )
            grafica_categoria = sns.catplot(
                data=productos_categoria,
                kind='bar',
                x='Quantity',
                y='Product Name Short',
                col='Category',
                col_wrap=2,
                sharex=False,
                height=4,
                aspect=1.3,
                palette='rocket'
            )
            grafica_categoria.set_axis_labels('Cantidad vendida', 'Producto')
            grafica_categoria.set_titles('{col_name}')
            st.pyplot(grafica_categoria.figure)
            plt.close(grafica_categoria.figure)

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

    with tab4:
        st.header("Ventas por estado")
        st.markdown("El color indica las ventas totales de cada estado y se actualiza al cambiar el filtro de categorías.")

        estados_us = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
            'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
            'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
            'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
            'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
            'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
            'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
            'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
            'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
            'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
            'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
            'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
            'Wisconsin': 'WI', 'Wyoming': 'WY'
        }
        nombre_a_codigo = {nombre.casefold(): codigo for nombre, codigo in estados_us.items()}
        codigo_a_codigo = {codigo.casefold(): codigo for codigo in estados_us.values()}
        estado_a_codigo = {**nombre_a_codigo, **codigo_a_codigo}

        if df_filtrado.empty:
            st.info("Selecciona al menos una categoría para ver el mapa.")
        elif 'State' not in df_filtrado.columns or 'Sales' not in df_filtrado.columns:
            st.error("El archivo debe incluir las columnas 'State' y 'Sales' para mostrar el mapa.")
        else:
            ventas_estado = df_filtrado[['State', 'Sales']].dropna().copy()
            ventas_estado['State Code'] = (
                ventas_estado['State'].astype(str).str.strip().str.casefold().map(estado_a_codigo)
            )
            ventas_estado['Sales'] = pd.to_numeric(ventas_estado['Sales'], errors='coerce')
            ventas_estado = ventas_estado.dropna(subset=['State Code', 'Sales'])
            ventas_estado = ventas_estado.groupby('State Code', as_index=False)['Sales'].sum()

            if ventas_estado.empty:
                st.warning("No se reconocieron estados para dibujar. La columna 'State' debe contener nombres de estados de EE. UU. o códigos como CA y TX.")
            else:
                try:
                    mapa_ventas = px.choropleth(
                        ventas_estado,
                        locations='State Code',
                        locationmode='USA-states',
                        color='Sales',
                        scope='usa',
                        color_continuous_scale='Blues',
                        labels={'Sales': 'Ventas ($)', 'State Code': 'Estado'},
                        title='Ventas totales por estado'
                    )
                    mapa_ventas.update_layout(
                        margin={'r': 0, 't': 50, 'l': 0, 'b': 0},
                        coloraxis_colorbar_title='Ventas ($)'
                    )
                    st.plotly_chart(mapa_ventas, use_container_width=True)
                except Exception as error_mapa:
                    st.error(f"No se pudo generar el mapa. Verifica que Plotly esté instalado y actualizado: {error_mapa}")

except Exception as e:
    st.error(f"Error al procesar el dashboard: {e}")
