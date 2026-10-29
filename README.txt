DOCUMENTACIÓN Y GUÍA DE USO DE LA APLICACIÓN
Analizador y Calculadora Interactiva del Teorema de Bayes
1. Resumen Breve del Proyecto
Esta aplicación es un software interactivo desarrollado en Python mediante la librería Streamlit para el procesamiento, análisis probabilístico y visualización del Teorema de Bayes a partir de conjuntos de datos reales en Chile. El sistema soporta tanto datos agregados por periodos como datos a nivel individual con estructura binaria (1 y 0), calculando automáticamente la probabilidad a priori P(A), la evidencia total P(B), la probabilidad a posteriori P(A|B), el veredicto de independencia y la generación de diagramas de árbol de decisión explicativos.
Estructura de Archivos del Proyecto
La aplicación está organizada siguiendo la estructura oficial de carpetas:

Proyecto_Analisis_Datos/
│
├── casos-csv/
│   ├── caso1_covid.csv
│   ├── caso2_transito.csv
│   └── caso3_enusc.csv
│
├── app.py
└── historial_casos_guardados.csv

2. Instructivo de Verificación e Instalación
Para ejecutar esta aplicación en cualquier equipo, se requiere contar con Python 3.10 o superior y las librerías necesarias.
Paso 2.1: Verificar o Descargar Python
•	Abre tu terminal (PowerShell o Símbolo del sistema en Windows, o Terminal en macOS/Linux).
•	Ejecuta el siguiente comando para verificar si Python está instalado:

python --version

•	Si la terminal responde con una versión como Python 3.10.x, 3.11.x o 3.12.x, ya cuentas con Python.
•	Nota Importante: En caso de no tenerlo instalado, descárgalo directamente desde el sitio oficial python.org/downloads. Asegúrate de marcar la opción 'Add Python to PATH' durante la instalación en Windows.
Paso 2.2: Instalar Librerías Requeridas
Ejecuta el siguiente comando en la terminal para instalar Streamlit, Pandas y Matplotlib:

pip install streamlit pandas matplotlib

3. Instrucciones para Encender la Aplicación Web
•	Abre la terminal de comandos en VS Code o tu sistema operativo.
•	Asegúrate de estar posicionado en la carpeta raíz del proyecto (Proyecto_Analisis_Datos).
•	Ejecuta el comando de arranque de Streamlit:

streamlit run app.py

•	La aplicación se desplegará automáticamente en tu navegador web predeterminado en la dirección http://localhost:8501.
4. Paso a Paso para Cargar y Probar los Archivos .csv
La carpeta 'casos-csv' contiene los tres archivos listos para ser cargados en la aplicación.
Caso 1: Reportes COVID-19 (Minsal)
•	En la aplicación, selecciona el Menú Principal '1. Analizar y Guardar Nuevo Caso (CSV)'.
•	En el campo 'Nombre descriptivo del caso', ingresa: Caso 1 - COVID-19 Minsal.
•	Haz clic en 'Browse files' y navega hasta la carpeta casos-csv/ para seleccionar el archivo caso1_covid.csv.
•	Resultado Esperado: Verificación de Resultados: La aplicación detectará automáticamente el formato de datos agregados por días. Mostrará una probabilidad priori P(A) del 20.33%, una posterior P(A|B) del 96.19% y el diagrama de árbol de diagnóstico.
•	Haz clic en el botón 'Guardar este caso en el Historial'.
Caso 2: Siniestros de Tránsito (CONASET)
•	En el campo de nombre descriptivo, ingresa: Caso 2 - Siniestros de Tránsito CONASET.
•	Haz clic en 'Browse files' y selecciona el archivo casos-csv/caso2_transito.csv.
•	En los desplegables de selección de columnas, configura:
•	Hipótesis [A]: fallecido
•	Evidencia [B]: noche
•	Resultado Esperado: Verificación de Resultados: Analizará más de 52,000 registros, entregando una priori P(A) del 0.84%, una evidencia P(B) del 21.27% y una posterior P(A|B) del 1.73% (con razón de independencia = 2.05, confirmando que la probabilidad de fatalidad se duplica en horario nocturno).
•	Haz clic en 'Guardar este caso en el Historial'.
Caso 3: Seguridad y Victimización (ENUSC 2025)
•	En el campo de nombre descriptivo, ingresa: Caso 3 - Victimización y Percepción (ENUSC 2025).
•	Haz clic en 'Browse files' y selecciona el archivo casos-csv/caso3_enusc.csv.
•	En los desplegables de selección de columnas, configura:
•	Hipótesis [A]: VP_DC
•	Evidencia [B]: percepcion_aumento
•	Resultado Esperado: Verificación de Resultados: Procesará más de 54,000 registros con una priori P(A) del 23.87%, una posterior del 23.68% y un veredicto de Independencia Aproximada (razón = 0.99).
•	Haz clic en 'Guardar este caso en el Historial'.
Consulta de Historial Consolidado
Puedes acceder a la opción '2. Historial de Casos Analizados' en el menú lateral para revisar, comparar y presentar la tabla consolidada con los 3 casos guardados.

5. Indicaciones para Procesar y Preparar Nuevos Casos
Si deseas incorporar nuevas fuentes de datos o probar otros archivos que no estén en la carpeta oficial, debes seguir estos pasos de preparación en Excel:
Reglas de Limpieza para Registros Individuales (Binarios 1 y 0)
•	Limpieza de Números y Puntos: Selecciona las celdas numéricas, haz clic derecho -> Formato de celdas -> Número, y desmarca estrictamente la casilla 'Usar separador de miles (.)'. Esto evitará que Python confunda los puntos de miles con decimales.
•	Transformación a Variables Binarias: La columna de la Hipótesis [A] y la columna de la Evidencia [B] deben contener únicamente valores 1 (cuando el evento o condición se cumple) y 0 (cuando no se cumple). Si la encuesta usa opciones textuales o múltiples categorías, usa fórmulas como =SI(condicion; 1; 0) en Excel para convertirlas.
•	Fijar Fórmulas como Valores: Copia las columnas recién creadas con fórmulas y haz clic derecho -> Pegar como Valores para dejar únicamente los dígitos 1 y 0 numéricos.
•	Nombres de Encabezados Limpios: Asigna nombres de columna simples en la Fila 1, en minúsculas, sin espacios ni tildes (ejemplo: victima, noche, percepcion_aumento).
•	Exportación Estándar: Guarda el archivo mediante la opción Archivo -> Guardar como -> CSV (delimitado por comas) (*.csv) dentro de la carpeta casos-csv/.
Reglas para Datos Agregados por Días
•	Asegúrate de incluir en la primera fila de la tabla encabezados que contengan explícitamente las palabras 'casos' y 'examenes' (en minúsculas y sin separadores de miles) para que el algoritmo identifique automáticamente el cálculo ponderativo por periodos.
