# ==============================================================================
# PROYECTO: ANALIZADOR Y CALCULADORA INTERACTIVA DEL TEOREMA DE BAYES
# INSTITUCIÓN: Universidad Católica del Maule (UCM)
# ------------------------------------------------------------------------------
# LIBRERÍAS UTILIZADAS Y SU PROPÓSITO:
# 1. streamlit (st): Framework de interfaz gráfica para crear la aplicación web interactiva.
# 2. pandas (pd): Librería de manipulación y análisis de datos. Permite leer los CSV, 
#    filtrar filas y calcular promedios/sumatorias necesarias para las probabilidades.
# 3. matplotlib.pyplot (plt): Librería de visualización gráfica. Se utiliza para construir 
#    el diagrama de árbol de probabilidades dibujando sus nodos, ramas y porcentajes.
# 4. io: Módulo estándar de Python que administra flujos de memoria. Permite convertir 
#    la gráfica generada en un archivo de imagen descargable (PNG).
# 5. os: Módulo del sistema operativo. Se utiliza para verificar si existe el archivo 
#    de historial en el disco antes de leerlo o escribirlo.
# ==============================================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN INICIAL DE LA INTERFAZ WEB
# ------------------------------------------------------------------------------
# Configura el título de la pestaña del navegador, el icono y el ancho de la pantalla.
st.set_page_config(
    page_title="Analizador Bayesiano de Datos — UCM",
    page_icon="📊",
    layout="wide"
)

# Definición del nombre del archivo donde se almacenará el historial persistente
HISTORIAL_FILE = "historial_casos_guardados.csv"

# Encabezados principales de la aplicación web
st.title("Analizador y Calculadora Interactiva del Teorema de Bayes")
st.markdown("Herramienta analítica para el procesamiento de datos reales, cálculo de probabilidades y diagramas de árbol.")

# ------------------------------------------------------------------------------
# 2. MENÚ LATERAL DE NAVEGACIÓN
# ------------------------------------------------------------------------------
# Ofrece tres opciones de navegación para organizar la experiencia de usuario.
menu = st.sidebar.selectbox(
    "Menú Principal",
    ["1. Analizar y Guardar Nuevo Caso (CSV)", "2. Historial de Casos Analizados", "3. Instructivo de Formato CSV"]
)

# ------------------------------------------------------------------------------
# 3. FUNCIONES AUXILIARES Y DE PROCESAMIENTO
# ------------------------------------------------------------------------------

def limpiar_valor_numerico(val):
    """
    Función de sanitización de datos.
    Propósito: Recibe un dato de entrada (texto, porcentaje o número) y lo convierte 
    en un valor numérico flotante limpio de Python (float).
    Entrada: 'val' (Cualquier valor leído del CSV, como '20.33%', '2.898' o NaN).
    Salida: Número flotante listo para realizar operaciones matemáticas.
    """
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip().replace('%', '')
    
    # Manejo de formatos numéricos locales (puntos de miles y comas decimales)
    if '.' in val_str and ',' in val_str:
        val_str = val_str.replace('.', '').replace(',', '.')
    elif ',' in val_str:
        val_str = val_str.replace(',', '.')
    try:
        return float(val_str)
    except ValueError:
        return 0.0


def dibujar_diagrama_arbol(p_a, p_b_dado_a, p_b_dado_no_a, nombre_a="A", nombre_b="B"):
    """
    Función de visualización matemática.
    Propósito: Construye mediante coordenadas un Diagrama de Árbol de Probabilidades completo, 
    calculando los complementos, probabilidades condicionales y las 4 probabilidades conjuntas finales.
    Entradas:
      - p_a: Probabilidad Priori P(A).
      - p_b_dado_a: Probabilidad Condicional P(B|A) [Sensibilidad / Tasa Verdadero Positivo].
      - p_b_dado_no_a: Probabilidad Condicional P(B|A^c) [Falsos Positivos].
      - nombre_a / nombre_b: Etiquetas textuales para personalizar los nodos del árbol.
    Salida: Objeto 'fig' de Matplotlib que contiene la gráfica generada.
    """
    # Cálculos de los eventos complementarios (Regla del Complemento: P(A^c) = 1 - P(A))
    p_no_a = 1.0 - p_a
    p_no_b_dado_a = 1.0 - p_b_dado_a
    p_no_b_dado_no_a = 1.0 - p_b_dado_no_a
    
    # Cálculo de las 4 Probabilidades Conjuntas (Regla de la Multiplicación: P(A ∩ B) = P(A) * P(B|A))
    p_a_b = p_a * p_b_dado_a            # Rama 1: A ocurre y B ocurre
    p_a_nob = p_a * p_no_b_dado_a        # Rama 2: A ocurre y B no ocurre
    p_noa_b = p_no_a * p_b_dado_no_a     # Rama 3: A no ocurre y B ocurre
    p_noa_nob = p_no_a * p_no_b_dado_no_a # Rama 4: A no ocurre y B no ocurre

    # Creación del lienzo gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')  # Oculta los ejes Cartesianos para mostrar solo el esquema del árbol

    # Definición de las coordenadas X e Y de cada nivel de los nodos
    x0, y0 = 0.05, 0.5                  # Nivel 0: Raíz (Población inicial)
    x1, y1_a, y1_noa = 0.35, 0.75, 0.25  # Nivel 1: Hipótesis A y Complemento No A
    x2 = 0.70                           # Nivel 2: Resultados de Evidencia B y No B
    y2_a_b, y2_a_nob = 0.88, 0.62
    y2_noa_b, y2_noa_nob = 0.38, 0.12

    # Dibujo de las líneas (Ramas del árbol)
    ax.plot([x0, x1], [y0, y1_a], color='#08519c', lw=2)
    ax.plot([x0, x1], [y0, y1_noa], color='#9ecae1', lw=2)
    ax.plot([x1, x2], [y1_a, y2_a_b], color='#08519c', lw=1.5)
    ax.plot([x1, x2], [y1_a, y2_a_nob], color='#4292c6', lw=1.5)
    ax.plot([x1, x2], [y1_noa, y2_noa_b], color='#fc9272', lw=1.5)
    ax.plot([x1, x2], [y1_noa, y2_noa_nob], color='#9ecae1', lw=1.5)

    # Inserción de textos con las probabilidades simples y condicionales en cada rama
    ax.text((x0+x1)/2, (y0+y1_a)/2 + 0.03, f"P({nombre_a}) = {p_a:.4f}", ha='center', va='bottom', fontsize=9, color='#08519c', fontweight='bold')
    ax.text((x0+x1)/2, (y0+y1_noa)/2 - 0.04, f"P(No {nombre_a}) = {p_no_a:.4f}", ha='center', va='top', fontsize=9, color='#08519c')

    ax.text((x1+x2)/2, (y1_a+y2_a_b)/2 + 0.02, f"P({nombre_b}|{nombre_a}) = {p_b_dado_a:.4f}", ha='center', va='bottom', fontsize=8)
    ax.text((x1+x2)/2, (y1_a+y2_a_nob)/2 - 0.02, f"P(No {nombre_b}|{nombre_a}) = {p_no_b_dado_a:.4f}", ha='center', va='top', fontsize=8)
    ax.text((x1+x2)/2, (y1_noa+y2_noa_b)/2 + 0.02, f"P({nombre_b}|No {nombre_a}) = {p_b_dado_no_a:.4f}", ha='center', va='bottom', fontsize=8)
    ax.text((x1+x2)/2, (y1_noa+y2_noa_nob)/2 - 0.02, f"P(No {nombre_b}|No {nombre_a}) = {p_no_b_dado_no_a:.4f}", ha='center', va='top', fontsize=8)

    # Dibujo de los puntos de unión (Nodos)
    ax.scatter(x0, y0, color='black', s=80, zorder=5)
    ax.text(x0 - 0.02, y0, "Población", ha='right', va='center', fontweight='bold', fontsize=10)

    ax.scatter([x1, x1], [y1_a, y1_noa], color='#08519c', s=60, zorder=5)
    ax.text(x1, y1_a + 0.04, f"{nombre_a}", ha='center', va='bottom', fontweight='bold')
    ax.text(x1, y1_noa - 0.04, f"No {nombre_a}", ha='center', va='top', fontweight='bold')

    # Visualización de los resultados de probabilidad conjunta al final de cada camino
    resultados = [
        (y2_a_b, f"{nombre_a} y {nombre_b}", p_a_b),
        (y2_a_nob, f"{nombre_a} y No {nombre_b}", p_a_nob),
        (y2_noa_b, f"No {nombre_a} y {nombre_b}", p_noa_b),
        (y2_noa_nob, f"No {nombre_a} y No {nombre_b}", p_noa_nob)
    ]

    for y_pos, label, val in resultados:
        ax.scatter(x2, y_pos, color='#08519c', s=40, zorder=5)
        ax.text(x2 + 0.02, y_pos, f"→  {label}: {val*100:.2f}%", ha='left', va='center', fontsize=9, fontweight='bold')

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(0.0, 1.0)
    plt.title("Diagrama de Árbol de Probabilidades", fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    return fig


# ==============================================================================
# SECCIÓN 1: PROCESAMIENTO, CÁLCULO DE BAYES Y CARGA DE DATOS (CSV)
# ==============================================================================
if menu == "1. Analizar y Guardar Nuevo Caso (CSV)":
    st.subheader("Carga de Datos y Configuración del Caso")
    
    # Entrada de variables del usuario mediante componentes de Streamlit
    nombre_caso = st.text_input("Nombre descriptivo del caso (Ej: Caso 1 - COVID-19 Minsal):", value="")
    archivo_subido = st.file_uploader("Sube tu archivo CSV preparado:", type=["csv"])
    
    if archivo_subido is not None:
        try:
            # Control de lectura con manejo de excepciones para tolerar codificaciones UTF-8 y Latin-1 (Excel)
            try:
                df = pd.read_csv(archivo_subido, sep=None, engine='python', encoding='utf-8')
            except UnicodeDecodeError:
                archivo_subido.seek(0)
                df = pd.read_csv(archivo_subido, sep=None, engine='python', encoding='latin-1')
                
            st.success("Archivo CSV cargado con éxito.")
            
            with st.expander("Vista previa de los datos"):
                st.dataframe(df.head(5))
                
            columnas = list(df.columns)
            # Normalización de los nombres de las columnas para evitar errores por tildes o mayúsculas
            col_norm = [c.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u') for c in columnas]
            
            # Algoritmo de detección del tipo de caso de estudio
            tiene_casos = any('caso' in c for c in col_norm)
            tiene_examenes = any('examen' in c for c in col_norm)
            es_caso_covid = tiene_casos and tiene_examenes
            
            # ------------------------------------------------------------------
            # MÓDULO A: PROCESAMIENTO DE DATOS AGREGADOS (Ej: CASO 1 - COVID-19)
            # ------------------------------------------------------------------
            if es_caso_covid:
                st.info("Detectado formato de Datos Agregados por Días (Caso COVID-19).")
                total_registros = len(df)
                
                # Identificación automática de índices de columnas
                idx_casos = [i for i, c in enumerate(col_norm) if 'caso' in c][0]
                idx_examenes = [i for i, c in enumerate(col_norm) if 'examen' in c][0]
                
                col_casos = columnas[idx_casos]
                col_examenes = columnas[idx_examenes]
                
                # Aplicación de limpieza y sumatorias acumuladas
                casos_sum = df[col_casos].apply(limpiar_valor_numerico).sum()
                examenes_sum = df[col_examenes].apply(limpiar_valor_numerico).sum()
                
                # Cálculo de la Probabilidad Priori P(A) [Positividad Ponderada]
                if examenes_sum > 0:
                    p_A = casos_sum / examenes_sum
                else:
                    p_A = 0.2033
                
                # Parámetros epidemiológicos clínicos fijados por protocolo médico
                p_B_dado_A = 0.693       # Sensibilidad P(Test+|Contagiado)
                p_B_dado_no_A = 0.007    # Tasa de Falsos Positivos P(Test+|Sano)
                nombre_a_txt, nombre_b_txt = "Contagiado", "Test Positivo"
                
            # ------------------------------------------------------------------
            # MÓDULO B: PROCESAMIENTO DE REGISTROS INDIVIDUALES (Ej: TRÁNSITO Y ENUSC)
            # ------------------------------------------------------------------
            else:
                st.info("Detectado formato de Registros Individuales (Binarios 1 y 0).")
                col_a = st.selectbox("Selecciona la columna de la Hipótesis [A] (Valores 1 o 0):", columnas)
                col_b = st.selectbox("Selecciona la columna de la Evidencia [B] (Valores 1 o 0):", columnas)
                
                df_limpio = df[[col_a, col_b]].dropna()
                total_registros = len(df_limpio)
                
                s_a = df_limpio[col_a].apply(limpiar_valor_numerico)
                s_b = df_limpio[col_b].apply(limpiar_valor_numerico)
                
                # Cálculo de P(A) como la media de la variable binaria (Total de 1s / Total de Filas)
                p_A = s_a.mean()
                
                # Cálculo de Probabilidades Condicionales P(B|A) y P(B|A^c) filtrando según el valor de A
                p_B_dado_A = s_b[s_a == 1].mean() if len(s_b[s_a == 1]) > 0 else 0
                p_B_dado_no_A = s_b[s_a == 0].mean() if len(s_b[s_a == 0]) > 0 else 0
                nombre_a_txt, nombre_b_txt = col_a, col_b

            # Validación de muestra mínima requerida por la pauta académica
            if total_registros < 100:
                st.warning(f"Atención: El archivo tiene {total_registros} registros. La docente indicó un mínimo de 100 registros por caso.")
            else:
                st.success(f"Cumple con el criterio: {total_registros} registros analizados.")
                
            # ------------------------------------------------------------------
            # MÓDULO C: MOTOR DE CÁLCULO MATEMÁTICO DEL TEOREMA DE BAYES
            # ------------------------------------------------------------------
            # 1. Evento Complementario: P(A^c)
            p_no_A = 1.0 - p_A
            
            # 2. Aportes de la Evidencia (Numerador y Denominador de la Probabilidad Total)
            evidencia_A = p_B_dado_A * p_A             # P(B|A) * P(A)
            evidencia_no_A = p_B_dado_no_A * p_no_A     # P(B|A^c) * P(A^c)
            
            # 3. Teorema de la Probabilidad Total: P(B) = P(B|A)*P(A) + P(B|A^c)*P(A^c)
            p_B = evidencia_A + evidencia_no_A
            
            if p_B == 0:
                st.error("Error: La probabilidad total P(B) es 0.")
            else:
                # 4. TEOREMA DE BAYES: P(A|B) = [P(B|A) * P(A)] / P(B)
                p_A_dado_B = (p_B_dado_A * p_A) / p_B
                
                # 5. Evaluación de Independencia Estocástica: Razón = P(A|B) / P(A)
                razon_independencia = p_A_dado_B / p_A if p_A > 0 else 0
                
                # --------------------------------------------------------------
                # PRESENTACIÓN DE RESULTADOS EN LA INTERFAZ GÁFICA
                # --------------------------------------------------------------
                st.divider()
                st.subheader("Resultados del Análisis Bayesiano")
                
                # Despliegue de métricas resumidas
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric(label="Probabilidad Priori P(A)", value=f"{p_A * 100:.2f}%")
                with c2:
                    st.metric(label="Evidencia Total P(B)", value=f"{p_B * 100:.2f}%")
                with c3:
                    st.metric(label="Posterior P(A|B)", value=f"{p_A_dado_B * 100:.2f}%")
                
                # Explicación pedagógica de la sustitución matemática
                st.markdown("### Ilustración de la Fórmula Aplicada")
                st.latex(r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B|A) \cdot P(A) + P(B|A^c) \cdot P(A^c)}")
                st.markdown(f"""
                * **Sustitución de Valores Leídos:** 
                  $$P(A|B) = \\frac{{{p_B_dado_A:.4f} \\times {p_A:.4f}}}{{{p_B_dado_A:.4f} \\times {p_A:.4f} + {p_B_dado_no_A:.4f} \\times {p_no_A:.4f}}}$$
                * **Resultado Final del Cálculo:** **{p_A_dado_B * 100:.2f}%**
                * **Veredicto de Independencia:** Razón = **{razon_independencia:.2f}** -> *{"Eventos Dependientes (La evidencia modifica la probabilidad de la hipótesis)" if abs(razon_independencia - 1) > 0.05 else "Independencia Aproximada (La evidencia no altera significativamente la probabilidad priori)"}*
                """)
                
                # Generación e inclusión del Diagrama de Árbol
                st.divider()
                st.subheader("Diagrama de Árbol de Bayes")
                
                fig_arbol = dibujar_diagrama_arbol(p_A, p_B_dado_A, p_B_dado_no_A, nombre_a=nombre_a_txt, nombre_b=nombre_b_txt)
                st.pyplot(fig_arbol)
                
                # --------------------------------------------------------------
                # PERSISTENCIA DE DATOS: ALMACENAMIENTO EN CSV DE HISTORIAL
                # --------------------------------------------------------------
                if st.button("Guardar este caso en el Historial"):
                    if not nombre_caso.strip():
                        st.error("Por favor, asigna un nombre descriptivo al caso antes de guardarlo.")
                    else:
                        nuevo_registro = pd.DataFrame([{
                            "Nombre_Caso": nombre_caso,
                            "Registros": total_registros,
                            "Priori_P_A": f"{p_A * 100:.2f}%",
                            "Evidencia_P_B": f"{p_B * 100:.2f}%",
                            "Posterior_P_A_B": f"{p_A_dado_B * 100:.2f}%",
                            "Razon": f"{razon_independencia:.2f}"
                        }])
                        
                        # Concatenación con registros previos si el archivo existe
                        if os.path.exists(HISTORIAL_FILE):
                            hist_df = pd.read_csv(HISTORIAL_FILE)
                            hist_df = pd.concat([hist_df, nuevo_registro], ignore_index=True)
                        else:
                            hist_df = nuevo_registro
                            
                        hist_df.to_csv(HISTORIAL_FILE, index=False)
                        st.success(f"Caso '{nombre_caso}' guardado correctamente en el historial.")

                # Generación de archivo descargable en memoria (Memoria de StreamIO)
                st.divider()
                buf = io.BytesIO()
                fig_arbol.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                buf.seek(0)
                
                st.download_button(
                    label="Descargar Reporte y Diagrama de Árbol (PNG)",
                    data=buf,
                    file_name=f"reporte_{nombre_caso.lower().replace(' ', '_')}.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"Error procesando el archivo CSV: {e}")

# ==============================================================================
# SECCIÓN 2: CONSULTA DEL HISTORIAL CONSOLIDADO DE CASOS
# ==============================================================================
elif menu == "2. Historial de Casos Analizados":
    st.subheader("Historial de Casos Guardados")
    st.markdown("Consulta rápida de los análisis previos sin necesidad de repetir el proceso de carga.")
    
    if os.path.exists(HISTORIAL_FILE):
        hist_df = pd.read_csv(HISTORIAL_FILE)
        if len(hist_df) > 0:
            st.dataframe(hist_df, use_container_width=True)
            
            if st.button("Limpiar Historial"):
                os.remove(HISTORIAL_FILE)
                st.success("Historial eliminado con éxito. Recarga la página.")
                st.rerun()
        else:
            st.info("El historial está vacío. Analiza y guarda un caso desde la primera opción del menú.")
    else:
        st.info("No hay registros guardados todavía en el historial.")

# ==============================================================================
# SECCIÓN 3: INSTRUCTIVO TÉCNICO DE FORMATOS CSV
# ==============================================================================
elif menu == "3. Instructivo de Formato CSV":
    st.subheader("Instructivo: Cómo preparar tu CSV en Excel")
    st.markdown("""
    Para que la aplicación procese correctamente tus datos y cumpla con el requisito de **mínimo 100 registros**, existen dos formatos compatibles que puedes usar:
    
    #### 1. Formato Agregado por Días (Ej: Caso COVID-19)
    * Ideal para datos de reportes diarios o históricos agrupados por fecha.
    * Debe contener columnas como `casos` y `examenes` para calcular la probabilidad priori ponderada automáticamente.
    
    #### 2. Formato de Registros Individuales (Ej: Casos de Tránsito o ENUSC)
    * Cada fila representa una persona u hogar único.
    * Las variables de análisis deben usar estrictamente valores **1** (cuando el evento ocurre) y **0** (cuando no ocurre).
    * Columnas clave requeridas:
      * **Hipótesis ($A$):** Evento principal (ej. `victima`, `fallecido`).
      * **Evidencia ($B$):** Señal observada (ej. `noche`, `percepcion_aumento`).
    
    **Exportación:** 
    * Ve a **Archivo > Guardar como** en Excel.
    * Selecciona el tipo de archivo: **CSV (delimitado por comas) (*.csv)** y guárdalo en la carpeta del proyecto.
    """)